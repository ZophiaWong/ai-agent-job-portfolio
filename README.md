# AI Agent 求职准备系统

面向国内、转行、初中级 AI Agent 应用工程师的能力驱动型准备仓库。

本仓库不是按顺序读完的资料合集。推荐循环是：

```text
岗位核心能力 → 诊断证据 → 互动学习 → 模拟面试
→ 更新弱点与计划 → 项目/求职表达 → 延迟复测
```

## 快速开始

初始化不会提交的私人状态：

```shell
./.codex/skills/interview-prep-coach/scripts/init-interview-prep --root .
./.codex/skills/interview-prep-coach/scripts/check-state --root .
```

然后在 Codex 中调用 [`interview-prep-coach`](.codex/skills/interview-prep-coach/SKILL.md)：

```text
Use $interview-prep-coach to initialize and diagnose my interview preparation.
安排我今天 8 小时的学习。
互动教我 RAG evaluation。
复测我上次没有掌握的能力。
深挖 MeterDesk。
进行一次 AI Agent 技术模拟面试。
```

默认先用两天建立能力基线：第一天覆盖 Agent、RAG、Evaluation 和项目；第二天覆盖
Python、后端、SQL/DSA、TypeScript/Node 和求职表达。能力等级必须来自回答、执行结果、
项目证据或真实面试反馈，不能由阅读进度或自评直接决定。

## 核心入口

- [核心能力模型](.codex/skills/interview-prep-coach/references/competency-model.md)：C01–C13、目标等级和证据标准。
- [系统学习主线](AI_Agent_System_Practical_Reference/00_README_学习路线与资料使用说明.md)：Agent、RAG、工程治理和实战参考。
- [面试资料总览](interviews-docs/README.md)：按岗位能力选择专项资料，并使用统一练习协议。
- [AI 面试资料](interviews-docs/01-AI/README.md)
- [后端面试资料](interviews-docs/02-后端/README.md)
- [DSA 面试资料](interviews-docs/03-DS_AL/README.md)
- [Python 专项](interviews-docs/05-misc/python/README.md)
- [Node.js 专项](interviews-docs/05-misc/nodejs/README.md)
- [简历、自我介绍与行为面试](interviews-docs/04-career/README.md)
- [工程实践与 vibe coding](best-practice/README.md)
- [项目证据索引](projects/README.md)：MeterDesk 与 Forge Harness。

## 公开内容与私人状态

仓库中提交通用知识、模板、skill、脚本和项目索引。`.local/interview-prep/` 保存真实简历、
目标、能力矩阵、计划、弱点、故事和 session；该目录被 Git 忽略，不应复制到公开文档。

未来遇到心仪岗位时，可把 JD 放入私人状态。JD 只覆盖通用能力的目标等级和优先级，
不会复制能力或改写历史证据。

## 项目结构

```text
.codex/skills/             Codex 求职教练与 Anki skill
AI_Agent_System_Practical_Reference/  系统化学习资料
interviews-docs/           技术与求职表达练习
learning-materials/        专题速查材料
best-practice/             工程方法和案例
projects/                  独立项目的证据索引
tests/                     状态脚本与导航测试
.local/interview-prep/     私人状态（不提交）
```

## Anki

[`anki-card-maker`](.codex/skills/anki-card-maker/SKILL.md) 只用于定义、区别、命令、决策规则和
常见陷阱等稳定、原子化知识。模拟表达、系统设计判断和宽泛技能不应直接制卡。

启动带 Anki MCP 配置的 Codex：

```shell
./scripts/codex-anki
```

生成卡片后先预览，只有明确确认后才写入 Anki。

## Acknowledgements

- [agent_java_offer](https://github.com/guoguo-tju/agent_java_offer)
