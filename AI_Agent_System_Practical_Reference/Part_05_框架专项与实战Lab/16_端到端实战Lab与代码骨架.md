# 16_端到端实战Lab与代码骨架

## 0. 章节元信息

- 岗位重要性：P0/P1
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读并动手实现

适合岗位：

- AI Agent 应用工程师
- Python AI 后端工程师
- LangGraph Agent 工程师
- RAG 工程师

对应岗位能力：

- 端到端项目
- 代码骨架
- FastAPI
- LangGraph
- RAG
- 工具调用
- 评测
- 安全
- 部署

依赖章节：

- 01 到 15

相关章节：

- 11 项目设计模板
- 12 高频面试题


## 1. Lab 目标

本 Lab 设计一个可写进简历和用于面试讲解的端到端项目：

```text
企业知识库 + 工具调用 + 人工审批的 LangGraph Agent
```

项目目标：

```text
用户提出问题或任务；
系统判断是否需要检索知识库；
必要时调用业务工具；
高风险动作进入人工审批；
最终返回带引用的答案或执行结果；
全链路记录 trace、评测和审计。
```

这不是完整源码，而是项目骨架和实现指南。后续你可以基于这个文件逐步实现真实项目。

## 2. 项目功能范围

### 2.1 用户场景

```text
场景 1：员工询问内部制度
  Agent 检索知识库并给出带引用答案。

场景 2：员工询问某个订单或工单状态
  Agent 先判断权限，再调用只读业务 API。

场景 3：员工要求发送通知或创建工单
  Agent 生成计划和参数，进入人工确认后执行。

场景 4：答案低置信度
  Agent 补充检索或转人工。
```

### 2.2 系统能力

```text
RAG 问答；
工具调用；
LangGraph Workflow；
State 管理；
HITL；
FastAPI 服务；
SSE 流式事件；
Redis 缓存；
PostgreSQL 任务和审计；
向量库；
评测脚本；
Bad Case 回流。
```

## 3. 总体架构

```text
Client
  ↓
FastAPI
  ├── /agent/tasks
  ├── /agent/tasks/{task_id}
  ├── /agent/tasks/{task_id}/approve
  └── /feedback
  ↓
Agent Service
  ↓
LangGraph
  ├── understand_node
  ├── router_node
  ├── query_rewrite_node
  ├── retrieve_node
  ├── rerank_node
  ├── context_builder_node
  ├── tool_select_node
  ├── tool_execute_node
  ├── human_review_node
  ├── answer_node
  └── validator_node
  ↓
Storage
  ├── PostgreSQL：任务、审计、反馈、评测
  ├── Redis：缓存、锁、进度
  ├── Vector DB：知识 chunk
  └── Object Storage：原始文档
  ↓
Observability
  ├── logs
  ├── metrics
  └── traces
```

## 4. 推荐目录结构

```text
agent_job_project/
  app/
    main.py
    config.py

    api/
      routes_agent.py
      routes_approval.py
      routes_feedback.py

    schemas/
      request.py
      response.py
      state.py
      tools.py

    agents/
      graph.py
      nodes.py
      routing.py
      prompts.py

    tools/
      base.py
      rag.py
      business_api.py
      notification.py

    rag/
      loaders.py
      chunking.py
      embeddings.py
      retriever.py
      reranker.py
      indexing.py

    services/
      llm_gateway.py
      task_service.py
      approval_service.py
      audit_service.py
      eval_service.py

    storage/
      postgres.py
      redis.py
      vector_store.py

    observability/
      logging.py
      tracing.py
      metrics.py

    security/
      auth.py
      permissions.py
      guardrails.py

  evals/
    datasets/
      rag_eval.jsonl
      tool_eval.jsonl
      safety_eval.jsonl
    run_eval.py

  scripts/
    ingest_docs.py
    rebuild_index.py

  docker-compose.yml
  README.md
```

## 5. State 设计

```python
from typing import TypedDict, Literal, List, Dict, Optional

class AgentState(TypedDict, total=False):
    task_id: str
    trace_id: str
    user_id: str
    user_goal: str
    task_type: Literal["qa", "tool", "approval", "unknown"]
    risk_level: Literal["low", "medium", "high"]
    step_count: int
    retry_count: int

    rewritten_query: Optional[str]
    retrieved_docs: List[Dict]
    reranked_docs: List[Dict]
    context: str

    selected_tool: Optional[str]
    tool_args: Dict
    tool_result: Dict

    approval_required: bool
    approval_status: Literal["pending", "approved", "rejected", "not_required"]

    errors: List[Dict]
    final_answer: Optional[str]
    status: Literal["running", "waiting_approval", "success", "failed", "fallback"]
```

设计说明：

```text
task_id / trace_id 用于全链路追踪；
step_count / retry_count 用于循环控制；
retrieved_docs 保存文档引用，不保存过长全文；
approval_status 控制 HITL；
status 表示任务总体状态。
```

## 6. LangGraph 节点设计

### 6.1 understand_node

```python
def understand_node(state: AgentState) -> AgentState:
    # 识别任务类型、风险等级、是否需要检索或工具
    # 输出 task_type, risk_level
    return {
        "task_type": "qa",
        "risk_level": "low",
        "step_count": state.get("step_count", 0) + 1,
    }
```

### 6.2 route_after_understanding

```python
def route_after_understanding(state: AgentState) -> str:
    if state["risk_level"] == "high":
        return "human_review"
    if state["task_type"] == "qa":
        return "query_rewrite"
    if state["task_type"] == "tool":
        return "tool_select"
    return "answer"
```

### 6.3 RAG 节点

```python
async def query_rewrite_node(state: AgentState) -> AgentState:
    # 调用 LLM 改写 query
    return {"rewritten_query": state["user_goal"]}

async def retrieve_node(state: AgentState) -> AgentState:
    # 向量 + BM25 检索
    docs = await retriever.search(state["rewritten_query"], user_id=state["user_id"])
    return {"retrieved_docs": docs}

async def rerank_node(state: AgentState) -> AgentState:
    docs = await reranker.rerank(state["rewritten_query"], state["retrieved_docs"])
    return {"reranked_docs": docs[:5]}

def context_builder_node(state: AgentState) -> AgentState:
    context = build_context(state["reranked_docs"])
    return {"context": context}
```

### 6.4 工具节点

```python
async def tool_execute_node(state: AgentState) -> AgentState:
    tool_name = state["selected_tool"]
    args = state["tool_args"]

    result = await tool_registry.execute(
        tool_name=tool_name,
        args=args,
        user_id=state["user_id"],
        trace_id=state["trace_id"],
        idempotency_key=f"{state['task_id']}:{tool_name}"
    )

    return {"tool_result": result}
```

工具 wrapper 必须包含：

```text
schema 校验；
权限校验；
风险判断；
幂等；
超时；
重试；
错误码；
审计日志。
```

### 6.5 Human Review 节点

```python
def human_review_node(state: AgentState) -> AgentState:
    # 写入审批表，暂停执行
    create_approval_request(
        task_id=state["task_id"],
        tool_name=state.get("selected_tool"),
        args=state.get("tool_args"),
        risk_level=state["risk_level"],
    )
    return {
        "approval_required": True,
        "approval_status": "pending",
        "status": "waiting_approval",
    }
```

### 6.6 Answer 节点

```python
async def answer_node(state: AgentState) -> AgentState:
    # 基于 context、tool_result、user_goal 生成最终答案
    answer = await llm.generate_answer(
        user_goal=state["user_goal"],
        context=state.get("context", ""),
        tool_result=state.get("tool_result", {}),
    )
    return {"final_answer": answer, "status": "success"}
```

## 7. Graph 结构

```text
START
  ↓
understand_node
  ↓
route_after_understanding
  ├── query_rewrite_node
  │     ↓
  │   retrieve_node
  │     ↓
  │   rerank_node
  │     ↓
  │   context_builder_node
  │     ↓
  │   answer_node
  │
  ├── tool_select_node
  │     ↓
  │   risk_check_node
  │     ├── human_review_node
  │     └── tool_execute_node
  │           ↓
  │         answer_node
  │
  └── answer_node
        ↓
      validator_node
        ├── pass → END
        ├── retry → query_rewrite_node
        └── fail → fallback_node
```

## 8. FastAPI 接口设计

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AgentRequest(BaseModel):
    user_id: str
    query: str

@router.post("/agent/tasks")
async def create_agent_task(req: AgentRequest):
    task_id = await task_service.create_task(req.user_id, req.query)
    # 可同步调用，也可投递后台任务
    return {"task_id": task_id}

@router.get("/agent/tasks/{task_id}")
async def get_task(task_id: str):
    return await task_service.get_task(task_id)

@router.post("/agent/tasks/{task_id}/approve")
async def approve_task(task_id: str, approved: bool):
    return await approval_service.approve(task_id, approved)
```

SSE 事件可以设计为：

```text
node_start
node_end
token
tool_start
tool_end
human_required
final
error
```

## 9. 数据库表设计

### 9.1 tasks

```text
task_id
user_id
status
task_type
risk_level
created_at
updated_at
final_answer
trace_id
```

### 9.2 tool_calls

```text
id
task_id
tool_name
arguments_summary
status
retry_count
latency_ms
error_type
created_at
```

### 9.3 approvals

```text
approval_id
task_id
tool_name
risk_level
arguments_snapshot
status
approver_id
approved_at
```

### 9.4 audit_logs

```text
audit_id
task_id
user_id
action
resource_id
result
trace_id
created_at
```

### 9.5 feedback

```text
feedback_id
task_id
rating
comment
failure_type
created_at
```

## 10. 评测脚本思路

```python
def run_rag_eval(dataset):
    for case in dataset:
        result = agent.invoke({"user_goal": case["query"]})
        check_answer(result["final_answer"], case["expected_answer"])
        check_citations(result["retrieved_docs"], case["gold_doc_ids"])

def run_tool_eval(dataset):
    for case in dataset:
        result = agent.invoke({"user_goal": case["task"]})
        assert result["selected_tool"] == case["expected_tool"]
        assert validate_args(result["tool_args"], case["expected_args"])
```

评测维度：

```text
RAG：
  gold doc 是否召回，引用是否支持答案。

Tool：
  工具选择是否正确，参数是否正确，是否遵守权限。

Workflow：
  是否完成任务，步骤数是否超限，是否错误转人工。

Safety：
  是否阻止越权和高风险动作。
```

## 11. 部署与运行

```text
本地开发：
  FastAPI + PostgreSQL + Redis + Vector DB

索引任务：
  scripts/ingest_docs.py
  scripts/rebuild_index.py

服务运行：
  uvicorn app.main:app --reload

后台任务：
  celery -A app.worker worker

生产部署：
  Docker Compose / Kubernetes
  环境变量管理模型 key 和数据库连接
  日志、指标、trace 接入观测系统
```

## 12. 降级策略

```text
模型不可用：
  切备用模型或返回任务延迟提示。

向量库不可用：
  降级 BM25 或返回无法检索说明。

Rerank 不可用：
  使用初召回排序。

工具不可用：
  返回工具暂不可用，并给人工处理建议。

高风险审批超时：
  不执行动作，保持 pending 或自动取消。

低置信度答案：
  明确说明不确定性，展示引用，建议转人工。
```

## 13. 简历表达模板

```text
项目：企业知识库与工具调用 Agent

基于 FastAPI + LangGraph 设计并实现多步骤 Agent Workflow，支持知识库 RAG、工具调用、人工审批和任务状态追踪。离线侧完成文档解析、切块、Embedding 和向量索引；在线侧通过 Query Rewrite、Hybrid Search、Rerank 和引用校验提升答案准确性。工具调用层引入 schema 校验、权限检查、幂等、重试和审计，高风险动作通过 HITL 审批。系统采集节点级 Trace、工具耗时、召回结果和用户反馈，支持 Bad Case 回流和离线评测。
```

## 14. 面试讲解顺序

```text
1. 业务目标：解决什么问题。
2. 架构：FastAPI + LangGraph + RAG + Tool + Storage。
3. 核心难点：RAG 质量、工具安全、状态恢复。
4. 方案：分层设计、状态机、评测、HITL。
5. 指标：召回、答案、工具、成功率、延迟、成本。
6. 风险：越权、误调用、循环、幻觉。
7. 迭代：Bad Case 回流。
```

## 15. 本章 TODO Checklist

- [ ] 能按该骨架创建项目目录。
- [ ] 能定义 AgentState。
- [ ] 能实现至少 5 个 LangGraph 节点。
- [ ] 能实现一个 RAG 检索工具。
- [ ] 能实现一个只读业务工具。
- [ ] 能实现 HITL 审批表。
- [ ] 能实现节点级日志。
- [ ] 能写一个 RAG eval 脚本。
- [ ] 能把项目写进简历并口述 5 分钟。
