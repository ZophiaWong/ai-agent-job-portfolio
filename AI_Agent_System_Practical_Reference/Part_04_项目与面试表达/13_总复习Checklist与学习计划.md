# 13_总复习Checklist与学习计划

## 0. 章节元信息

- 岗位重要性：P3
- 面试常见度：中
- 工程实战价值：中
- 推荐学习深度：复习阶段精读

适合岗位：

- 所有目标岗位

对应岗位能力：

- 复习计划
- 概念检查
- 架构检查
- 面试冲刺
- 学习优先级

依赖章节：

- 01 到 12 主体章节

相关章节：

- role_paths


## 1. 总体学习目标

这份 Checklist 用来在系统学习后做复盘。最终目标不是背术语，而是能完成三件事：

```text
1. 讲清概念：
   Agent、Workflow、RAG、Tool Calling、MCP、LangGraph、Context、Memory。

2. 设计系统：
   Python + LangGraph + RAG + Tool + Evaluation + Safety。

3. 面试表达：
   用业务目标、架构、指标、风险、优化闭环讲项目。
```

## 2. P0 必须掌握

### 2.1 Agent 基础

- [ ] 能定义 AI Agent。
- [ ] 能区分 Agent 与 Chatbot。
- [ ] 能解释 ReAct。
- [ ] 能画出 Agent 执行闭环。
- [ ] 能说明 Planner、Executor、Tool、State、Memory 的职责。
- [ ] 能说明 Agent 上线难点：稳定性、可控性、成本、安全、评测。

### 2.2 Workflow 与 LangGraph

- [ ] 能区分 Chain、Workflow、Agent。
- [ ] 能解释为什么生产系统常用 Workflow + Agent 混合。
- [ ] 能设计 Planner-Executor 流程。
- [ ] 能解释多 Agent 的优势和风险。
- [ ] 能说出循环控制和终止条件。
- [ ] 能把 State、Node、Edge、Conditional Edge、Checkpoint 讲清楚。

### 2.3 工具调用与 MCP

- [ ] 能解释 Function Calling 流程。
- [ ] 能设计工具 schema。
- [ ] 能区分只读工具、写工具、高风险工具。
- [ ] 能解释超时、重试、熔断、降级。
- [ ] 能解释幂等键。
- [ ] 能说明 MCP 和 Function Calling 的关系。
- [ ] 能说明普通 API 如何工具化 / MCP 化。

### 2.4 RAG

- [ ] 能画出离线索引链路。
- [ ] 能画出在线检索链路。
- [ ] 能解释 Chunking 策略和权衡。
- [ ] 能解释 Embedding 与向量检索。
- [ ] 能解释 Hybrid Search 和 Rerank。
- [ ] 能说出 RAG 评测指标。
- [ ] 能排查 RAG Bad Case。

### 2.5 Python 后端工程

- [ ] 能画出 Python Agent 服务架构。
- [ ] 能说明 FastAPI、LangGraph、Redis、PostgreSQL、Vector DB 分工。
- [ ] 能解释 asyncio 和任务队列边界。
- [ ] 能说明限流、熔断、降级、幂等。
- [ ] 能设计长任务和流式输出。
- [ ] 能说明状态持久化和审计日志。

### 2.6 评测监控

- [ ] 能区分 LLM 评测和 Agent 评测。
- [ ] 能设计离线评测集。
- [ ] 能定义任务成功率。
- [ ] 能说明 LLM-as-a-Judge 的优缺点。
- [ ] 能设计 Trace 字段。
- [ ] 能按 Workflow、Tool、RAG、Prompt、Model 排查问题。
- [ ] 能建立 Bad Case 回流。

## 3. P1 核心进阶

- [ ] 能设计长期记忆写入和读取策略。
- [ ] 能解释上下文工程和记忆污染。
- [ ] 能设计 Human-in-the-loop。
- [ ] 能解释 Prompt Injection 防御。
- [ ] 能做 Agent 框架选型。
- [ ] 能讲清 LangChain、LangGraph、AutoGen、CrewAI 的定位。
- [ ] 能设计企业知识库、客服、代码助手、数据分析 Agent。
- [ ] 能把项目表达成业务价值 + 架构 + 指标 + 风险。

## 4. P2 加分能力

- [ ] 能解释 SFT、RLHF、DPO、RLAIF。
- [ ] 能解释 LoRA 和 QLoRA。
- [ ] 能说明 Agent 轨迹数据格式。
- [ ] 能说明微调上线流程。
- [ ] 能设计模型网关和多模型路由。
- [ ] 能设计更复杂的多 Agent 协作和 Subgraph。

## 5. 必须会画的文字版架构

### 5.1 Agent 执行闭环

```text
用户目标
  ↓
任务理解
  ↓
规划
  ↓
工具选择
  ↓
工具执行
  ↓
Observation
  ↓
状态更新
  ↓
继续规划 / 结束 / 转人工
```

### 5.2 RAG 链路

```text
文档 → 解析 → 清洗 → 切块 → Embedding → 向量库 / 元数据索引
用户问题 → Query Rewrite → Hybrid Search → Rerank → Context → LLM → 引用答案
```

### 5.3 Python Agent 后端

```text
FastAPI
  ↓
Auth / Rate Limit
  ↓
LangGraph Orchestrator
  ↓
Tool Layer
  ↓
Redis / PostgreSQL / Vector DB
  ↓
Logs / Metrics / Traces
```

### 5.4 安全治理

```text
输入过滤 → 权限校验 → 工具白名单 → 参数校验 → 风险分级 → HITL → 沙箱 / 幂等执行 → 审计
```

## 6. 7 天学习计划

### Day 1：Agent 主干

```text
精读：
- 01 Agent 基础
- 02 Workflow 与多 Agent
- 03 工具调用

目标：
能讲清 Agent 如何从目标到行动。
```

### Day 2：RAG

```text
精读：
- 04 RAG

目标：
能画出离线和在线 RAG 链路，能排查召回问题。
```

### Day 3：上下文与优化策略

```text
精读：
- 05 上下文工程
- 06 Prompt/Context/RAG/微调协同

目标：
能判断问题该改 Prompt、RAG、工具、Workflow 还是微调。
```

### Day 4：Python 工程

```text
精读：
- 08 Python 后端工程
- 14 LangGraph 专项

目标：
能讲出 Python + LangGraph 的服务实现。
```

### Day 5：评测与安全

```text
精读：
- 09 评测监控
- 10 安全风控

目标：
能讲 Agent 如何上线、监控和控风险。
```

### Day 6：项目表达

```text
精读：
- 11 项目设计模板
- 16 端到端实战 Lab

目标：
准备 1 个主项目和 2 个备选项目。
```

### Day 7：面试冲刺

```text
精读：
- 12 高频面试题
- role_paths 中对应路径

目标：
完成 30 道题口述练习。
```

## 7. 面试前 30 分钟速记

```text
Agent：
  LLM + Workflow + Tool + State + Memory + Evaluation + Safety。

RAG：
  离线索引 + 在线召回 + Rerank + 上下文 + 引用 + 评测。

LangGraph：
  State + Node + Edge + Conditional Edge + Checkpoint + HITL。

工具调用：
  模型选工具，后端校验和执行。

安全：
  最小权限、工具白名单、HITL、幂等、沙箱、审计。

评测：
  不只看答案，看任务成功率、工具、RAG、成本、延迟和安全。

项目：
  业务目标 → 架构 → 数据流 → 工具流 → 状态流 → 指标 → 风险 → 优化。
```

## 8. 易混概念速查

| 概念 A | 概念 B | 区别 |
|---|---|---|
| Prompt Engineering | Context Engineering | 前者写指令，后者管信息流 |
| State | Memory | State 是当前任务状态，Memory 是长期可复用信息 |
| RAG | 微调 | RAG 管外部知识，微调管行为模式 |
| Function Calling | MCP | 前者表达调用意图，后者标准化工具暴露 |
| Chain | Workflow | 前者线性，后者有状态和分支 |
| Workflow | Agent | 前者预定义路径，后者动态决策 |
| 只读工具 | 写工具 | 只读重在准确，写工具重在权限和幂等 |

## 9. 最终自检

- [ ] 我能 3 分钟讲清 AI Agent 系统架构。
- [ ] 我能 5 分钟讲清 RAG 全流程和优化。
- [ ] 我能 5 分钟讲清 Python + LangGraph 项目架构。
- [ ] 我能 3 分钟讲清工具调用安全治理。
- [ ] 我能 3 分钟讲清评测监控与 Bad Case 回流。
- [ ] 我能用一个项目回答系统设计题。
- [ ] 我能解释为什么我的项目不是 demo，而是可上线系统。
