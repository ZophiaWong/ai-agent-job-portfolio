# 04_RAG检索增强生成工程

## 0. 章节元信息

- 岗位重要性：P0
- 面试常见度：高
- 工程实战价值：高
- 推荐学习深度：精读

适合岗位：

- AI Agent 应用工程师
- RAG 工程师
- Python AI 后端工程师
- LLMOps 工程师

对应岗位能力：

- RAG 离线索引
- 在线检索链路
- Chunking
- Embedding
- 向量数据库
- Hybrid Search
- Rerank
- RAG Evaluation
- Agentic RAG

依赖章节：

- 01 Agent 基础
- 03 工具调用

相关章节：

- 05 上下文工程
- 09 评测监控
- 16 端到端实战 Lab


## 1. 本章学习目标

RAG 是 AI Agent 应用岗位中最核心的工程能力之一。它解决的问题不是“让模型变大”，而是让模型在回答时能够使用外部、私有、实时、可追溯的知识。

学完本章后，你需要能够讲清：

```text
原始文档如何变成可检索知识；
用户问题如何转成检索请求；
如何召回、重排、压缩和组装上下文；
如何让答案带引用；
召回不准时如何排查；
RAG 如何和 Agent / LangGraph / Python 后端结合。
```

## 2. 核心概念总览

### 2.1 RAG 的定义

RAG，即 Retrieval-Augmented Generation，检索增强生成。它的基本思想是：

```text
先检索相关外部知识；
再把知识作为上下文提供给模型；
最后让模型基于上下文生成答案。
```

RAG 不修改模型参数，而是通过外部知识注入来提升事实性、时效性和可追溯性。

### 2.2 RAG 解决的问题

```text
模型知识过时；
模型不知道企业私有数据；
模型容易幻觉；
答案无法追溯来源；
不适合把频繁变化的知识全都微调进模型；
业务数据需要权限控制和版本管理。
```

### 2.3 RAG 不解决的问题

```text
模型推理能力不足；
用户问题本身不清楚；
文档质量很差；
检索没有召回正确证据；
上下文过长导致模型忽略关键证据；
生成时不遵守引用要求；
权限或数据治理缺失。
```

RAG 是系统工程，不是“接一个向量库”就完成。

## 3. 关键知识点详解
### 3.1 离线索引链路

**是什么：** 离线索引链路是把原始文档处理成可检索索引的过程。

**为什么需要：** 模型无法直接高效读取大量文档。需要先把文档解析、清洗、切块、向量化并写入检索系统。

**核心机制：** 典型流程是文档接入 → 解析 → 清洗 → 切块 → Embedding → 写向量库 → 写元数据 → 版本管理。

**工程实现：** Python 中可以用文档解析器、LlamaIndex/LangChain loader、自定义 chunker、embedding 服务、pgvector/Milvus/FAISS/Elasticsearch 等完成。生产系统需要增量索引、失败重试和索引版本。

**常见坑：**

- 文档解析失败但未告警。
- 切块破坏语义。
- 元数据缺失导致无法权限过滤。
- 索引无版本，无法回滚。

**优化方式：**

- 建立文档解析质量检查。
- 按文档类型设计切块策略。
- 为 chunk 写入 doc_id、section、version、permission、timestamp。
- 使用双索引或蓝绿切换。

**面试表达：** RAG 离线链路的关键不是 embedding，而是数据质量、切块策略、元数据治理和索引版本化。
### 3.2 在线检索链路

**是什么：** 在线检索链路是从用户问题到召回证据、组装上下文、生成答案的实时过程。

**为什么需要：** 用户问题往往不等于最佳检索 query，需要规范化、改写、过滤、召回、重排和压缩。

**核心机制：** 典型流程是 Query Rewrite → 向量召回/BM25 → Hybrid 合并 → Rerank → Context Compression → Answer Generation → Citation。

**工程实现：** 在 LangGraph 中可以把 Query Rewrite、Retriever、Reranker、Context Builder、Answer Node 拆成独立节点，便于评测和定位问题。

**常见坑：**

- 直接用原始问题检索。
- TopK 固定不变。
- 召回后不重排。
- 上下文拼接无顺序和引用。
- 答案没有证据来源。

**优化方式：**

- 针对问题类型选择检索策略。
- 使用 Hybrid Search 提升召回。
- 引入 Rerank 提升排序质量。
- 按证据重要性和 token 预算组装上下文。
- 强制引用来源。

**面试表达：** 在线 RAG 的核心是把用户问题变成高质量上下文，而不是简单把 TopK 文档塞给模型。
### 3.3 Chunking 策略

**是什么：** Chunking 是把文档拆成适合检索和生成的小块。

**为什么需要：** 文档太长无法直接放入上下文，也不利于精确召回。切块决定了检索粒度、语义完整性和上下文噪声。

**核心机制：** 常见策略包括固定长度切块、按段落/标题切块、语义切块、代码按函数/类切块、表格特殊处理、多尺度切块。

**工程实现：** 工程上可以从 300-800 tokens 的 chunk + 10%-20% overlap 起步，再根据 Recall@K、答案质量和成本调优。不同文档类型应采用不同切块策略。

**常见坑：**

- 块太大导致噪声高。
- 块太小导致语义断裂。
- overlap 过大导致重复召回。
- 表格、代码、配置文件按普通文本切坏。

**优化方式：**

- 按标题层级保留路径。
- 代码按函数/类/调用关系切。
- 表格保留表头和行列语义。
- 引入 parent-child / small-to-large chunking。

**面试表达：** Chunking 的本质是召回粒度和语义完整性的权衡。面试中要能讲出块太大和块太小分别有什么问题。
### 3.4 Embedding 与向量检索

**是什么：** Embedding 是把文本映射成向量，向量检索根据语义相似度找到相关 chunk。

**为什么需要：** 关键词检索只能匹配字面词，Embedding 能捕捉语义相似。但它也可能忽略精确术语、数字、代码符号和权限条件。

**核心机制：** 向量库通常基于 ANN 算法提升检索效率，例如 HNSW、IVF、PQ 等。检索结果还需要结合元数据过滤和 rerank。

**工程实现：** 模型选型要看语言、领域、维度、速度、成本、私有部署和评测指标。向量库可选 pgvector、Milvus、FAISS、Elasticsearch/OpenSearch。

**常见坑：**

- 只看 embedding benchmark，不做业务评测。
- 忽视中文/行业术语表现。
- 没有归一化和一致预处理。
- 权限过滤放在召回之后导致泄露风险。

**优化方式：**

- 构建业务 query-doc 评测集。
- 评估 Recall@K、MRR、nDCG。
- 混合关键词和向量检索。
- 召回前或召回中加入元数据过滤。

**面试表达：** Embedding 是 RAG 的语义召回基础，但不是万能。生产系统通常需要向量检索、关键词检索、元数据过滤和 Rerank 组合。
### 3.5 Hybrid Search 与 Rerank

**是什么：** Hybrid Search 是把向量检索和关键词检索结合；Rerank 是对初召回结果进行更精细排序。

**为什么需要：** 向量检索适合语义相似，BM25 适合精确词、缩写、数字、专有名词。初召回注重召回率，Rerank 注重排序质量。

**核心机制：** Hybrid 可以合并 BM25 和向量结果，Rerank 可以用 cross-encoder、LLM 或规则特征对候选 chunk 排序。

**工程实现：** 工程上常见做法是向量 TopK 50 + BM25 TopK 50 合并去重，再 Rerank 到 TopK 5-10，最后进入上下文压缩。

**常见坑：**

- 只用向量导致精确词漏召。
- Rerank 候选集太小，正确文档没进来。
- Rerank 成本过高。
- 重排后丢失引用元数据。

**优化方式：**

- 初召回保证高 Recall。
- Rerank 控制候选规模。
- 缓存高频 query 结果。
- 保留 chunk_id、doc_id、score、rank_reason。

**面试表达：** Hybrid 解决召回覆盖，Rerank 解决排序质量。面试中可以说：召回阶段宁可多召回，重排阶段再提高精度。
### 3.6 Agentic RAG

**是什么：** Agentic RAG 是让 Agent 动态决定是否检索、检索什么、检索几轮、是否调用其他数据源或工具。

**为什么需要：** 传统 RAG 通常是一条固定链路；复杂问题可能需要多跳查询、子问题拆解、不同数据源联合检索和结果校验。

**核心机制：** Agent 可以先判断问题类型，再做 query decomposition、multi-query retrieval、SQL/向量/图谱联合查询、反思是否证据充分。

**工程实现：** 在 LangGraph 中，Agentic RAG 可以由 Router、Query Planner、Retriever、Reranker、Evidence Checker、Answer Node 组成循环。

**常见坑：**

- 让 Agent 无限制检索。
- 多轮检索没有证据合并规则。
- 检索结果相互矛盾时不处理。
- 没有成本控制。

**优化方式：**

- 设置最大检索轮数。
- 对证据做去重和冲突检测。
- 低置信度转人工或说明不确定。
- 记录每次检索 query 和结果质量。

**面试表达：** Agentic RAG 的价值是适应复杂问题，但必须通过状态机控制轮数、成本和证据质量。


## 4. 文字版架构图

### 4.1 离线索引链路

```text
原始文档
  ↓
文档接入
  ↓
格式解析
  ├── PDF / Word / Markdown
  ├── 网页
  ├── 表格
  ├── 代码仓库
  └── 数据库记录
  ↓
数据清洗
  ├── 去噪
  ├── 去重
  ├── 标题层级识别
  └── 权限元数据补齐
  ↓
Chunking
  ↓
Embedding
  ↓
向量库
  +
元数据索引
  +
原始文档存储
  ↓
索引版本管理
```

### 4.2 在线问答链路

```text
用户问题
  ↓
权限识别
  ↓
Query Rewrite / Query Decomposition
  ↓
向量检索
  +
关键词检索
  +
元数据过滤
  ↓
候选结果合并去重
  ↓
Rerank
  ↓
上下文压缩与组装
  ↓
LLM 基于证据生成答案
  ↓
引用来源校验
  ↓
返回答案
  ↓
记录 query、召回、重排、答案、用户反馈
```

## 5. 工程实战设计

### 5.1 RAG Bad Case 排查

```text
用户说答案错了
  ↓
先看是否召回正确证据
  ├── 没召回：查 query rewrite、chunking、embedding、向量库、权限过滤
  └── 召回了：继续
  ↓
看正确证据排序是否靠前
  ├── 不靠前：查 rerank、score 融合、TopK
  └── 靠前：继续
  ↓
看上下文是否被截断或放在中间
  ├── 被截断：查 token budget 和 context compression
  └── 未截断：继续
  ↓
看模型是否遵守证据
  ├── 没遵守：查 prompt、引用约束、答案校验
  └── 遵守但文档错：查知识库数据质量
```

### 5.2 RAG 指标

```text
检索指标：
- Recall@K
- Precision@K
- MRR
- nDCG
- 空召回率
- 错召回率

生成指标：
- 答案正确率
- 引用准确率
- 引用覆盖率
- 幻觉率
- 拒答合理率

系统指标：
- p50 / p95 / p99 延迟
- Embedding 成本
- Rerank 成本
- 向量库 QPS
- 索引新鲜度
```

## 6. 与 LangGraph / Python 后端的映射

```text
RAG 步骤                  LangGraph 节点
------------------------------------------------
权限判断                  auth_filter_node
Query Rewrite             rewrite_node
子问题拆解                query_planner_node
向量召回                  vector_retriever_node
BM25 召回                 keyword_retriever_node
结果合并                  merge_node
Rerank                    rerank_node
上下文压缩                context_builder_node
答案生成                  answer_node
引用校验                  citation_validator_node
Bad Case 记录             feedback_node
```

Python 技术栈示例：

```text
FastAPI：问答接口
PostgreSQL：文档元数据、权限、任务记录
pgvector / Milvus / FAISS：向量检索
Elasticsearch / OpenSearch：关键词检索
Redis：缓存热门 query、短期状态
Celery / asyncio：异步索引与并行检索
Object Storage：原始文档和解析结果
OpenTelemetry：检索链路 trace
```

## 7. 常见误区

### 7.1 RAG 等于向量数据库

向量库只是 RAG 的一部分。RAG 的质量更依赖数据清洗、切块、元数据、检索策略、重排、上下文组装和评测。

### 7.2 TopK 越大越好

TopK 过大可能引入噪声、增加成本，并触发 Lost in the Middle。正确做法是通过评测选择 TopK，并用 Rerank 和压缩提高上下文质量。

### 7.3 有引用就一定可靠

引用可能不支持答案，也可能是模型随意引用。需要做 citation validation，检查答案中的关键断言是否能被引用证据支持。

## 8. 面试题与答题闭环
### Q：RAG 的完整流程是什么？

**考察点：** 端到端链路、离线/在线区分。

**推荐回答：** RAG 分离线和在线两条链路。离线链路是文档接入、解析清洗、切块、Embedding、写入向量库和元数据索引、版本管理。在线链路是用户问题、Query Rewrite、向量/BM25 召回、Hybrid 合并、Rerank、上下文组装、LLM 生成、引用校验和日志回流。

### Q：RAG 召回不准怎么优化？

**考察点：** Bad Case 定位、检索优化。

**推荐回答：** 先区分是没召回、召回但排序差，还是召回了但生成没用。没召回看 query rewrite、chunking、embedding、元数据过滤；排序差看 hybrid search 和 rerank；生成没用看上下文压缩、prompt、引用校验和模型遵循能力。

### Q：Chunking 如何设计？

**考察点：** 切块策略和权衡。

**推荐回答：** Chunking 要在语义完整性和检索粒度之间权衡。块太大噪声高、成本高，块太小语义断裂。可以从段落/标题切块、适度 overlap 起步，代码按函数/类切，表格保留表头和行列语义，必要时做 small-to-large 或多尺度切块。


## 9. 本章 TODO Checklist

- [ ] 能画出 RAG 离线索引链路。
- [ ] 能画出 RAG 在线问答链路。
- [ ] 能解释 Chunking 的权衡。
- [ ] 能说明 Embedding 模型和向量库选型维度。
- [ ] 能解释 Hybrid Search 和 Rerank 的作用。
- [ ] 能说出 RAG 的核心评测指标。
- [ ] 能设计 LangGraph + RAG 的节点结构。
- [ ] 能按召回、重排、上下文、生成四层排查 Bad Case。
