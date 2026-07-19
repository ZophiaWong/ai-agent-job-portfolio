# 受控的 Agent 辅助开发

## 先分清两个说法

历史上的公共术语 [vibe coding](https://x.com/karpathy/status/1886192184808149383) 指一种用自然语言快速试做的编程方式。本文不把它当作工程交付方法。这里讨论的是受控的 Agent 辅助开发：人负责目标、边界和验收，Agent 在明确范围内帮助查找、计划、修改和检查。

术语来源访问日期：2026-07-19。

这个区别不只是换个名字。公开讨论中的 vibe coding 可以指快速试做；受控的 Agent 辅助开发要求每项结论有来源，每项修改能检查，风险操作有人决定是否执行。

## 工作循环

`范围 → 上下文 → 计划 → 最小 patch → 验证 → review → bad case 回流`

先把任务写成一句可验收的话，再列出不能碰的模块和风险。让 Agent 先只读地找入口、调用点、测试、文档和当前 diff。计划应说明会改哪些文件、保留什么行为、怎么验证；没有这些内容，就别进入修改。

修改只做计划内的最小 patch。完成后运行与任务相符的测试或检查，阅读 diff，并由人判断是否接受。失败时不要让 Agent 连续猜修；记录是需求、上下文、工具、代码、测试还是 review 漏了关口，把改进写回任务卡或检查表。

可直接使用的任务卡：

```text
目标：
验收：
范围与禁止修改项：
风险与需要确认的写操作：
只读上下文和来源：
验证命令或人工检查：
```

## 可检查的公开例子：Forge Harness

本仓库的 [Forge Harness 证据索引](../../projects/forge-harness/README.md) 固定在 `9c1b1dbb0566` 快照，访问日期为 2026-07-18。以下是该索引链接到的公开、可检查文件；它们只能支撑列出的结论。

- 已实现：工具注册与分发会拒绝未知工具，并由 [tool runtime tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/tools/toolRuntime.test.ts) 覆盖读取边界。
- 已实现：最小循环会在返回最终回答前执行最终门控；失败时只进行一次恢复尝试，见 [minimal loop tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/core/minimalLoop.test.ts#L1632-L1770)。
- 已实现：异步子会话记录 pending 工作、只返回一次终态通知，并暴露隔离编辑预览的元数据，见 [child-session tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/extensions/childSessions.test.ts)。
- 已提议：外部工具以及 MCP 或插件路由是后续边界，不属于该已实现 checkpoint，见 [c15b next-gap section](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/docs/tutorial/c15b-async-child-sessions-parallel-handoff.md)。
- 未知：这个教程快照没有证明 SaaS 运维、多租户授权、基准性能或生产可靠性。

这些公开文件没有给出节省多少时间、通过率提高多少或减少多少返工。因此它们不是个人效率成果，也不能替代真实项目经历。

## 指标和个人叙事

把下面内容当作测量候选指标，而不是已经得到的结果：任务完成时间、返工率、被 review 拒绝的 patch 比例、回归数量、无关 diff 数量。在方法和原始记录都存在前，这些指标不能用于宣称效果。记录时先定义任务类型、样本期、基线和失败如何计数，并保留命令输出和 diff。

只有实际完成这次练习，才可以说“我按这个流程练习过”。若实际完成了却没有保留可检查的提交、测试输出或记录，应说明证据没有保留，不能补造结果。没有实践时，只描述计划和准备采用的记录方法，不把计划说成经历。

实际执行时使用 [操作检查表](workflow-checklist.md)。
