# 14_LangGraph工程实战专项

## 0. 章节元信息

- 岗位重要性：P0/P1
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读并配合代码练习

适合岗位：

- LangGraph Agent 工程师
- AI Agent 应用工程师
- Python AI 后端工程师

对应岗位能力：

- StateGraph
- Node
- Edge
- Conditional Edge
- Checkpoint
- HITL
- Tool Node
- Subgraph
- Streaming
- LangGraph + RAG

依赖章节：

- 01 Agent 基础
- 02 Workflow
- 03 工具调用
- 08 Python 后端

相关章节：

- 15 框架选型
- 16 端到端实战 Lab


## 1. 本章学习目标

本章把 LangGraph 作为主框架实践线来学习。目标不是背 API，而是掌握如何用 LangGraph 表达一个生产级 Agent Workflow。

你需要能够做到：

```text
用 State 表示任务状态；
用 Node 表示执行步骤；
用 Edge 表示流程；
用 Conditional Edge 表示动态路由；
用 Checkpoint 支持中断和恢复；
用 Tool Node 接入工具；
用 Human-in-the-loop 控制高风险动作；
用 Trace 观察每一步；
用 FastAPI 把 graph 变成服务。
```

## 2. LangGraph 的定位

LangGraph 适合构建：

```text
有状态 Agent；
多步骤 Workflow；
可循环执行的任务；
带条件分支的流程；
长任务；
需要 checkpoint 的任务；
需要人工审批的任务；
多 Agent 编排；
需要节点级观测和调试的系统。
```

不适合把所有简单 LLM 调用都复杂化。对于单轮摘要、简单分类、固定 Chain，普通函数或 LangChain Chain 就够。

## 3. 核心概念

### 3.1 State

State 是整个图在执行过程中共享的状态。它不是随意的 dict，而应该是明确 schema。

```text
State 中适合放：
- task_id
- user_goal
- plan
- current_step
- retrieved_docs
- tool_observations
- errors
- risk_level
- approval_status
- final_answer

State 中不适合直接放：
- 超长原始文档
- 完整工具返回大文本
- 无关历史对话
- 敏感凭证
```

### 3.2 Node

Node 是处理步骤，可以是普通函数、模型调用、工具调用、检索、校验、人工审批等。

```text
常见 Node：
- understand_task_node
- planner_node
- rewrite_query_node
- retriever_node
- rerank_node
- tool_node
- validator_node
- human_review_node
- final_answer_node
```

好的 Node 应该职责单一、输入输出明确、便于测试。

### 3.3 Edge 和 Conditional Edge

Edge 定义节点之间的流转。Conditional Edge 根据 State 决定下一步。

```text
普通 Edge：
  planner → tool_executor

Conditional Edge：
  validator → final_answer
           → retry
           → human_review
           → fail
```

条件路由是 LangGraph 生产化价值的重要来源。它让流程不是一串黑盒调用，而是可解释、可控制的状态机。

### 3.4 Checkpoint

Checkpoint 用于保存图执行过程中的状态，支持中断、恢复、人工审批和时间旅行式调试。

适合场景：

```text
长任务中断；
工具失败后恢复；
人工审批暂停；
线上问题回放；
多轮会话持久化；
任务执行审计。
```

### 3.5 Interrupt / HITL

Human-in-the-loop 可以让图在某个节点暂停，等待用户或审核人操作。

```text
高风险动作
  ↓
human_review_node
  ↓
展示工具名、参数、资源、影响
  ↓
审批通过 / 驳回 / 修改
  ↓
结果写回 State
  ↓
图继续执行或终止
```

## 4. LangGraph Agent 执行链路

```text
FastAPI 接收请求
  ↓
构造初始 State
  ↓
graph.stream / graph.invoke
  ↓
任务理解节点
  ↓
Planner 节点
  ↓
条件路由：是否需要 RAG？
  ├── 是 → RAG 子链路
  └── 否 → 继续
  ↓
条件路由：是否需要工具？
  ├── 是 → Tool Node
  └── 否 → Answer Node
  ↓
工具结果写入 State
  ↓
Validator 节点
  ├── 通过 → Final Answer
  ├── 可修正 → 回到 Planner
  ├── 高风险 → Human Review
  └── 超限 → 降级输出
  ↓
保存 Trace / Checkpoint / 日志
```

## 5. 典型模式

### 5.1 Router

```text
用户请求
  ↓
router_node 判断类型
  ├── 知识问答 → rag_flow
  ├── 工具任务 → tool_flow
  ├── 高风险操作 → approval_flow
  └── 普通回答 → answer_node
```

适合根据任务类型分流。

### 5.2 Planner-Executor

```text
planner_node
  ↓
executor_node
  ↓
observation_node
  ↓
route_after_execution
  ├── continue → planner_node
  ├── final → answer_node
  └── human → human_review_node
```

适合多步骤任务。

### 5.3 Evaluator-Optimizer

```text
generator_node
  ↓
evaluator_node
  ↓
条件判断
  ├── pass → final
  └── revise → generator_node
```

适合文案、报告、代码修正，但必须限制最大轮数。

### 5.4 Orchestrator-Worker

```text
orchestrator_node
  ↓
分配任务
  ├── worker_a
  ├── worker_b
  └── worker_c
  ↓
aggregate_node
  ↓
final_node
```

适合多 Agent 和并行任务。

## 6. LangGraph + RAG

```text
query_rewrite_node
  ↓
retriever_node
  ↓
rerank_node
  ↓
context_builder_node
  ↓
answer_node
  ↓
citation_validator_node
  ↓
条件判断
  ├── 引用充分 → final
  ├── 证据不足 → query_rewrite_node
  └── 低置信度 → human_review
```

关键设计：

```text
RAG 结果不要只作为字符串；
要把 doc_id、chunk_id、score、source、permission 写入 State；
答案生成后检查关键断言是否有引用支持。
```

## 7. LangGraph + Tool Calling

```text
planner_node
  ↓
tool_selection_node
  ↓
tool_call_node
  ↓
tool_wrapper
  ├── schema 校验
  ├── 权限校验
  ├── 幂等检查
  ├── 执行工具
  └── 标准化结果
  ↓
observation 写入 State
  ↓
next_step_router
```

工具节点不是简单调用函数，要包住生产可靠性：

```text
timeout
retry
circuit breaker
permission
audit
idempotency
result validation
```

## 8. LangGraph + FastAPI

```text
POST /agent/tasks
  ↓
创建 task_id
  ↓
写入任务表
  ↓
调用 graph.stream
  ↓
SSE 返回节点事件
  ├── node_start
  ├── token
  ├── tool_start
  ├── tool_end
  ├── human_required
  └── final
```

长任务可以改成：

```text
POST /agent/tasks → 返回 task_id
后台 worker 执行 graph
GET /agent/tasks/{task_id} 查询状态
GET /agent/tasks/{task_id}/events 获取事件流
```

## 9. State 设计注意事项

```text
不要把 State 当全局变量；
不要让所有节点读写所有字段；
不要把大文本直接放入 State；
不要把敏感凭证放入 State；
不要没有 step_count 和 retry_count；
不要没有 status 和 error 字段。
```

推荐字段：

```text
task_id
trace_id
user_id
user_goal
plan
current_node
step_count
retry_count
retrieved_refs
tool_observation_refs
approval_status
risk_level
errors
final_answer
```

## 10. 常见坑

### 10.1 图太复杂

很多初学者会把所有逻辑都画成图，导致节点过多。原则是：

```text
业务流程复杂才用图；
简单处理保持函数化；
节点要按职责拆，不按每一行代码拆。
```

### 10.2 路由条件不稳定

如果 conditional edge 依赖模型自由文本，很容易不稳定。应尽量让模型输出结构化状态，例如：

```text
{"next": "retrieve", "reason": "..."}
```

再由后端映射到合法节点。

### 10.3 缺少终止条件

所有循环都要有最大轮数、最大重试、超时和失败出口。

### 10.4 Checkpoint 只用于保存，不用于恢复设计

Checkpoint 真正价值是支持中断恢复、人工审批和问题回放。设计时要考虑从任意关键节点恢复是否安全。

## 11. 面试表达模板

### Q：你如何用 LangGraph 设计 Agent？

**回答：**

我会先把任务建模成 State，然后把流程拆成节点，例如任务理解、规划、检索、工具调用、校验、人工审批和最终回答。节点之间用 edge 串联，动态分支用 conditional edge 控制，例如是否需要检索、是否需要工具、是否需要人工审批。对于长任务和高风险动作，我会使用 checkpoint 和 interrupt 支持恢复和 HITL。工具调用不会直接交给模型执行，而是在 tool node 中做 schema、权限、幂等、重试和审计。

### Q：LangGraph 相比普通 Chain 的优势是什么？

**回答：**

普通 Chain 适合固定流程，LangGraph 适合有状态、多步骤、有分支、可循环、可恢复的 Agent Workflow。它把执行过程显式成图，便于插入工具、校验、人工审批和监控，也便于节点级 trace 和失败恢复。

## 12. 本章 TODO Checklist

- [ ] 能解释 State、Node、Edge、Conditional Edge。
- [ ] 能设计一个 Planner-Executor 图。
- [ ] 能设计一个 RAG 图。
- [ ] 能设计一个工具调用节点。
- [ ] 能说明 checkpoint 的作用。
- [ ] 能说明 HITL 如何在 LangGraph 中实现。
- [ ] 能把 LangGraph 接入 FastAPI。
- [ ] 能说出 LangGraph 常见坑和治理方法。
