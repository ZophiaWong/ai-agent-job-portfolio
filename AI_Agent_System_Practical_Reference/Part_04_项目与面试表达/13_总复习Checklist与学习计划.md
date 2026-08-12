# 13_C01–C13 总复习与证据路线

## 1. 这条路线怎么用

这是手册唯一的公开复习路线。它覆盖[C01–C13 核心能力](../../.codex/skills/interview-prep-coach/references/competency-model.md)，用产物推动练习，不用阅读页数代替证据。

路线给出练习块和验收门。每个学习日至少完成一个可检查产物；时间不足就少做一块，不要把两个半成品当成完成。私人目标保存在 `.local/interview-prep/`，私人日程由里面的教练状态按现实可用时间安排，不写入公开文档。

默认顺序：冷启动 → 澄清约束 → 独立作答/编码 → 执行或检查 → 解释权衡 → 迁移题 → 延迟复测。

## 2. 2–3 周 C01–C13 证据路线

### 第1周：代码、Agent 边界与 RAG 诊断

| 学习日任务 | 覆盖能力 | 可检查产物 |
|---|---|---|
| 独立完成一道 Python 调试题和一道 DSA 迁移题，执行边界 case | C01、C12 | 代码 `python-dsa-evidence.py` 与运行记录 `python-dsa-output.txt` |
| 为结构化输出设计 schema、错误边界和服务端校验 | C02 | 设计 `llm-boundary.md` 与 schema `response-schema.json` |
| 限时画一个有状态 Workflow，标出循环、终止、重试和恢复 | C03 | 设计 `agent-workflow-design.md` |
| 为一个有副作用的工具定义权限、幂等、审批和审计 | C04、C08 | 工具契约 `tool-contract.json` 与状态设计 `approval-state.md` |
| 对一个 RAG bad case 分离入库、召回、上下文和生成问题，写回归样例 | C05、C06 | 诊断 `rag-bad-case.md` 与评测数据 `rag-eval.json` |

周验收：随机抽一个旧任务重做，新建 `week-1-delayed-retest.md`。如果无法在不看原答案的情况下解释失败原因，不记为通过。

### 第2周：后端、系统设计与项目事实

| 学习日任务 | 覆盖能力 | 可检查产物 |
|---|---|---|
| 设计 FastAPI 请求、取消、超时、持久化和错误边界，执行一个最小测试 | C07 | 代码 `api-boundary.py` 与测试输出 `api-test-output.txt` |
| 限时完成一道 Agent/RAG 系统设计，先问规模、SLO、数据和风险 | C09 | 设计 `timed-system-design.md` |
| 深挖 MeterDesk，逐条区分 implemented、planned、proposed improvement 和 unknown | C10 | 项目证据 `meterdesk-project-evidence.md` |
| 追踪 Forge Harness 的一次 runtime 或权限路径，引用具体源码/测试 | C10、C11 | 项目 trace `forge-runtime-trace.md` |
| 不看稿完成一次自我介绍和一道行为题，只保留可核对事实 | C13 | 冷答 `career-cold-answer.txt` |

周验收：把系统设计中的两个主张指向代码、设计记录或项目证据，写入 `week-2-claim-audit.md`。无证据的句子改为练习设计或待验证提案。

### 第3周：可选的综合模拟与延迟复测

| 学习日任务 | 覆盖能力 | 可检查产物 |
|---|---|---|
| 从 Chapter 12 抽题，完成一次不看参考区的技术冷答，然后做迁移题 | C02–C09 | 冷答 `technical-cold-answer.md` 与迁移记录 `transfer-answer.md` |
| 重做 Python/SQL/DSA 中最弱的一项，不复制首周代码 | C01、C12 | 代码 `delayed-code-retest.py` 或 `delayed-sql-retest.sql` |
| 完成一次项目深挖模拟，要求面试官追问权衡、失败和个人决策 | C10、C11、C13 | 模拟记录 `project-mock.md` |
| 完成一次综合技术模拟，保留未答出、被提示和修正的地方 | C01–C13 | 模拟记录 `full-technical-mock.md` 与弱点 `mock-gaps.json` |

周验收：将模拟中的一个失败变成回归任务，保留 `mock-regression.md`。未暴露失败的模拟不自动视为高质量证据。

## 3. 证据门槛

产物进入个人能力记录前，逐项检查：

- 能否打开、运行或按步骤复现；
- 是否保留了原始错误、输出、trace 或证据链接；
- 是否记录了约束、权衡和一个失败模式；
- 是否来自独立作答、编码、设计、项目核对或模拟，而不是抄写章节内容；
- 个人项目主张是否与[项目证据索引](../../projects/README.md)一致。

任何一项不满足，就把产物留在练习区，先修正，不用“看过”或“大概会”替它升级。

## 4. 快速入口

- 查能力定义和目标等级：[C01–C13 核心能力](../../.codex/skills/interview-prep-coach/references/competency-model.md)。
- 找系统设计练习：[Chapter 11](11_项目设计模板与架构表达.md)。
- 做冷答：[Chapter 12](12_高频面试题与答题闭环.md)。
- 找代码骨架：[Chapter 16](../Part_05_框架专项与实战Lab/16_端到端实战Lab与代码骨架.md)。
- 核对 MeterDesk 和 Forge Harness：[项目证据索引](../../projects/README.md)。
