# 08_Python后端视角的Agent工程实践

## 0. 章节元信息

- 岗位重要性：P0
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读

适合岗位：

- Python AI 后端工程师
- AI Agent 应用工程师
- RAG 工程师
- LLMOps 工程师

对应岗位能力：

- FastAPI
- asyncio
- 任务队列
- Redis
- PostgreSQL
- 向量库
- 并发工具调用
- 幂等
- 限流熔断降级
- 服务分层

依赖章节：

- 01 Agent 基础
- 03 工具调用
- 04 RAG

相关章节：

- 09 评测监控
- 10 安全风控
- 14 LangGraph
- 16 实战 Lab


## 1. 本章学习目标

本章把 Agent 概念落到 Python 后端工程。目标不是学习 Python 语法，而是理解如何把 Agent 做成一个可运行、可扩展、可监控、可恢复的服务。

你需要掌握：

```text
FastAPI 如何承接 Agent 请求；
LangGraph 如何作为 Orchestrator；
asyncio 如何并发执行检索和工具调用；
任务队列如何处理长任务；
Redis / PostgreSQL / Vector DB 各自负责什么；
如何做幂等、限流、重试、熔断、降级；
如何设计日志、Trace 和审计。
```

## 2. 核心概念总览

### 2.1 Agent 服务分层

```text
Client / Frontend
  ↓
API Gateway / FastAPI
  ↓
Auth / Rate Limit / Request Validation
  ↓
Agent Orchestrator / LangGraph
  ↓
Tool Layer
  ├── RAG Retriever
  ├── Business API Tool
  ├── Database Tool
  ├── Code Execution Tool
  └── Notification Tool
  ↓
Storage Layer
  ├── Redis
  ├── PostgreSQL
  ├── Vector DB
  └── Object Storage
  ↓
Observability
  ├── Logs
  ├── Metrics
  └── Traces
```

### 2.2 Python 技术栈定位

```text
FastAPI：
  API 服务层，处理请求、认证、参数校验、流式返回。

LangGraph：
  Agent Workflow 编排层，管理 State、节点、边、循环、checkpoint。

asyncio：
  并发 I/O，用于并行检索、多个工具调用、流式输出。

Celery / RQ / Dramatiq：
  长任务、异步索引、批处理、耗时 Agent 任务。

Redis：
  缓存、分布式锁、短期状态、限流、任务进度。

PostgreSQL：
  业务数据、任务记录、审计日志、评测结果、元数据。

pgvector / Milvus / FAISS：
  向量检索。

Elasticsearch / OpenSearch：
  关键词检索、日志检索、Hybrid Search 辅助。

Docker：
  服务部署和沙箱执行。

OpenTelemetry：
  Trace、Metrics、Logs 统一观测。
```

## 3. 关键知识点详解
### 3.1 FastAPI 服务层

**是什么：** FastAPI 是 Python Agent 应用常用的 API 服务框架，负责接收请求、校验参数、调用 Agent、返回同步或流式结果。

**为什么需要：** Agent 应用通常需要 HTTP API、SSE 流式输出、认证鉴权、请求限流和参数校验，FastAPI 与 Pydantic 适合承担这一层。

**核心机制：** API 层不应该写复杂 Agent 逻辑，而应该做请求解析、trace_id 创建、用户身份传递、任务创建和调用 Orchestrator。

**工程实现：** 工程实现中可按 router、service、agent、tool、storage、schema 分层。长任务可立即返回 task_id，由后台任务处理。

**常见坑：**

- 把 Agent 流程都写在 endpoint 里。
- 没有 request_id / trace_id。
- 同步阻塞处理长任务。
- 参数不校验。

**优化方式：**

- API 层保持薄。
- 使用 Pydantic schema。
- 对长任务使用任务队列。
- 所有请求生成 trace_id。

**面试表达：** FastAPI 在 Agent 系统中是服务入口，不是 Agent 大脑。真正的编排应放在 Orchestrator 或 LangGraph 中。
### 3.2 asyncio 与并发工具调用

**是什么：** asyncio 是 Python 的异步 I/O 并发机制，适合并行处理网络请求、检索、模型调用和工具调用。

**为什么需要：** Agent 一次任务可能同时调用多个检索源或 API。如果串行执行，延迟会很高。

**核心机制：** 可以用 asyncio.gather 并发执行多个只读工具，用 timeout 控制耗时，用 semaphore 控制并发度。

**工程实现：** 写操作不应随意并发，尤其涉及同一资源时要加锁、幂等或事务控制。

**常见坑：**

- 把 CPU 密集任务放进 asyncio。
- 无限并发打爆下游服务。
- 并发写导致状态冲突。
- 异常处理不完整导致任务挂起。

**优化方式：**

- 用 semaphore 限制并发。
- 设置超时。
- 区分只读并发和写操作串行。
- 对异常返回结构化错误。

**面试表达：** asyncio 的价值是提高 I/O 密集型 Agent 链路的吞吐和延迟表现，但必须配合限流和错误处理。
### 3.3 任务队列与长任务

**是什么：** 任务队列用于处理耗时、可异步、可重试的 Agent 任务，例如文档索引、复杂研究、批量评测和长链路工具执行。

**为什么需要：** Agent 任务可能持续几十秒甚至更久，直接占用 HTTP 连接不稳定，也不便于重试和恢复。

**核心机制：** 常见模式是 API 创建任务并返回 task_id，后台 worker 执行任务，前端通过轮询、WebSocket 或 SSE 获取进度。

**工程实现：** Python 中可选 Celery、RQ、Dramatiq 或自研 asyncio worker。任务状态写 PostgreSQL/Redis，结果写对象存储或数据库。

**常见坑：**

- 所有任务同步执行。
- 任务失败没有重试和状态记录。
- 重复提交导致重复执行。
- 任务结果只保存在内存中。

**优化方式：**

- 任务表记录状态。
- 幂等键防重复提交。
- 失败重试并记录错误类型。
- 长结果持久化。

**面试表达：** 长任务要任务化、状态化、可恢复，而不是让一个 HTTP 请求一直挂着。
### 3.4 Redis 与 PostgreSQL 的分工

**是什么：** Redis 适合短期、高速、可过期的数据；PostgreSQL 适合持久、结构化、可查询和事务性数据。

**为什么需要：** Agent 系统既有短期状态，也有任务记录、审计和评测数据。两类存储职责必须分清。

**核心机制：** Redis 可做缓存、分布式锁、限流计数器、任务进度；PostgreSQL 可做任务表、用户权限、工具调用记录、审计日志、评测结果。

**工程实现：** 如果使用 pgvector，PostgreSQL 也可以承担中小规模向量检索；大规模高并发可使用 Milvus 等专用向量库。

**常见坑：**

- 把重要状态只放 Redis。
- 把热点缓存全放 PostgreSQL。
- 没有 TTL 导致缓存污染。
- 没有事务导致状态不一致。

**优化方式：**

- 关键状态落库。
- 缓存设置 TTL。
- 写操作用事务。
- 幂等记录使用数据库唯一约束。

**面试表达：** Redis 用于快，PostgreSQL 用于稳。Agent 的关键任务状态和审计不能只依赖缓存。
### 3.5 限流、熔断、降级与幂等

**是什么：** 限流控制请求速率，熔断防止故障扩散，降级保证系统在部分不可用时仍可控，幂等避免重复副作用。

**为什么需要：** Agent 会调用模型、向量库和外部工具，下游服务昂贵且可能限流。没有治理会造成成本失控和级联失败。

**核心机制：** 限流可按用户、IP、模型、工具设置；熔断根据失败率和延迟触发；降级可切备用模型、减少 TopK、跳过 rerank 或转人工；幂等用于写操作。

**工程实现：** 工程上可以通过中间件、Redis 计数器、工具 wrapper、feature flag 和数据库幂等表实现。

**常见坑：**

- 只做模型限流，不做工具限流。
- 降级后结果没有标记。
- 写操作重试无幂等。
- 熔断后没有恢复策略。

**优化方式：**

- 按资源维度限流。
- 降级输出说明能力限制。
- 写工具强制 idempotency key。
- 熔断器有半开恢复机制。

**面试表达：** 生产级 Agent 要像后端系统一样设计限流、熔断、降级和幂等，不能只依赖模型行为。


## 4. 文字版架构图

```text
用户
  ↓
FastAPI
  ├── 参数校验
  ├── 认证鉴权
  ├── 限流
  └── 创建 trace_id / task_id
  ↓
Agent Service
  ↓
LangGraph Orchestrator
  ├── State 初始化
  ├── Node 执行
  ├── Conditional Edge 路由
  ├── Checkpoint
  └── Streaming
  ↓
Tool Layer
  ├── RAG Tool
  ├── External API Tool
  ├── SQL Tool
  ├── Code Tool
  └── Human Review Tool
  ↓
Storage
  ├── Redis：缓存、锁、进度
  ├── PostgreSQL：任务、审计、权限
  ├── Vector DB：知识检索
  └── Object Storage：原始文档、长结果
  ↓
Observability
  ├── Structured Logs
  ├── Metrics
  ├── Traces
  └── Alerts
```

## 5. 工程实战设计

### 5.1 目录结构建议

```text
app/
  api/
    routes_agent.py
    routes_feedback.py
  schemas/
    request.py
    response.py
    state.py
  agents/
    graph.py
    nodes.py
    routers.py
  tools/
    rag_tool.py
    api_tool.py
    sql_tool.py
    code_tool.py
  services/
    llm_gateway.py
    task_service.py
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
```

### 5.2 Agent 请求处理模式

```text
同步短任务：
  FastAPI → graph.invoke → 返回结果

流式任务：
  FastAPI → graph.stream → SSE 返回 token / events

异步长任务：
  FastAPI → 创建 task_id → 任务队列 → worker 执行 graph → 前端查询进度

高风险任务：
  FastAPI → graph 执行到审批节点 → 状态暂停 → 人工审批 → graph 继续
```

## 6. 与 LangGraph / Python 后端的映射

```text
后端需求                 推荐实现
------------------------------------------------
请求入口                 FastAPI
参数校验                 Pydantic
Agent 编排               LangGraph
模型调用                 LLM Gateway
并发检索                 asyncio.gather
长任务                   Celery / RQ / Dramatiq
短期状态                 Redis
持久状态                 PostgreSQL
向量检索                 pgvector / Milvus / FAISS
关键词检索               Elasticsearch / OpenSearch
流式输出                 SSE
日志                     structlog / logging
Trace                    OpenTelemetry / LangSmith
配置                     pydantic-settings
部署                     Docker / Kubernetes
```

## 7. 常见误区

### 7.1 把 Agent Demo 当生产服务

Demo 可以单进程、内存状态、无评测；生产服务必须考虑认证、限流、状态持久化、失败恢复和监控。

### 7.2 忽视任务状态

Agent 任务可能被中断、超时、人工审批或重试。没有持久化状态，就无法恢复和审计。

### 7.3 对所有工具一视同仁

只读工具、写工具、高风险工具的治理完全不同。后端必须按风险分级。

## 8. 面试题与答题闭环
### Q：Python 后端如何实现一个 Agent 服务？

**考察点：** 端到端服务架构。

**推荐回答：** 我会用 FastAPI 做 API 层，Pydantic 做参数校验，LangGraph 做 Agent Workflow 编排，工具层封装 RAG、API、SQL 等能力，Redis 处理缓存和短期状态，PostgreSQL 保存任务、审计和权限，向量库做检索，同时加入日志、指标、Trace、限流、重试、幂等和降级。

### Q：什么时候用 asyncio，什么时候用任务队列？

**考察点：** 异步并发和后台任务边界。

**推荐回答：** asyncio 适合单个请求内的 I/O 并发，比如并行检索多个数据源；任务队列适合跨请求的长任务、批处理、文档索引、复杂研究和可重试后台任务。二者可以结合：worker 内部也可以用 asyncio 并发执行只读工具。

### Q：Redis 和 PostgreSQL 在 Agent 系统中如何分工？

**考察点：** 存储分层。

**推荐回答：** Redis 适合缓存、限流、锁和短期任务进度；PostgreSQL 适合持久化任务状态、权限、审计日志、工具调用记录和评测结果。关键状态和审计不能只放 Redis。


## 9. 本章 TODO Checklist

- [ ] 能画出 Python Agent 后端架构。
- [ ] 能说明 FastAPI、LangGraph、Redis、PostgreSQL、Vector DB 的职责。
- [ ] 能解释 asyncio 和任务队列的使用边界。
- [ ] 能说明限流、熔断、降级、幂等在 Agent 中的作用。
- [ ] 能设计 Agent 服务目录结构。
- [ ] 能说明长任务、流式任务和高风险任务的处理方式。
