# 15_Agent框架选型_LangGraph_LangChain_AutoGen等

## 0. 章节元信息

- 岗位重要性：P1
- 面试常见度：中/高
- 工程实战价值：高
- 推荐学习深度：掌握选型逻辑，了解框架差异

适合岗位：

- AI Agent 应用工程师
- LangGraph Agent 工程师
- Python AI 后端工程师
- LLMOps 工程师

对应岗位能力：

- 框架选型
- LangChain
- LangGraph
- AutoGen
- CrewAI
- LlamaIndex
- 自研编排
- 面试选型表达

依赖章节：

- 02 Workflow
- 14 LangGraph 工程实战

相关章节：

- 16 端到端实战 Lab


## 1. 本章学习目标

JD 中常见 LangChain、LangGraph、AutoGen、CrewAI、LlamaIndex 等框架关键词。面试时，重要的不是把所有框架 API 都背下来，而是能解释：

```text
为什么需要 Agent 框架；
每个框架更适合什么问题；
为什么你的项目选择 LangGraph；
什么时候不用框架或自研轻量编排；
框架能力和通用工程能力如何结合。
```

## 2. 选型原则

### 2.1 先看任务形态

```text
简单单轮任务：
  直接模型调用或轻量 Chain。

RAG 知识库：
  LlamaIndex / LangChain 组件 + 自定义检索链路。

有状态多步骤 Agent：
  LangGraph。

多 Agent 角色协作原型：
  AutoGen / CrewAI / LangGraph Supervisor。

需要生产治理：
  LangGraph + 后端工程化 + 评测监控。

强业务系统集成：
  自研 Orchestrator + 框架组件。
```

### 2.2 选型维度

```text
任务复杂度；
是否有状态；
是否需要循环；
是否需要人工审批；
是否需要 checkpoint；
是否需要多 Agent；
是否需要 RAG 数据接入；
是否需要生产监控；
团队熟悉度；
生态稳定性；
可维护性；
供应商锁定风险。
```

## 3. 框架定位

### 3.1 LangChain

LangChain 更像 LLM 应用组件库，常见能力包括：

```text
模型封装；
Prompt 模板；
Retriever；
Tool；
Output Parser；
Runnable / LCEL；
简单 Chain；
Agent 抽象。
```

适合：

```text
快速搭建 LLM 应用；
复用模型、工具、检索、解析组件；
构建简单链路；
作为 LangGraph 中节点能力的组件来源。
```

不适合单独承担：

```text
复杂有状态图编排；
长任务恢复；
复杂 HITL；
强生产治理。
```

面试表达：

```text
LangChain 更偏组件层，LangGraph 更偏编排层。我的项目可以用 LangChain 的 retriever、prompt、tool 等组件，但用 LangGraph 管理有状态流程。
```

### 3.2 LangGraph

LangGraph 更偏有状态 Agent Workflow 编排。

适合：

```text
多步骤 Agent；
循环和条件路由；
Planner-Executor；
多 Agent Supervisor；
RAG pipeline 图编排；
HITL；
Checkpoint；
节点级 trace；
生产可恢复任务。
```

不适合：

```text
非常简单的单次调用；
只需要固定三步 Chain 的小任务；
团队完全不需要状态和恢复能力的场景。
```

面试表达：

```text
我选择 LangGraph 的原因是它能把 Agent 执行过程显式建模成 State、Node 和 Edge，更适合做有状态、多步骤、可恢复、可插入人工审批的生产 Agent。
```

### 3.3 LlamaIndex

LlamaIndex 更偏数据接入、索引和 RAG。

适合：

```text
文档 loader；
索引构建；
多种检索器；
query engine；
知识库问答；
RAG 原型和数据层封装。
```

与 LangGraph 的关系：

```text
LlamaIndex 可以负责 RAG 数据和检索；
LangGraph 可以负责 Agent 工作流；
二者可以组合。
```

### 3.4 AutoGen

AutoGen 常用于多 Agent 对话和协作原型，强调 Agent 间消息交互、角色分工和对话式协作。

适合：

```text
多 Agent 研究原型；
角色对话；
协作式任务分解；
实验不同 Agent 交互模式。
```

注意：

```text
框架生态会变化，选型时要关注维护状态、社区活跃度和团队长期投入。不要只因为 JD 出现 AutoGen 就把它作为唯一主框架。
```

### 3.5 CrewAI

CrewAI 更偏角色化多 Agent 工作流，常见概念包括 crew、agent、task、process。

适合：

```text
快速搭建角色分工型多 Agent；
研究助手；
内容生成工作流；
原型验证。
```

注意：

```text
多 Agent 框架适合表达角色协作，但生产治理仍然需要后端权限、状态、评测和监控。
```

### 3.6 OpenAI Agents SDK / 云厂商 Agent 平台

这类方案通常适合：

```text
快速接入托管工具；
利用供应商模型和工具生态；
降低基础设施建设成本；
做原型或特定平台集成。
```

需要注意：

```text
供应商锁定；
工具权限；
数据合规；
可观测性；
自定义 Workflow 灵活度。
```

### 3.7 自研轻量编排

适合：

```text
流程简单；
团队需要完全控制；
框架过重；
合规要求特殊；
只需要少量节点和工具。
```

但自研要补齐：

```text
状态管理；
工具 schema；
错误处理；
日志 trace；
评测；
HITL；
安全审计。
```

## 4. 框架对比表

| 框架/方案 | 核心定位 | 优势 | 风险/限制 | 适合场景 |
|---|---|---|---|---|
| LangChain | LLM 应用组件库 | 生态丰富，组件多 | 复杂状态编排需额外设计 | 简单 LLM 应用、RAG 组件 |
| LangGraph | 有状态 Agent 编排 | 状态机、循环、checkpoint、HITL | 学习成本高于简单 Chain | 生产级 Agent Workflow |
| LlamaIndex | 数据索引与 RAG | 数据接入和检索强 | 不专注复杂 Agent 编排 | 知识库和 RAG |
| AutoGen | 多 Agent 对话 | 多角色协作原型 | 生态状态需关注 | 多 Agent 实验 |
| CrewAI | 角色化多 Agent | 上手快，角色清晰 | 生产治理仍需补齐 | 研究助手、内容协作 |
| 自研 | 完全控制 | 灵活、可定制 | 需要自建大量能力 | 简单流程或强合规场景 |

## 5. 推荐组合

### 5.1 当前学习主线

```text
主框架：
  LangGraph

RAG 组件：
  LlamaIndex / LangChain / 自定义 Retriever

服务层：
  FastAPI

存储：
  PostgreSQL + Redis + Vector DB

评测监控：
  自定义 eval runner + OpenTelemetry / LangSmith

安全：
  自研权限、HITL、审计、沙箱
```

### 5.2 为什么不主攻所有框架

```text
框架 API 会变化；
岗位真正考察的是 Agent 工程思想；
浅学多个框架不如深挖一个主框架；
LangGraph 能很好承载状态机、RAG、工具、HITL 和多 Agent；
其他框架了解定位和选型即可。
```

## 6. 面试选型表达

### Q：为什么用 LangGraph，而不是直接 LangChain？

**回答：**

LangChain 更偏组件库，适合模型、Prompt、Tool、Retriever、Parser 等能力复用；但我的项目需要多步骤、有状态、条件路由、工具调用、失败恢复和人工审批，所以用 LangGraph 做编排层。LangGraph 能把流程显式成 State、Node 和 Edge，更适合生产治理。

### Q：为什么不用 AutoGen / CrewAI？

**回答：**

AutoGen 和 CrewAI 适合多 Agent 角色协作和原型验证，但我的核心需求是可控的状态机、可恢复、HITL、RAG 和工具治理，所以优先 LangGraph。对于多 Agent 场景，也可以在 LangGraph 中实现 Supervisor-Worker 模式。

### Q：什么时候自研？

**回答：**

如果流程很简单、团队不希望引入框架，或者合规要求特殊，可以自研轻量编排。但自研必须补齐状态、日志、错误处理、权限、评测和安全。否则只是把框架复杂度转移到自己系统里。

## 7. 选型决策图

```text
任务是否简单固定？
  ├── 是 → 直接模型调用 / 简单 Chain
  └── 否
      ↓
是否以 RAG 数据接入为主？
  ├── 是 → LlamaIndex / LangChain + 自定义链路
  └── 否
      ↓
是否有状态、循环、分支、HITL？
  ├── 是 → LangGraph
  └── 否
      ↓
是否主要是多 Agent 角色协作原型？
  ├── 是 → CrewAI / AutoGen / LangGraph
  └── 否 → 自研轻量编排或 LangChain
```

## 8. 常见误区

### 8.1 用框架名代替能力

JD 写 LangGraph，不代表只考 API。真正考察的是状态机、工具调用、RAG、评测、安全和生产治理。

### 8.2 盲目追新框架

Agent 框架迭代快。长期竞争力来自通用工程能力，不是某个框架版本。

### 8.3 框架选型没有业务理由

面试中不要只说“因为流行”。要说任务需要状态、分支、恢复、HITL，所以选择 LangGraph。

## 9. 本章 TODO Checklist

- [ ] 能解释 LangChain 和 LangGraph 的区别。
- [ ] 能解释为什么当前主攻 LangGraph。
- [ ] 能说明 LlamaIndex 的 RAG 定位。
- [ ] 能说明 AutoGen / CrewAI 的多 Agent 定位。
- [ ] 能说出自研轻量编排的条件和成本。
- [ ] 能用选型维度回答框架选择题。
