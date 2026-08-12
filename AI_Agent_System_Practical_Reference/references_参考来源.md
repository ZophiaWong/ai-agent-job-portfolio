# references_参考来源

> 生成日期：2026-04-29  
> 说明：本文件记录本资料使用的主要来源。招聘信息会随时间变化，岗位调研仅作为能力画像依据。

## 1. 用户指定原始材料

- GitHub 目录：`guoguo-tju/agent_java_offer/docs/interview_prep/01_AI`
- 主题包括：
  - Agent 基础
  - Workflow 与多 Agent
  - RAG
  - 上下文工程与记忆
  - 模型调优与微调
  - 评测与监控
  - 安全与风控
  - 框架协议与工程化
  - 追加补充

## 2. 官方文档

### LangGraph / LangChain

- LangGraph Overview  
  https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph Workflows and Agents  
  https://docs.langchain.com/oss/python/langgraph/workflows-agents
- LangGraph Interrupts：暂停、恢复、节点重启与副作用规则
  https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph Persistence：checkpointer、thread 与 store 边界
  https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph Graph API：`Command(resume=...)`
  https://docs.langchain.com/oss/python/langgraph/graph-api
- LangChain Overview  
  https://docs.langchain.com/oss/python/langchain/overview

访问日期：2026-07-19。框架代码片段按这些页面核对；仍需在具体项目中用锁定版本验证。

### Model Context Protocol

- MCP Architecture：Host、Client、Server 和协议分层
  https://modelcontextprotocol.io/docs/learn/architecture
- MCP Lifecycle（2025-11-25 稳定规范）
  https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- MCP Transports（stdio、Streamable HTTP）
  https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP Authorization（HTTP 授权与 token audience）
  https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
- MCP Tools
  https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- MCP Resources
  https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- MCP Prompts
  https://modelcontextprotocol.io/specification/2025-11-25/server/prompts

访问日期：2026-07-19。本手册以 MCP 2025-11-25 稳定规范为基线；实验功能必须明确标注，不静默混入稳定协议说明。

### LlamaIndex / CrewAI / AutoGen

- LlamaIndex Documentation  
  https://docs.llamaindex.ai/

- CrewAI Documentation  
  https://docs.crewai.com/

- Microsoft AutoGen GitHub  
  https://github.com/microsoft/autogen

- Microsoft Agent Framework  
  https://learn.microsoft.com/en-us/agent-framework/

## 3. 经典论文与概念来源

- ReAct: Synergizing Reasoning and Acting in Language Models  
  https://arxiv.org/abs/2210.03629

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks  
  https://arxiv.org/abs/2005.11401

- Tree of Thoughts: Deliberate Problem Solving with Large Language Models  
  https://arxiv.org/abs/2305.10601

- Graph of Thoughts: Solving Elaborate Problems with Large Language Models  
  https://arxiv.org/abs/2308.09687

- Lost in the Middle: How Language Models Use Long Contexts  
  https://arxiv.org/abs/2307.03172

- LoRA: Low-Rank Adaptation of Large Language Models  
  https://arxiv.org/abs/2106.09685

- QLoRA: Efficient Finetuning of Quantized LLMs  
  https://arxiv.org/abs/2305.14314

- Direct Preference Optimization  
  https://arxiv.org/abs/2305.18290

## 4. 公开 JD 调研来源

调研中参考了公开招聘页和公开搜索结果，岗位覆盖：

- Generative AI Engineer
- AI Agent Engineer
- LLM Engineer
- RAG Engineer
- Agentic AI Engineer
- Python AI Backend Engineer
- LLMOps / AI Platform Engineer

样本能力关键词包括：

```text
Agentic Workflow
LangGraph
LangChain
AutoGen
CrewAI
Function Calling / Tool Use
MCP
RAG
Vector Database
Hybrid Search
Rerank
Prompt Engineering
Context Engineering
Python Backend
FastAPI
asyncio
Evaluation
Observability
OpenTelemetry
Security / Guardrails
Human-in-the-loop
```

代表性公开 JD 来源包括：

- Dataiku Generative AI Engineer
- Sonder AI / Agentic workflow roles
- OfferUp AI Engineering roles
- Translucent AI / Agentic Systems roles
- CodeRoad Agent Evaluation roles
- Humana Applied AI / Agentic AI roles
- GE Vernova AI Agent roles
- 其他公开搜索结果和企业招聘页

## 5. 使用注意

1. 框架生态变化快，尤其是 AutoGen、OpenAI Agents SDK、Microsoft Agent Framework 等方向，应定期检查官方文档。
2. 岗位 JD 会变化，能力画像建议每 1-2 个月更新一次。
3. 本资料优先服务“AI Agent 应用工程 / Python 后端 / RAG / LLMOps”方向，不等同于大模型预训练或底层算法研究资料。
4. 微调章节为应用岗位所需的工程理解，不替代专门的模型训练课程。
5. 安全章节应结合具体业务合规要求补充。
