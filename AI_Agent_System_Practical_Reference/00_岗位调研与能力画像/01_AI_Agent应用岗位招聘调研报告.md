# AI Agent 应用岗位招聘调研报告

> 生成日期：2026-04-29  
> 资料定位：AI Agent 应用岗位的系统学习 + 工程实战参考资料。  
> 来源基础：用户指定 GitHub 目录、公开 JD 调研、官方框架文档与经典论文。  
> 注意：招聘信息会变化，岗位调研用于能力画像，不代表某公司当前仍在招聘。

## 1. 调研目标

本报告用于回答：市场上的 AI Agent 应用岗位到底需要哪些能力，以及这些能力如何映射到后续学习资料。调研范围聚焦“应用开发 / Agent 工程 / RAG 工程 / AI 后端 / LLMOps”，不以纯算法研究、模型预训练、CV/NLP 传统算法岗为主。

## 2. 调研方法

- 时间范围：2026-04-29 前后公开可访问岗位与搜索结果。
- 语言范围：中文语境求职为主，英文岗位为辅，用于校准国际市场对 Agentic Workflow、RAG、Tool Use、Evaluation、Observability 的要求。
- 样本口径：公开 JD 页面、公司招聘页、Greenhouse/Ashby/Workable 等公开页面，以及可访问搜索摘要。
- 样本数量：25 条公开岗位样本。
- 限制说明：部分招聘平台存在登录、反爬或过期问题，因此本报告只把样本用于能力画像，不把岗位状态视为实时招聘承诺。

## 3. 样本岗位清单

| # | 公司/来源 | 岗位 | 关键词 | 来源 |
|---:|---|---|---|---|
| 1 | Dataiku | Generative AI Engineer | Agent Builder、LangGraph/CrewAI/Claude Agent SDK/OpenAI Agents SDK、MCP、Agent Tools、API 集成、Knowledge Banks | https://job-boards.greenhouse.io/dataiku/jobs/5978968004 |
| 2 | Humana | Senior Applied AI Engineer (Agentic AI) | 生产级 AI agents、agent orchestration、RAG、tool use、workflow automation | https://careers.humana.com/us/en/job/R-406185/Senior-Applied-AI-Engineer-Agentic-AI |
| 3 | GE Vernova | Senior AI Agent Engineer | LLM agents、RL、planning algorithms、多 Agent 架构、API/backend/database/enterprise app 集成 | https://careers.gevernova.com/sr-ai-agent-engineer/job/R5025220 |
| 4 | Newton Research | Junior Software Engineer (Backend + AI) | LangGraph-based agents、RAG memory、vector embeddings、semantic search、API endpoints | https://job-boards.greenhouse.io/newtonresearch/jobs/5202112008 |
| 5 | Sonder Australia | Fullstack AI Software Engineer (Agentic Systems) | LangGraph/CrewAI/native tool-use、RAG、context engineering、chunking、metadata filtering、MCP servers | https://job-boards.greenhouse.io/sonderaustralia/jobs/8507622002 |
| 6 | Lumos | AI Agent Engineer | tool-calling systems、RAG pipelines、autonomous orchestration、LangChain/LangGraph、API design、system performance | https://job-boards.greenhouse.io/lumos/jobs/6629003003 |
| 7 | Valtech | Senior Python+AI Engineer | LLM-powered apps、tool-calling、agentic patterns、LangChain、LangGraph、stateful workflows | https://job-boards.eu.greenhouse.io/valtech/jobs/4770353101 |
| 8 | Ping Identity | AI Automation Engineer | production-grade agentic workflows、RAG、tool use、LangGraph/CrewAI/custom orchestration、多 Agent | https://job-boards.greenhouse.io/pingidentity/jobs/8472396002 |
| 9 | OfferUp | AI Engineer | Python、agentic frameworks、LangChain/LangGraph、function calling、tool-use、RAG、asyncio、streaming、Pydantic | https://job-boards.greenhouse.io/offerup/jobs/7739995 |
| 10 | Translucent | Senior AI Engineer | state machines、tool routing、planning loops、LangGraph/CrewAI/AutoGen、tool schema、hybrid search、rerank、context-window management | https://job-boards.greenhouse.io/translucent/jobs/4121068009 |
| 11 | GR8 Tech | Senior AI Specialist | LLM/RAG architectures、tool/function calling、MCP-like systems、production products、performance/cost trade-offs | https://job-boards.eu.greenhouse.io/gr8tech/jobs/4784094101 |
| 12 | Toogeza | AI Agent Architect | LangGraph/LangChain、cyclic state graphs、stateful agent systems、advanced RAG、memory | https://jobs.ashbyhq.com/toogeza/646f0294-31b3-4dbf-9b25-798a72b189dc |
| 13 | Curie | Senior AI Engineer | multi-step AI agent pipelines、RAG pipelines、vector search、retrieval systems | https://jobs.ashbyhq.com/curie/aa329701-6a5b-4968-a9e7-4a22f41248ad |
| 14 | Telepatia | AI Engineer | AI agent pipelines、reasoning、orchestration、context engineering、RAG、vector stores、knowledge graphs | https://jobs.ashbyhq.com/telepatia/c6ec85dc-e8ff-4e68-b4b7-352128c477ed |
| 15 | MightyBot | AI Engineer | RAG indexing/ranking/query processing、LangGraph、LlamaIndex、SmolAgent、Instructor、Anthropic | https://jobs.ashbyhq.com/mightybot/4338903c-c692-4499-9350-9f72caa7ad0a |
| 16 | Dexmate | Senior Software Engineer, AI Platform | RAG pipelines、when to retrieve vs long context、LangGraph/PydanticAI、agent architectures | https://jobs.ashbyhq.com/dexmate/a71df3b6-5248-442d-b1cf-cd7ae450190a |
| 17 | Camunda | Senior Software Engineer, Enterprise Agentic Automation | RAG、constraints、evaluation signals、agent frameworks LangChain/LangGraph/CrewAI | https://jobs.ashbyhq.com/camunda/d095095f-600c-4803-8347-6e1a81fd80be/application |
| 18 | Trivium | AI Agent Engineer | Backend/LLM systems、Python/Node/TypeScript、AI agent systems | https://jobs.workable.com/view/wb4c4uaPgS3GnrdwpLtLxo/remote-ai-agent-engineer-in-ukraine-at-trivium |
| 19 | Capgemini | AI Application Engineer (GenAI / RAG) Python | LLMs、RAG pipelines、conversational interfaces、intelligent tooling、production-ready prototypes | https://www.capgemini.com/jobs/436256-en_US_SAPBTP/ |
| 20 | Dice / Capgemini | AI Application Engineer (GenAI / RAG) Python | GenAI powered applications、LLMs、RAG pipelines、conversational interfaces、engineering workflows | https://www.dice.com/job-detail/3a27c8f1-66aa-498e-abd3-3545d73d438b |
| 21 | StackOne | AI Engineer, Developer Ecosystem | LangGraph、DSPy、RLMF harness、auto-research loops、long-horizon agents、RAG vs long context | https://jobs.ashbyhq.com/stackone/a1fda84a-303e-4500-8d72-d93c6fb99b53 |
| 22 | Abacum | AI Engineer | fine-tuning、evaluations、prompt optimization、RAG pipelines、LangGraph | https://jobs.ashbyhq.com/abacum/d4851c02-d36a-4a88-8ce8-a83e514b367d |
| 23 | Niural | Head of Applied AI | agentic systems、multi-agent orchestration in production、LangGraph | https://jobs.ashbyhq.com/niural/95de8b61-2f6f-455a-a4a9-2538a2eed5d9 |
| 24 | CodeRoad | QA Analyst (AI Systems) | Agent evaluation、Python scripts、RAG instances、Success Rate、Tool Use Accuracy、Planning Quality、Autonomy | https://job-boards.greenhouse.io/coderoad/jobs/4205541009 |
| 25 | Citi | Senior Data Scientist / Gen AI Engineer | LangGraph、CrewAI、AutoGen、tool-use/function-calling、multi-agent orchestration | https://jobs.citi.com/job/pune/senior-data-scientist-gen-ai-engineer-assistant-vice-president/287/94492649152 |

## 4. 高频能力观察

### 4.1 RAG 与知识库工程仍然是最高频能力

公开 JD 中大量出现 RAG pipeline、vector search、semantic chunking、rerankers、retrieval systems、hybrid search、metadata filtering、Knowledge Banks 等词。这说明应用岗位并不是只需要会调大模型 API，而是要能把企业私有知识、外部数据源和模型输出稳定连接起来。

工程上，RAG 的岗位价值不只在“检索一段文本”，而在：文档解析、切块、索引、召回、重排、上下文组装、引用验证、评测回流、索引版本治理。

### 4.2 Agent Workflow、状态机和框架能力明显上升

LangGraph、LangChain、CrewAI、AutoGen、custom orchestration、stateful agent systems、planning loops、tool routing、multi-agent orchestration 等关键词多次出现。岗位不是要求候选人只会写 prompt，而是能把 Agent 拆成可控节点、状态、边、条件路由和终止条件。

这也是本资料把 `工具调用` 提前到第 3 章、并新增 `LangGraph 工程实战专项` 的原因。

### 4.3 Tool Use / Function Calling / MCP 是 Agent 应用的行动层

多个 JD 提到 tool-use、function calling、API integration、MCP servers、tool schemas、tool invocation、validation、multi-step chaining。它们共同指向一个能力：让模型通过受控接口连接真实系统。

面试中不能只说“模型调用工具”，而要补充服务端校验、权限、幂等、超时、重试、熔断、降级和审计。

### 4.4 Python 后端工程是应用岗位落地能力的核心

样本中频繁出现 Python、async Python、Pydantic、backend services、API design、system performance、production systems。对于你的技术栈，重点不是 Java，而是 FastAPI、asyncio、任务队列、Redis、PostgreSQL、pgvector/Vector DB、日志、Trace、Docker、限流和幂等。

### 4.5 Evaluation、Observability 和 Bad Case 回流正在从加分项变成生产必备

部分 JD 明确要求 evaluation pipeline、Agent evaluation、success rate、tool use accuracy、planning quality、observability、OpenTelemetry、cost/latency trade-offs。生产级 Agent 需要证明“是否真的变好”，并定位“为什么失败”。

### 4.6 微调是加分项，不是应用岗第一优先级

Fine-tuning、LoRA、DPO 等在部分岗位出现，但更常见于高级 AI Engineer、AI Platform、模型适配类岗位。对一般 Agent 应用开发，优先级通常是：RAG / Workflow / Tool Calling / Context / Python 后端 / Evaluation，高于微调。

## 5. 调研结论

AI Agent 应用岗位的核心不是“会不会调用一个模型 API”，而是能否构建一个可上线的任务系统：

```text
用户目标
  ↓
意图理解与任务拆解
  ↓
状态化 Workflow / LangGraph
  ↓
RAG 获取知识
  ↓
Tool Calling / MCP 执行动作
  ↓
上下文与记忆治理
  ↓
评测、监控、安全、审计
  ↓
持续 Bad Case 回流
```

因此后续资料应围绕 P0 能力组织：Agent 基础、Workflow/LangGraph、Tool Calling/MCP、RAG、上下文工程、Python 后端、评测监控。微调、AutoGen、CrewAI、复杂推理方法作为进阶和选型补充。
