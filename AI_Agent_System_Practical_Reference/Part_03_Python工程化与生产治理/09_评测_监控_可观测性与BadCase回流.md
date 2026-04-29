# 09_评测_监控_可观测性与BadCase回流

## 0. 章节元信息

- 岗位重要性：P0/P1
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读

适合岗位：

- AI Agent 应用工程师
- LLMOps 工程师
- Python AI 后端工程师
- RAG 工程师

对应岗位能力：

- 离线评测
- 线上监控
- LLM-as-a-Judge
- RAG Evaluation
- Agent 任务成功率
- Trace
- Bad Case 回流
- 成本延迟监控

依赖章节：

- 04 RAG
- 08 Python 后端工程实践

相关章节：

- 10 安全风控
- 14 LangGraph
- 16 实战 Lab


## 1. 本章学习目标

Agent 项目能不能上线，不取决于 demo 看起来是否聪明，而取决于能否被评测、监控、定位和持续改进。

本章目标是建立完整的质量闭环：

```text
离线评测
  ↓
上线前回归
  ↓
线上监控
  ↓
Trace 定位
  ↓
Bad Case 分类
  ↓
改进 Prompt / RAG / Tool / Workflow / Model
  ↓
再次评测
```

## 2. 核心概念总览

### 2.1 LLM 评测 vs Agent 评测

```text
LLM 评测：
  关注单次输入输出质量，如准确性、格式、事实性、安全性。

Agent 评测：
  关注整个任务执行过程，如计划是否合理、工具是否正确、步骤是否收敛、最终任务是否成功、成本和时延是否可接受。
```

Agent 的评测粒度更细：

```text
最终答案
  +
中间步骤
  +
工具调用
  +
检索证据
  +
状态变化
  +
人工接管
  +
成本延迟
```

### 2.2 离线评测、在线监控、Bad Case 回流

```text
离线评测：
  上线前用固定测试集评估版本变化。

在线监控：
  上线后持续观察质量、成本、延迟、失败率。

Bad Case 回流：
  把线上失败案例分类、标注、修正，并回流到数据、Prompt、RAG、工具和评测集。
```

## 3. 关键知识点详解
### 3.1 离线评测集

**是什么：** 离线评测集是在上线前用于稳定评估模型、Prompt、RAG 和 Agent Workflow 的固定样本集合。

**为什么需要：** 没有离线评测，任何优化都只能凭感觉。Prompt 改动、模型切换、RAG 调参都可能引入回归。

**核心机制：** 评测集应覆盖常见问题、长尾问题、边界问题、对抗问题、安全问题、工具调用问题和真实线上 Bad Case。

**工程实现：** 工程上可以用 pytest 或自定义 eval runner 执行，记录版本、输入、输出、分数、失败原因和 trace。

**常见坑：**

- 只用少量简单样本。
- 评测集长期不更新。
- 只评最终答案，不评检索和工具。
- 没有回归阈值。

**优化方式：**

- 分层评测。
- 加入真实 Bad Case。
- 设置发布门槛。
- 每次 Prompt/模型/RAG 改动都跑回归。

**面试表达：** 离线评测集是 Agent 项目的质量地基。没有评测集，就无法证明系统真的变好了。
### 3.2 RAG 评测

**是什么：** RAG 评测同时评估检索质量和生成质量。

**为什么需要：** 答案错误可能来自召回失败、排序失败、上下文构造失败或模型未遵守证据，必须分层定位。

**核心机制：** 检索指标包括 Recall@K、Precision@K、MRR、nDCG、空召回率；生成指标包括答案正确率、引用准确率、幻觉率。

**工程实现：** 工程上应记录 query、召回文档、rerank 分数、最终上下文、答案和引用，便于复盘。

**常见坑：**

- 只看用户是否满意。
- 检索和生成混在一起评。
- 引用看起来正确但不支持答案。
- 没有 gold doc。

**优化方式：**

- 构建 query-gold-doc 集。
- 评估 citation support。
- 对召回失败和生成失败分别归因。
- 将失败样本回流到索引和评测集。

**面试表达：** RAG 评测要先问：正确证据有没有进来；再问：模型有没有正确使用证据。
### 3.3 Agent 任务成功率

**是什么：** 任务成功率衡量 Agent 是否完成用户目标，而不只是最终文本是否好看。

**为什么需要：** Agent 可能答案正确但工具执行失败，也可能工具成功但输出不合规。任务成功率要覆盖整个过程。

**核心机制：** 指标包括最终任务成功率、步骤成功率、工具调用成功率、计划完成率、重试率、循环率、人工接管率、失败恢复率。

**工程实现：** 工程上可为每类任务定义 success criteria，例如 RAG 问答要求答案正确且引用支持，邮件任务要求草稿生成且未越权发送。

**常见坑：**

- 成功条件模糊。
- 只用人工主观评价。
- 没有任务类型分桶。
- 不区分失败原因。

**优化方式：**

- 为任务类型定义程序化成功条件。
- 结合人工和 LLM Judge。
- 按任务类型、用户、工具、模型版本分桶。
- 记录失败 taxonomy。

**面试表达：** Agent 评测核心是任务是否完成，而不是模型是否生成了一段流畅文本。
### 3.4 LLM-as-a-Judge

**是什么：** LLM-as-a-Judge 是用强模型按照评分标准评价输出质量。

**为什么需要：** LLM 评测可扩展、成本低于人工，适合大规模初筛和回归，但存在偏见和误判。

**核心机制：** Judge 应有明确 rubric，例如事实性、引用支持、完整性、格式、安全性，每项给定义和评分示例。

**工程实现：** 工程上可采用双模型评审、顺序打乱、人工抽检、校准集和一致性统计。

**常见坑：**

- Judge 偏好长回答。
- Judge 被候选答案误导。
- 评分标准模糊。
- 完全替代人工评审。

**优化方式：**

- 使用结构化 rubric。
- 隐藏系统信息和答案顺序。
- 抽样人工复核。
- 对 Judge 本身做校准。

**面试表达：** LLM-as-a-Judge 是评测工具，不是最终真理。关键场景要结合人工、规则和程序化验证。
### 3.5 可观测性与 Trace

**是什么：** 可观测性是通过日志、指标和 Trace 理解 Agent 系统运行状态。

**为什么需要：** Agent 长链路中，只看最终答案无法定位问题。必须知道每个节点输入输出、工具耗时、路由原因和错误类型。

**核心机制：** Trace 应记录 request_id、task_id、node_name、input_summary、output_summary、latency、token、cost、tool_status、error_type。

**工程实现：** Python 中可使用 OpenTelemetry、结构化日志、LangSmith 或自建 trace 表。LangGraph 节点天然适合做节点级 trace。

**常见坑：**

- 日志只记录最终答案。
- 没有 trace_id 贯穿全链路。
- 工具调用和模型调用分散记录。
- 日志含敏感数据。

**优化方式：**

- 统一 trace_id。
- 节点级结构化日志。
- 敏感字段脱敏。
- 指标按模型、工具、任务类型分桶。

**面试表达：** 可观测性让 Agent 从黑盒变成可调试系统。没有 trace，就很难解释为什么失败。


## 4. 文字版排查图

```text
Agent 成功率下降
  ↓
先看 Workflow
  ├── 是否循环？
  ├── 是否超时？
  ├── 终止条件是否错误？
  └── 路由是否异常？
  ↓
再看 Tool
  ├── 是否 5xx / 429？
  ├── 是否 schema 错误？
  ├── 是否权限错误？
  └── 是否重试过多？
  ↓
再看 RAG
  ├── 是否空召回？
  ├── 是否错召回？
  ├── 索引是否过期？
  └── Rerank 是否异常？
  ↓
再看 Context / Prompt
  ├── 上下文是否过长？
  ├── 证据是否被截断？
  ├── Prompt 是否变更？
  └── 输出格式是否回归？
  ↓
最后看 Model
  ├── 模型版本是否变化？
  ├── 参数是否变化？
  ├── 成本/延迟是否异常？
  └── 供应商行为是否变化？
```

## 5. 工程实战设计

### 5.1 必采集字段

```text
请求级：
  request_id, user_id, task_id, task_type, timestamp

模型级：
  model_name, prompt_version, input_tokens, output_tokens, latency, cost

节点级：
  node_name, input_summary, output_summary, status, latency

工具级：
  tool_name, arguments_summary, status_code, retry_count, error_type

RAG 级：
  query, rewritten_query, retrieved_doc_ids, rerank_scores, final_context_ids

安全级：
  risk_level, approval_status, policy_hit, blocked_reason

用户反馈：
  rating, correction, complaint_type, followup_action
```

### 5.2 Bad Case Taxonomy

```text
知识类：
  召回失败、错召回、文档过期、引用错误

工具类：
  工具误选、参数错误、权限错误、超时、重复执行

流程类：
  循环、提前终止、路由错误、状态丢失

生成类：
  格式错误、幻觉、遗漏、语气不当

安全类：
  越权、敏感数据泄露、prompt injection、危险动作

产品类：
  用户意图不清、交互不友好、转人工不及时
```

## 6. 与 LangGraph / Python 后端的映射

```text
评测监控对象             实现方式
---------------------------------------------------
节点输入输出             LangGraph node trace
路由原因                 conditional edge log
工具耗时                 tool wrapper metrics
RAG 结果                 retriever / rerank logs
模型成本                 llm_gateway metrics
任务成功率               task table status
Bad Case                 feedback table
离线评测                 eval runner + pytest
线上指标                 Prometheus / OpenTelemetry
链路追踪                 trace_id + spans
```

## 7. 常见误区

### 7.1 只看最终答案

Agent 是过程系统，失败可能发生在计划、检索、工具、状态、生成任意环节。只看最终答案无法定位根因。

### 7.2 评测集和线上样本脱节

评测集要持续吸收线上 Bad Case，否则会越来越不代表真实问题。

### 7.3 没有分桶指标

总体成功率可能掩盖某个任务类型、工具或模型版本的失败。指标必须按任务类型、模型、工具、用户群体分桶。

## 8. 面试题与答题闭环
### Q：如何评估一个 Agent？

**考察点：** Agent 过程评测。

**推荐回答：** 我会分层评估：最终任务成功率、答案正确性、RAG 引用质量、工具调用准确率、步骤数、重试率、人工接管率、成本、延迟和安全拦截。Agent 不只评最终文本，还要评执行过程。

### Q：Agent 成功率下降怎么排查？

**考察点：** 生产故障定位。

**推荐回答：** 我会按 Workflow、Tool、RAG、Context/Prompt、Model 的顺序排查。先看是否循环、超时、路由错误；再看工具 5xx/429/schema/权限；再看空召回、错召回和索引；然后看上下文和 Prompt；最后看模型版本和参数。

### Q：LLM-as-a-Judge 有什么风险？

**考察点：** 评测方法优缺点。

**推荐回答：** 它可扩展但会有位置偏好、冗长偏好、风格偏好和误判。需要明确 rubric，打乱顺序，人工抽检，使用校准集，并且不要让它完全替代人工和程序化验证。


## 9. 本章 TODO Checklist

- [ ] 能区分 LLM 评测和 Agent 评测。
- [ ] 能设计离线评测集。
- [ ] 能说出 RAG 检索和生成指标。
- [ ] 能定义 Agent 任务成功率。
- [ ] 能设计节点级 Trace 字段。
- [ ] 能按 Workflow、Tool、RAG、Prompt、Model 排查成功率下降。
- [ ] 能建立 Bad Case 分类和回流机制。
