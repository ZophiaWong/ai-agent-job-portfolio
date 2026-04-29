# AI Agent 系统学习与工程实战参考手册

> 生成日期：2026-04-29  
> 资料定位：AI Agent 应用岗位的系统学习 + 工程实战参考资料。  
> 来源基础：用户指定 GitHub 目录、公开 JD 调研、官方框架文档与经典论文。  
> 注意：招聘信息会变化，岗位调研用于能力画像，不代表某公司当前仍在招聘。

## 1. 资料定位

这是一份面向 AI Agent 应用岗位的系统学习与工程实战资料。它不是单纯的面试题库，也不是框架 API 手册，而是把 Agent、RAG、上下文工程、工具调用、LangGraph、Python 后端、评测监控、安全治理和项目表达整合成一套长期参考资料。

核心目标：

```text
把“会调模型 API”升级为“能设计、实现、评测、上线和治理 Agent 系统”。
```

## 2. 推荐学习顺序

```text
Part 01：Agent 核心原理
  01 Agent 基础
  02 Workflow 与多 Agent
  03 工具调用 / Function Calling / MCP

Part 02：知识、上下文与模型优化
  04 RAG
  05 上下文工程与记忆
  06 Prompt / Context / RAG / 微调协同
  07 模型调优与微调

Part 03：Python 工程化与生产治理
  08 Python 后端工程实践
  09 评测、监控、可观测性与 Bad Case 回流
  10 安全、权限、风控与 HITL

Part 04：项目与面试表达
  11 项目设计模板
  12 高频面试题
  13 总复习 Checklist

Part 05：框架专项与实战 Lab
  14 LangGraph 工程实战专项
  15 Agent 框架选型
  16 端到端实战 Lab
```

## 3. 学习路径图

```text
Agent 是什么
  ↓
Agent 如何规划与编排
  ↓
Agent 如何调用工具和外部系统
  ↓
Agent 如何获取知识：RAG
  ↓
Agent 如何管理上下文、状态和记忆
  ↓
效果不好时如何选择 Prompt / RAG / 工具链路 / 微调
  ↓
如何用 Python + LangGraph 做成服务
  ↓
如何评测、监控、安全治理
  ↓
如何包装成项目和面试表达
```

## 4. 文件使用方法

- 想系统学习：按 Part 01 → Part 05 顺序读。
- 想面试冲刺：先读 `12_高频面试题`、`11_项目设计模板`、`16_端到端实战Lab`。
- 想投 RAG 岗：看 `role_paths/RAG工程师学习路径.md`。
- 想投 LangGraph/Agent 岗：看 `role_paths/LangGraph_Agent工程师学习路径.md`。
- 想做项目：从 `16_端到端实战Lab与代码骨架.md` 开始反推需要补哪些章节。

## 5. 重要原则

### 5.1 先通用原理，后框架 API

LangGraph 是本资料的主框架实践线，但资料不会变成 LangGraph API 手册。每个框架能力都先解释通用工程动机，再讲 LangGraph 如何映射。

### 5.2 先系统稳定，再模型能力

Agent 项目失败经常不是模型“不聪明”，而是流程不可控、上下文污染、工具失败、状态膨胀、缺少评测、安全边界不清。

### 5.3 每个知识点形成答题闭环

```text
定义 → 作用 → 原理 → 工程实现 → 常见坑 → 优化方式 → 面试表达
```

## 6. 最终验收标准

学完后你应该能够：

- 画出一个企业级 Agent 系统的文字架构图；
- 讲清 Agent、Workflow、RAG、Tool Calling、MCP、LangGraph、Context Engineering 的关系；
- 设计一个 Python + LangGraph + RAG 的端到端项目；
- 解释 Agent 成功率下降时如何排查；
- 解释高风险工具调用如何做权限、HITL、幂等和审计；
- 在面试中把项目讲成“业务目标 → 架构设计 → 指标 → 风险 → 优化闭环”。
