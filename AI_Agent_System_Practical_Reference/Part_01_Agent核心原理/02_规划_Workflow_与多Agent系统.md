# 02_规划_Workflow_与多Agent系统

## 0. 章节元信息

- 岗位重要性：P0
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读

适合岗位：

- AI Agent 应用工程师
- LangGraph Agent 工程师
- Python AI 后端工程师
- LLMOps 工程师

对应岗位能力：

- Chain / Workflow / Agent 区分
- 状态机编排
- Planner-Executor
- 多 Agent 协作
- 循环控制与失败恢复
- LangGraph 工作流设计

依赖章节：

- 01 Agent 基础与系统架构

相关章节：

- 03 工具调用
- 05 上下文工程与记忆
- 09 评测监控
- 14 LangGraph 工程实战专项


## 1. 本章学习目标

本章解决一个核心问题：Agent 如何从“一次模型调用”升级为“可控的多步骤任务系统”。

你需要掌握三种不同层次：

```text
Chain：固定顺序执行；
Workflow：显式流程、分支、状态和终止条件；
Agent：模型动态决定下一步动作。
```

生产环境中，最常见的形态并不是完全自治 Agent，而是：

```text
确定性 Workflow
  +
局部模型决策
  +
工具调用
  +
状态持久化
  +
人工审批
  +
评测监控
```

## 2. 核心概念总览

### 2.1 Chain、Workflow、Agent 的区别

| 形态 | 核心特点 | 适合场景 | 风险 |
|---|---|---|---|
| Chain | 固定步骤，线性执行 | 摘要、分类、简单 RAG | 灵活性低 |
| Workflow | 显式状态机，有分支和治理 | 业务流程、审批、RAG pipeline、数据处理 | 设计成本高 |
| Agent | 动态决策下一步 | 开放式任务、研究、自动化操作 | 不稳定、难评测、成本高 |

文字图：

```text
Chain：
输入 → 步骤 A → 步骤 B → 步骤 C → 输出

Workflow：
输入 → 节点 A → 条件判断
          ├── 路径 B → 输出
          └── 路径 C → 人工审批 → 输出

Agent：
输入 → LLM 判断下一步 → 工具 / 检索 / 继续规划
       ↑                         ↓
       └──── Observation ←───────┘
```

### 2.2 为什么生产系统更偏 Workflow + Agent 混合

完全让模型自由规划和执行，很容易出现循环、越权、误调用工具、成本失控。Workflow 的价值是把系统边界写清楚：

```text
哪些路径允许走；
哪些动作需要审批；
失败后如何处理；
什么时候必须终止；
每个节点输入输出是什么；
如何记录 trace 和指标。
```

Agent 的价值则是在局部开放空间里做动态判断，例如选择检索 query、判断是否需要工具、生成中间计划、评估答案是否充分。

## 3. 关键知识点详解
### 3.1 Planner-Executor 模式

**是什么：** Planner-Executor 是把任务拆解和动作执行分开的 Agent 模式。Planner 负责计划，Executor 负责调用工具或完成子任务。

**为什么需要：** 复杂任务直接让模型一步完成容易遗漏步骤。拆解后可以并行、检查、回滚，也更容易给每一步设置权限和成功条件。

**核心机制：** Planner 生成结构化计划，包含子任务、依赖、工具、风险等级和完成条件；Executor 根据计划执行并返回 Observation。

**工程实现：** 在 LangGraph 中可以把 Planner 做成节点，Executor 做成工具节点或 Worker 子图。每次执行后由 Router 判断继续、重试、转人工或结束。

**常见坑：**

- Planner 生成过度抽象计划。
- 计划无法落地到具体工具。
- Executor 执行失败后状态没有回写。
- Planner 每轮重写计划导致目标漂移。

**优化方式：**

- 要求 Planner 输出 JSON 格式计划。
- 每个步骤绑定可用工具和完成条件。
- 执行后进行状态增量更新。
- 保留原始目标，避免多轮后偏离。

**面试表达：** Planner-Executor 的核心价值是把复杂任务拆成可控步骤。面试中可以强调它便于插入检查点、人工审批、重试和并行执行。
### 3.2 Reflection / Critic / Reviewer

**是什么：** Reflection 或 Critic 是在 Agent 执行过程中引入自检或外部审查节点，用来判断计划、工具结果或最终答案是否满足要求。

**为什么需要：** LLM 生成结果不一定可靠，尤其是长链路任务。引入 Critic 可以降低错误累积，并把质量检查前置到流程中。

**核心机制：** Critic 可以检查事实一致性、格式合规、引用是否支持答案、工具结果是否可信、是否需要补充检索。

**工程实现：** 工程上 Critic 可以是规则、模型、检索校验、测试脚本或人工审查。不要只依赖同一个模型自我评价，关键任务要结合程序化验证。

**常见坑：**

- Critic 只说泛泛评价，没有可执行反馈。
- 生成器和评审器使用同一 Prompt，偏差相同。
- 反复自我修正导致循环。
- 把 Critic 分数当成绝对真理。

**优化方式：**

- 让 Critic 输出明确的 pass/fail、问题类别和修正建议。
- 限制最大修正轮数。
- 重要场景引入外部证据或人评。
- 保存评审结果用于 Bad Case 分析。

**面试表达：** 我会把 Critic 看成 Agent 工作流里的质量门禁，而不是让模型无限反思。它必须有明确检查标准、终止条件和可追溯日志。
### 3.3 多 Agent 协作

**是什么：** 多 Agent 是把复杂任务拆给多个角色化 Agent 协作，例如 Planner、Researcher、Coder、Tool Agent、Critic、Supervisor。

**为什么需要：** 单 Agent 承担所有职责时，Prompt 会很复杂，角色边界不清。多 Agent 可以分工、并行、互审，提高复杂任务的可维护性。

**核心机制：** 常见模式包括 Supervisor-Worker、Debate、Planner-Executor-Critic、Researcher-Writer-Reviewer、多工具专家分工。

**工程实现：** 工程上要明确每个 Agent 的输入、输出、权限、可用工具和终止条件。多 Agent 不是越多越好，过多会带来通信成本和状态一致性问题。

**常见坑：**

- 角色划分不清。
- Agent 之间循环对话不收敛。
- 共享上下文污染。
- 多个 Agent 同时修改同一状态。
- 成本和延迟显著增加。

**优化方式：**

- 设定 Supervisor 统一调度。
- 使用结构化消息和共享状态。
- 限制最大轮次和最大 token。
- 关键状态单写多读。
- 保留全链路 trace。

**面试表达：** 多 Agent 的价值在复杂任务分工，但工程上必须控制通信、状态和终止条件。否则多 Agent 只是把一个不稳定系统变成多个不稳定系统。
### 3.4 循环控制与终止条件

**是什么：** 循环控制是限制 Agent 在规划、执行、观察之间无限迭代的机制；终止条件定义何时成功、失败、转人工或降级。

**为什么需要：** Agent 天然可能循环：检索不满意继续检索，工具失败继续重试，计划修正后又回到原点。没有终止条件就会成本失控。

**核心机制：** 终止条件可以包括：目标完成、达到最大步数、达到最大重试、工具连续失败、置信度不足、需要人工审批、时间超限。

**工程实现：** 在 LangGraph 中可以通过 conditional edge 控制路由，通过状态字段记录 step_count、retry_count、status、confidence 和 risk_level。

**常见坑：**

- 只设置最大步数，没有定义完成条件。
- 所有错误都重试。
- 写操作重试没有幂等。
- 低置信度仍然强行给答案。

**优化方式：**

- 区分成功终止、失败终止、人工接管和降级终止。
- 工具错误按类型处理。
- 为写操作设置 idempotency key。
- 对低置信度输出说明不确定性或转人工。

**面试表达：** Agent 上线必须先定义终止条件。面试中可以说：没有终止条件的 Agent 不是智能，而是不可控。


## 4. 文字版架构图

### 4.1 单 Agent Workflow

```text
用户目标
  ↓
任务理解节点
  ↓
Planner 节点
  ↓
条件判断：需要检索？
  ├── 是 → RAG 节点 → 证据写入 State
  └── 否 → 继续
  ↓
条件判断：需要工具？
  ├── 是 → Tool 节点 → Observation 写入 State
  └── 否 → 继续
  ↓
Validator 节点
  ├── 通过 → Final Answer
  ├── 不通过但可修正 → 回到 Planner
  ├── 风险过高 → Human Review
  └── 超限 → 降级输出
```

### 4.2 多 Agent Supervisor 模式

```text
用户目标
  ↓
Supervisor Agent
  ├── Planner Agent：拆解任务
  ├── Research Agent：检索和收集证据
  ├── Tool Agent：调用 API / 数据库 / 代码执行
  ├── Writer Agent：组织输出
  └── Critic Agent：审查事实、格式和风险
        ↓
Aggregator：合并结果
        ↓
Finalizer：生成最终交付
        ↓
审计 / 评测 / Bad Case 回流
```

## 5. 工程实战设计

### 5.1 设计 Workflow 的步骤

```text
1. 明确业务目标和成功条件；
2. 列出必须经过的步骤；
3. 区分确定性步骤和模型决策步骤；
4. 为每个节点定义输入、输出、错误类型；
5. 为每条边定义路由条件；
6. 设置最大步数、重试、超时；
7. 为高风险节点加入 HITL；
8. 加入 trace、metrics、logs；
9. 建立回归评测集。
```

### 5.2 适合用 Workflow 的场景

```text
企业知识库问答；
客服工单处理；
合同审查；
代码修复建议；
数据分析报告；
邮件草稿生成；
审批流自动化；
RAG 多阶段检索；
高风险动作前置确认。
```

## 6. 与 LangGraph / Python 后端的映射

```text
Workflow 概念             LangGraph 映射
------------------------------------------------
节点                       Node
流程边                     Edge
条件路由                   Conditional Edge
开始 / 结束                START / END
共享状态                   State
多角色 Agent               多节点 / Subgraph / Supervisor
任务恢复                   Checkpoint
人工确认                   Interrupt / Human Review Node
并行分支                   Parallel Branch / Map-Reduce 思路
```

Python 后端中，Workflow 通常由 API 层触发：

```text
FastAPI 接收请求
  ↓
创建 task_id
  ↓
写入任务表
  ↓
调用 LangGraph graph.invoke / graph.stream
  ↓
节点执行期间写日志和状态
  ↓
结果返回前端或异步通知
```

## 7. 常见误区

### 7.1 把 Workflow 写得过度复杂

不是所有任务都需要多 Agent。简单分类、摘要、格式化输出，用 Chain 就够。只有出现分支、循环、外部工具、人工审批、状态恢复时，才需要复杂 Workflow。

### 7.2 多 Agent 等于更智能

多 Agent 的本质是组织分工，不是自动提升模型能力。如果没有清晰角色、通信协议和状态治理，多 Agent 会放大不稳定性。

### 7.3 忽略状态一致性

多个节点或多个 Agent 修改同一状态时，要明确谁负责写、谁只读。否则最终结果可能来自过期状态或冲突状态。

## 8. 面试题与答题闭环
### Q：Chain、Workflow、Agent 有什么区别？

**考察点：** 概念边界、生产系统形态。

**推荐回答：** Chain 是固定线性步骤，Workflow 是显式状态机，有分支、循环、错误处理和人工审批；Agent 是模型动态决定下一步。生产系统常见的是 Workflow + Agent 混合：确定性流程由代码控制，开放式判断交给模型。

### Q：为什么很多 Agent 系统要用 LangGraph 这类状态机框架？

**考察点：** 状态管理、可控性、可恢复性、LangGraph。

**推荐回答：** 因为 Agent 任务通常有多步骤、分支、循环、工具调用、状态持久化和人工审批。状态机框架能把节点、边、条件路由、Checkpoint 和终止条件显式化，比一串自由模型调用更可控、更好调试和恢复。

### Q：多 Agent 系统最容易出什么问题？

**考察点：** 多 Agent 失败模式和治理。

**推荐回答：** 最常见问题是角色不清、通信不收敛、上下文污染、状态冲突、成本高和延迟高。解决方法是用 Supervisor 统一调度，定义结构化消息、共享状态、最大轮次、终止条件和节点级 trace。


## 9. 本章 TODO Checklist

- [ ] 能区分 Chain、Workflow、Agent。
- [ ] 能解释 Planner-Executor 模式。
- [ ] 能设计一个带 Validator 的 Agent 工作流。
- [ ] 能说出多 Agent 的优势和风险。
- [ ] 能定义 Agent 的成功、失败、转人工、降级终止条件。
- [ ] 能把 Workflow 概念映射到 LangGraph 的节点、边、条件边和 State。
- [ ] 能解释为什么生产系统通常不是完全自治 Agent。
