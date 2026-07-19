# 14 LangGraph 工程实战专项

## 0. 章节元信息

- 主要能力：C03.03
- 关联能力：C03.02、C04.02、C08.02
- 练习协议：[统一练习协议](../../interviews-docs/practice-protocol.md)
- 官方文档访问日期：2026-07-19

本章用 LangGraph 映射有状态 Workflow，重点是持久化、中断恢复和受控副作用。API 名称会变，状态边界不能含糊。

## 1. 冷启动设计题

不看下文，先为“发送客户通知”写一份 `langgraph-hitl-cold.md`：

1. 定义状态字段，区分 proposed、approved、rejected、executed。
2. 画出图从提案、暂停、恢复到执行结果验证的路径。
3. 写出稳定 thread identity、幂等键和失败/取消出口。
4. 标出 interrupt 前后哪些代码可能重新执行。

产物要能让另一位工程师检查每条状态转换。只读代码、复制 API 或勾选清单都不是独立证据。

### 迁移题

改变约束：审批人可以编辑收件人和正文，而且服务在暂停期间会重启。更新 `langgraph-hitl-cold.md`，说明恢复后在哪里重新校验、怎样避免把批准当作已经发送。

### 延迟复测

隔天从空白页重画，保存 `langgraph-hitl-retest.md`。解释不清 node restart 或工具结果验证时，继续保留为待复测项。

<!-- LangGraph 参考分隔线：完成冷答后再继续 -->

## 2. 用图表达什么

LangGraph 适合有状态、多步骤、带分支或循环，并且需要恢复的任务。单轮分类、固定的两步调用，用普通函数往往更直接。

```text
State：图在一次 thread 中的业务状态
Node：读取 State，返回部分更新
Edge：固定流转
Conditional Edge：按确定的状态字段分支
Checkpointer：按 thread 保存 checkpoint
Store：跨 thread 的长期数据，不等同于 checkpointer
```

State 应有明确 schema。原始大文档、密钥和无界历史不要塞进 State；可保存引用或受控摘要。

## 3. 常见工作流模式

### Router

Router 把结构化分类映射到固定节点。不要直接用模型自由文本作为节点名。

```text
classify → retrieve | use_tool | answer | reject
```

### Planner–Executor

Planner 生成有限步骤，Executor 每次执行一个步骤，Router 根据观察结果继续、结束或转人工。必须有最大步数、超时和失败出口。

### Evaluator–Optimizer

生成、评估、修改形成闭环，适合受 rubric 约束的产物。循环次数和成本都要封顶，评估未通过不能伪装成 success。

## 4. Checkpointer 与 thread

interrupt 依赖持久化。图要用 checkpointer 编译，每次调用带稳定的 `thread_id`。暂停与恢复必须使用同一 `thread_id`，并复用同一个配置：

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "notification:tenant-7:req-42"}}
```

`InMemorySaver` 只适合演示或单进程测试，进程退出后不会保留 checkpoint。生产环境使用与部署匹配的持久化 checkpointer，并为 thread、checkpoint 和业务记录设计保留期。

`thread_id` 是恢复同一执行线程的地址，不是授权凭据，也不天然等于业务幂等键。API 层仍要验证当前用户能否恢复该 thread。

## 5. 一个连贯的 HITL 模式

### 状态先区分提案、决定和执行

```python
from typing import Literal, TypedDict

class Action(TypedDict):
    kind: Literal["send_notification"]
    tenant_id: str
    business_action_id: str
    recipient_id: str
    body: str

class AgentState(TypedDict, total=False):
    proposed: Action
    approved: Action
    decision: Literal["pending", "approved", "rejected"]
    executed: bool | None
    execution_status: Literal["not_started", "success", "failed", "cancelled", "unknown"]
    tool_result: dict
    validation_error: str
```

`approved` 表示允许按冻结参数执行。`executed=True` 表示副作用已经发生，`False` 表示确定未发生，`None` 表示外部结果仍不确定。批准、执行和结果确认不能共用一个布尔值；拒绝、取消、确定失败和未知也要分开记录。

### 在审批边界真正暂停

```python
from langgraph.types import interrupt

def approval_node(state: AgentState) -> dict:
    review = interrupt(
        {
            "kind": "action_review",
            "proposed": state["proposed"],
            "choices": ["approve", "edit", "reject"],
        }
    )

    if not isinstance(review, dict):
        return {
            "decision": "pending",
            "executed": False,
            "execution_status": "not_started",
            "validation_error": "review payload must be an object",
        }

    decision = review.get("decision")
    if decision == "reject":
        return {
            "decision": "rejected",
            "executed": False,
            "execution_status": "cancelled",
        }

    if decision not in {"approve", "edit"}:
        return {
            "decision": "pending",
            "executed": False,
            "execution_status": "not_started",
            "validation_error": "decision must be approve, edit, or reject",
        }

    candidate = state["proposed"] if decision == "approve" else review.get("action")
    if not isinstance(candidate, dict):
        return {
            "decision": "pending",
            "executed": False,
            "execution_status": "not_started",
            "validation_error": "edit requires an action object",
        }

    validation = validate_action(candidate, allowlist=ACTION_ALLOWLIST, schema=Action)
    if not validation.ok:
        return {
            "decision": "pending",
            "executed": False,
            "execution_status": "not_started",
            "validation_error": validation.error,
        }
    return {"approved": validation.value, "decision": "approved", "executed": False}
```

`interrupt()` 的 payload 必须可 JSON 序列化。恢复时，包含 interrupt 的节点会从头重新执行；interrupt() 前的副作用必须移走、变成幂等操作，或被事务边界包住。不要先创建审批记录、发消息，再指望代码从 interrupt 下一行继续。

空值、`cancel`、拼写错误或未知 decision 都回到 pending，并带验证错误；只有显式的 `approve` 或 `edit` 能进入批准分支。编辑后的动作也不可信，要先经过 allowlist 和 schema 校验，再进入执行节点。校验必须发生在副作用之前。图用 conditional edge 把带 `validation_error` 的 pending 状态路由回审批节点，让下一次 node invocation 再调用一次 `interrupt()`。

### 使用同一 thread 恢复

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "notification:tenant-7:req-42"}}

async def run_approval_roundtrip(graph, action):
    # 首次调用运行到 interrupt() 并保存 checkpoint
    paused = await graph.ainvoke({"proposed": action}, config=config)

    # 同一个 config；resume 值会成为 interrupt() 的返回值
    resumed = await graph.ainvoke(
        Command(resume={"decision": "approve", "action": action}),
        config=config,
    )
    return paused, resumed
```

如果恢复请求换了 `thread_id`，它不会继续原 checkpoint。Web 接口收到 approval id 后，应先查出对应 thread identity，再调用 `Command(resume=...)`；不能只更新一张 approval 表然后假设图会自动醒来。

### 执行前再校验，执行后再报成功

```python
import hashlib
import json

def action_idempotency_key(action: Action) -> str:
    normalized = json.dumps(
        {"recipient_id": action["recipient_id"], "body": action["body"]},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    stable_business_identity = f"{action['tenant_id']}:{action['business_action_id']}"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"send_notification:{stable_business_identity}:{digest}"

async def execute_node(state: AgentState) -> dict:
    if state.get("decision") != "approved":
        return {"executed": False, "execution_status": "cancelled"}

    validation = validate_action(state["approved"], allowlist=ACTION_ALLOWLIST, schema=Action)
    if not validation.ok:
        return {
            "executed": False,
            "execution_status": "failed",
            "validation_error": validation.error,
        }
    action = validation.value
    key = action_idempotency_key(action)
    try:
        result = await notification_tool.send(action, idempotency_key=key)
    except (TimeoutError, ConnectionError):
        result = None

    outcome = classify_tool_outcome(result, action)
    if outcome == "unknown":
        result = await notification_tool.lookup(
            idempotency_key=key,
            business_action_id=action["business_action_id"],
        )
        outcome = classify_tool_outcome(result, action)

    if outcome == "success":
        return {"executed": True, "execution_status": "success", "tool_result": result}
    if outcome == "failure":
        return {"executed": False, "execution_status": "failed", "tool_result": result}
    return {"executed": None, "execution_status": "unknown", "tool_result": result}
```

幂等键要由稳定业务标识和规范化动作参数生成。这里的 `business_action_id` 代表业务上同一次“发送”意图，用来区分业务上独立但参数相同的动作；业务 ID 不是随机调用 ID，也不应在每次重试时重建。`task_id:tool_name` 不足：同一 task 内两个不同动作会冲突，重放同一业务动作也可能换 task。

工具结果有 `success`、`failure`、`unknown` 三种。超时或响应丢失时，先用幂等键和业务对象查询；仍无法确认就保留 `executed=None` 和 `unknown`。只有查到确定性失败证据才能写 `failed`，只有验证了成功结果才能写 `success`。

生产实现还需要数据库唯一约束和结果查询，不能只靠进程内字符串。

## 6. 图结构

```text
START
  → propose_action
  → approval_node  -- interrupt / resume --> approved | rejected
      ├── invalid → pending + validation_error → approval_node
      ├── rejected → END
      └── approved → execute_node
                       → verified success | verified failure | unknown
                       → END
```

审批节点只保存决定，不执行工具；执行节点不接受 pending 或 rejected 状态。这样恢复、重试和审计都有明确位置。

## 7. RAG 和 Tool Calling 的映射

RAG State 保存 `doc_id`、`chunk_id`、score、source 和 permission，而不是无限增长的原文。答案生成后，引用校验节点检查关键断言是否有证据。

Tool wrapper 应覆盖 schema、授权、超时、错误分类、幂等和结果验证。LangGraph 负责流转，不替代这些后端控制。

## 8. 常见错误

- 编译图时没有 checkpointer，却声称能跨请求恢复。
- 暂停和恢复使用不同的 thread identity。
- “审批节点”只返回 pending，没有调用 `interrupt()`，图其实没有暂停。
- interrupt 前执行不可重复的写操作，恢复时再次执行。
- 审批人编辑参数后不重新校验。
- 一批准就把任务标成 success，没有等工具的可验证结果。

## 9. 面试自检

1. Checkpointer、Store 和业务数据库分别保存什么？
2. 为什么恢复时节点会重新执行，而不是从 Python 行号继续？
3. approval、execution 与 verified success 为什么要拆开？
4. 动作级幂等键应包含哪些稳定字段？
5. 服务重启后，InMemorySaver 为什么不够？
