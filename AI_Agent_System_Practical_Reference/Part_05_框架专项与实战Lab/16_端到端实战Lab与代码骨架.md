# 16 端到端实战 Lab 与代码骨架

## 0. 事实边界

- 主要能力：C08.02
- 关联能力：C03.03、C04.02、C05、C06、C07、C09
- 练习协议：[统一练习协议](../../interviews-docs/practice-protocol.md)

这是“企业知识库 + 工具调用 + 人工审批”的设计草图。仓库没有与本章对应的可运行源码或集成测试，因此不能把代码片段称为已实现项目，也不能直接写进简历。片段用于检查模块边界，省略了依赖注入、数据库事务和框架版本适配。

## 1. 冷启动交付

先不看参考骨架，用 45 分钟写 `agent-lab-cold-design.md`：

1. 画出 RAG 问答、只读工具和高风险写工具三条链路。
2. 定义 State，明确 proposed、approved/rejected、executed 和最终结果。
3. 写出 pause/resume 的调用协议、稳定 thread identity 和动作级幂等键。
4. 列出至少六个失败场景，逐一标注 retry、reject、cancel、fail 或人工处理。
5. 给出你会怎样用集成测试证明“暂停时未执行，恢复后至多执行一次”。

阅读参考代码、补齐 TODO 或勾选清单不算独立证据。要升级为项目证据，至少需要可运行源码、测试输出、一次受控 trace 和实际贡献说明。

### 迁移题

改变约束：审批人允许修改动作参数，服务可能在 `interrupt()` 后重启，并且工具调用成功后响应可能丢失。更新设计，说明重新校验、持久化 checkpointer、幂等结果查询各放在哪里。

### 延迟复测

两天后重做核心状态图，保存 `agent-lab-delayed.md`。对照第一次产物，检查是否仍把“approved”误写成“executed”。

<!-- Lab 参考分隔线：完成冷答后再继续 -->

## 2. 目标和非目标

设计覆盖四类请求：

- 内部制度问答：先做权限过滤，再返回带引用的答案。
- 订单状态查询：鉴权后调用只读 API。
- 创建工单或发送通知：形成动作提案，暂停等待确认，恢复后执行。
- 证据不足或工具结果不确定：补充检索、失败退出或转人工。

它不是某个现有系统的说明书，也不暗示 MeterDesk、Forge Harness 或本仓库已经采用这些接口。

## 3. 架构边界

```text
Client
  → FastAPI：身份、请求/恢复接口、SSE
  → Agent Service：LangGraph + durable checkpointer
      ├── RAG：ingest / retrieve / rerank / cite
      ├── Tool Gateway：schema / authz / idempotency / outcome verification
      └── HITL：interrupt / resume / audit
  → Storage
      ├── PostgreSQL：业务任务、动作、审批、幂等结果、审计
      ├── Vector Store：有权限标签的 chunk
      └── Object Storage：原始文档
  → Observability：logs / metrics / traces
```

Checkpointer 保存图的 checkpoint；业务数据库保存审批身份、冻结参数、幂等记录和工具结果。不要假设 checkpoint 取代业务事务。

## 4. 目录草图

```text
agent_lab/
  app/
    api/tasks.py
    agents/graph.py
    agents/nodes.py
    schemas/state.py
    services/approval.py
    services/tool_gateway.py
    rag/retriever.py
    security/authorization.py
    storage/checkpoints.py
    storage/postgres.py
  tests/
    test_hitl_resume.py
    test_tool_idempotency.py
    test_rag_permissions.py
  evals/
    rag_cases.jsonl
    action_cases.jsonl
```

这些文件目前不存在。真正实现后应以仓库路径和测试记录替代这段草图。

## 5. State：批准不是执行

```python
from typing import Literal, TypedDict

class Action(TypedDict):
    kind: Literal["create_ticket", "send_notification"]
    tenant_id: str
    business_object_id: str
    arguments: dict

class AgentState(TypedDict, total=False):
    thread_business_id: str
    user_id: str
    query: str

    retrieved_refs: list[dict]
    proposed: Action
    approved: Action
    decision: Literal["pending", "approved", "rejected"]
    executed: bool
    execution_status: Literal[
        "not_started", "success", "failed", "cancelled", "unknown"
    ]
    tool_result: dict
    final_answer: str
```

`proposed` 是模型或规则产生的候选动作。`approved` 是用户确认、可能编辑后又通过校验的参数快照。`executed` 只有在副作用发生且结果可验证时才为 true。审批不等于执行。

## 6. RAG 分支

```python
async def retrieve_node(state: AgentState) -> dict:
    refs = await retriever.search(
        query=state["query"],
        principal=state["user_id"],
    )
    return {"retrieved_refs": refs}

async def answer_node(state: AgentState) -> dict:
    answer = await llm.answer(state["query"], refs=state.get("retrieved_refs", []))
    verified = citation_validator.check(answer, state.get("retrieved_refs", []))
    if not verified.ok:
        return {"execution_status": "failed", "final_answer": verified.safe_message}
    return {"final_answer": answer}
```

检索时做数据权限过滤，生成后检查引用。`doc_id`、`chunk_id`、版本和 permission scope 要能进入 trace；单纯把长文本放进 prompt 不足以诊断坏案例。

## 7. HITL：真正暂停并恢复

### Checkpointer 和稳定 thread identity

```python
from langgraph.checkpoint.memory import InMemorySaver

# 仅供本地演示；生产要换成可持久化的 checkpointer。
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "tenant-7:action-request-42"}}
```

`InMemorySaver` 不能支持进程重启后的恢复。生产部署要选择持久化实现，并让暂停和恢复使用同一 `thread_id`。thread identity 用来找到 checkpoint，不代表当前调用者有审批权。

### 审批节点

```python
from langgraph.types import interrupt

def approval_node(state: AgentState) -> dict:
    review = interrupt(
        {
            "kind": "review_action",
            "proposed": state["proposed"],
            "choices": ["approve", "edit", "reject"],
        }
    )

    if review["decision"] == "reject":
        return {
            "decision": "rejected",
            "executed": False,
            "execution_status": "cancelled",
        }

    candidate = review.get("action", state["proposed"])
    approved = validate_action(candidate, allowlist=ACTION_ALLOWLIST, schema=Action)
    return {"approved": approved, "decision": "approved", "executed": False}
```

`interrupt()` 会保存 checkpoint 并暂停；恢复后节点从头重新执行。interrupt() 前不要放不可重复副作用；无法移走时必须让副作用幂等，并保存可查询的执行结果。payload 要能 JSON 序列化。

审批人编辑后的 action 重新走 allowlist 和 schema。校验在任何副作用之前完成，执行节点再防御性校验一次。

### 恢复接口的核心调用

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "tenant-7:action-request-42"}}

paused = graph.invoke({"proposed": action, "decision": "pending"}, config=config)

resumed = graph.invoke(
    Command(resume={"decision": "approve", "action": edited_action}),
    config=config,
)
```

实际 API 还要验证审批人、审批是否过期、approval id 与 thread 的绑定，并防止重复 resume。只在数据库里把状态改成 approved，不会让图自动继续。

## 8. 动作级幂等与结果验证

```python
import hashlib
import json

def action_key(action: Action) -> str:
    normalized_arguments = json.dumps(
        action["arguments"], sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    stable_business_identity = (
        f"{action['tenant_id']}:{action['kind']}:{action['business_object_id']}"
    )
    digest = hashlib.sha256(normalized_arguments.encode("utf-8")).hexdigest()
    return f"{stable_business_identity}:{digest}"

async def execute_action_node(state: AgentState) -> dict:
    if state.get("decision") != "approved":
        return {"executed": False, "execution_status": "cancelled"}

    action = validate_action(state["approved"], allowlist=ACTION_ALLOWLIST, schema=Action)
    result = await tool_gateway.execute(action, idempotency_key=action_key(action))
    if not tool_gateway.verify_outcome(action, result):
        return {
            "executed": False,
            "execution_status": "failed",
            "tool_result": result,
        }
    return {"executed": True, "execution_status": "success", "tool_result": result}
```

键由稳定业务标识和规范化动作参数生成，并由数据库唯一约束保护。`task_id:tool_name` 不足，会让同一任务里的不同动作碰撞；仅使用随机 request id 又无法识别业务重放。

只有工具结果经过验证才能记录 `success`。如果请求超时而服务端结果未知，应先查幂等记录或业务对象，不要直接重试，也不要写 success。拒绝、取消和失败各自保留终态。

## 9. 图结构

```text
START → classify
  ├── qa → retrieve → answer → citation_check → END
  ├── readonly_tool → authorize → execute_read → verify → answer → END
  └── write_tool → propose → approval_node
                              ├── rejected → END(cancelled)
                              └── approved → execute_action_node
                                                ├── verified → END(success)
                                                └── unknown/failed → END(failed)
```

没有一个“human_review_node 返回 pending 后继续往下走”的假暂停节点。图只会在 `interrupt()` 处停下，由 `Command(resume=...)` 恢复。

## 10. 接口契约

```text
POST /agent/tasks
  创建业务请求，生成稳定 thread 映射，首次 invoke。

GET /agent/tasks/{task_id}
  返回业务状态；不暴露 checkpoint 或敏感参数。

POST /agent/approvals/{approval_id}/resume
  鉴权、检查过期与重复提交，加载同一 thread_id，调用 Command(resume=...).

GET /agent/tasks/{task_id}/events
  返回经过权限和脱敏处理的状态事件。
```

审批接口接收的是 approval id，不允许调用者直接指定任意 thread。服务端从受控记录解析 thread identity。

## 11. 最小验收测试

真正实现时，至少保留这些可检查结果：

1. 首次调用命中 interrupt，写工具调用计数仍为 0。
2. 使用同一 thread_id 批准后，工具调用一次，结果验证通过才进入 success。
3. 重复 resume 或模拟超时重试，业务对象仍只创建一次。
4. 编辑参数超出 allowlist/schema 时，工具不执行。
5. reject、cancel、failed 和 success 的审计事件不同。
6. 换 thread_id 不能恢复原 checkpoint，越权用户也不能 resume。

只做单元测试 mock 仍不足以证明外部副作用安全。应再做带持久化 checkpointer、数据库唯一约束和假的确定性工具服务的集成测试。

## 12. 评测和可观测性

RAG 评测拆成检索、引用和回答；工具评测拆成选择、参数、授权、执行结果；Workflow 再看任务完成率、错误分支和人工升级。trace 至少关联 thread、checkpoint、action、approval 和 tool outcome，但日志不保存凭证或完整敏感正文。

## 13. 如何转成真实项目证据

完成源码和测试后，再按以下结构记录：

```text
需求和约束
→ 本人实现的路径与 commit
→ 测试命令及输出
→ 一次暂停/恢复 trace
→ 重复提交、拒绝和工具失败的结果
→ 尚未实现的部分
```

简历只能写已经有证据的内容。“设计了 HITL 状态机”和“上线了可恢复审批系统”是两种不同主张。
