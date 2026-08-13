# 中国大陆 0–2 年 Agent 岗位需求与双项目匹配报告

调研日期：2026-08-10

目标市场：北京、上海、深圳、杭州、广州

评估项目：[MeterDesk](https://github.com/ZophiaWong/meter-desk/tree/f9dee13)、[Forge Harness](https://github.com/ZophiaWong/forge-harness/tree/a0146b2)

## 结论

这两个项目适合主投 Agent，但要分成两条简历叙事。

第一条是 AI Agent / 大模型应用工程师。MeterDesk 放在前面：它有明确业务入口、受控工具、人工审批、审计和 Eval Lab，能证明候选人不只会接模型 API。Forge Harness 放在后面，用来解释工具权限、上下文、Trace、验证和多 Agent 协调为什么这样设计。

第二条是 Agent Platform / Runtime / Coding Agent 工程师。Forge Harness 应该成为主项目。它直接覆盖 TypeScript Runtime、MCP、上下文压缩、Session Trace、Worktree 隔离、TaskGraph、teammate 协调、CompletionGate 和离线行为回归。MeterDesk 作为配套案例，证明底层机制可以进入一个有审批和业务状态的产品。

AI 平台后端可以投，但要避开 Java 强绑定岗位。AI 产品全栈也能投，MeterDesk 的契合度不错，不过这条路线没有充分利用 Forge Harness 的技术深度，不适合作为组合的主身份。

两个项目现在就能支撑投递。主要短板不是“缺一个 Agent 框架”，而是缺少公开在线运行、真实用户或负载数据，以及 RAG、云原生部署、生产稳定性指标等招聘方常问的证据。补强时不要把 MeterDesk 改造成 RAG 项目，也不要把 Forge Harness 硬扩成分布式平台。

## 样本和口径

本次收集 40 条仍可访问的社招岗位，明细见 [`data/2026-08-jd-samples.csv`](data/2026-08-jd-samples.csv)。样本按职责分类，不按职位名称机械归类。

| 岗位簇 | 样本数 | 用途 |
| --- | ---: | --- |
| AI Agent / 大模型应用 | 18 | 主投方向，观察业务落地、Agent 编排和模型集成要求 |
| Agent Platform / Runtime / Coding Agent | 12 | 主投方向，观察框架、工具、上下文、评测和可靠性要求 |
| AI 平台后端 | 6 | 备选方向，观察语言、API、数据库和系统设计要求 |
| AI 产品全栈 | 4 | 机会型方向，观察端到端产品交付要求 |

城市分布为北京 7 条、上海 8 条、深圳 8 条、杭州 9 条、广州 8 条。经验字段中，36/40（90.0%）标为“1–3 年”，3/40（7.5%）为“经验不限”，1/40（2.5%）为“1 年以内”。“1–3 年”是招聘平台的常用分桶，只与本报告的 0–2 年目标部分重叠。明确要求 3 年以上的岗位没有进入统计。

学历字段中，本科或统招本科占 32/40（80.0%），硕士 4/40（10.0%），大专 3/40（7.5%），学历不限 1/40（2.5%）。这说明项目能帮助通过技术面，但不能替代多数岗位的学历筛选。

来源质量并不均匀：2/40 是完整详情页，24/40 是招聘列表正文，14/40 来自搜索摘要。BOSS 详情页会触发安全页，猎聘也偶尔出现验证码。报告中的频率是“可见字段命中率”，应该当作下限。某项没有出现在摘要里，不等于公司不要求它。

## 市场需求画像

### AI Agent / 大模型应用

18 条样本里，业务场景落地出现 11/18（61.1%），任务规划、工作流或编排出现 10/18（55.6%），工具调用、MCP 或 Skill 出现 8/18（44.4%）。上下文或记忆、多 Agent、RAG 各出现 4/18（22.2%）。

招聘方要的通常是能把模型接进业务流程的人。岗位会写 LangChain、Dify、Coze、RAG 或某个模型 API，但框架名不是核心。真正反复出现的是：拆任务、接工具、维护上下文、处理业务数据，并把结果放进可测试、可交付的产品。

MeterDesk 对这类岗位的匹配度最高。它从 billing ticket 开始，Agent 读取 invoice、charge、credit、usage 和 policy evidence，后端决定 eligibility 与金额，模型负责受限规划和草稿，高风险动作进入人工审批。这个故事比“做了一个聊天机器人”更接近岗位里的业务落地要求。

缺口也很明确：RAG 在 4/18 的可见描述中出现，而 MeterDesk 明确不做 pgvector 或大规模 RAG。投递 RAG 权重很高的岗位时，应把它列为能力缺口，不要把显式 policy lookup 改写成 RAG。

### Agent Platform / Runtime / Coding Agent

12 条样本里，平台、框架或 Runtime 出现 9/12（75.0%）；工具、MCP 或插件出现 5/12（41.7%）；多 Agent 和评测/回归各出现 4/12（33.3%）；任务规划以及上下文/记忆各出现 3/12（25.0%）。

这一类岗位数量少，标题也很乱。样本中既有 Agent SDK、OpenHarness、MCP Tools，也有 AI Native 引擎、Agent PaaS、Harness 和模型评测。共同点是招聘方希望候选人理解 Agent 执行过程，而不是只会使用上层框架。

Forge Harness 与这组要求高度重合。它有明确的 `allow / ask / deny` 权限决策、Tool Runtime、上下文投影与压缩、Session Trace、验证恢复、Git Worktree 隔离、MCP/插件信任、TaskGraph、teammate mailbox 和 CompletionGate。代码和测试能解释每个机制解决了什么失败，而不是把多 Agent 当成流程图名词。

这里最需要克制包装。Forge Harness 是本地 TypeScript Runtime，不是托管平台。它没有 crash-safe resume、跨运行幂等、分布式 worker、操作系统沙箱、高可用或 hosted control plane。简历可以写“实现了本地受治理 Runtime 和完成协议”，不能写“构建了生产级分布式 Agent 平台”。

### AI 平台后端

6 条对照样本里，业务或模型场景集成出现 4/6（66.7%），Java 出现 3/6（50.0%）。其余样本分别偏向 TypeScript/Node.js 或未披露语言。岗位仍然看 API、数据库、系统设计、上线和问题排查，只是服务对象换成了模型或 Agent。

MeterDesk 可以证明 FastAPI、Postgres、JWT/RBAC、幂等、事务一致性、数据库并发测试和容器化。问题在于不少国内后端岗位绑定 Java/Spring Boot。对这种 JD，项目能证明后端设计能力，却不能替代 Java 经验。优先投 Python、TypeScript 或语言开放的 AI 后端岗位。

### AI 产品全栈

4 条样本都要求端到端业务产品交付。技术栈差异很大：有 React + Spring Boot，也有 Node.js/TypeScript 和未限定框架的 AI Native 全栈。这个方向看的是能否把模型能力、后端状态和用户界面做成一条完整路径。

MeterDesk 的 Next.js、FastAPI、Postgres、Workbench、Approval Queue 和 Eval Lab 可以直接支撑这类投递。Forge Harness 能补充底层理解，但它没有 Web UI，不应被包装成全栈产品。

## 项目证据对照

证据等级采用四档：已验证直接证据、直接实现证据、相邻证据、缺口。这里的“已验证”指仓库有相应实现和可审查测试或运行证据，不代表生产环境 SLA。

| 招聘要求 | MeterDesk | Forge Harness |
| --- | --- | --- |
| 业务 Agent 端到端落地 | 已验证直接证据：Ticket Workbench、受控调查、审批与 Eval Lab | 相邻证据：Runtime 可支持应用，但没有领域产品层 |
| 工具调用与权限治理 | 已验证直接证据：后端拥有工具和金融动作边界 | 已验证直接证据：`allow / ask / deny`、Tool Runtime、MCP policy |
| 任务规划与编排 | 已验证直接证据：LLM 规划、后端 verifier、确定性 decision | 已验证直接证据：模型循环、工具调度、TaskGraph 和 CompletionGate |
| 上下文与记忆 | 相邻证据：保存业务 evidence 与 Trace，但没有通用记忆系统 | 已验证直接证据：prompt assembly、bounded observation、compaction；没有长期记忆 |
| 多 Agent 协作 | 缺口：产品是受治理的单 Agent 工作流 | 已验证直接证据：child Sessions、teammates、mailbox、TaskGraph |
| MCP / Skill / 插件 | 缺口：仅保留未来 adapter 边界，当前没有 MCP server | 已验证直接证据：MCP adapter、plugin preflight、Session trust、skills |
| Human-in-the-loop | 已验证直接证据：退款/credit 审批门、RBAC、原子执行 | 已验证直接证据：变更与插件信任审批、Leader review、edit-plan approval |
| Trace 与审计 | 已验证直接证据：Agent run、tool、policy、approval、mutation、workflow transition | 已验证直接证据：Session metadata、append-only Trace、Git 与任务 evidence |
| Agent eval | 已验证直接证据：结果、证据、policy、审批路由和终态的确定性评分 | 已验证直接证据：13 次行为批次、版本 baseline 和非补偿式回归规则 |
| RAG / 向量检索 | 缺口；产品规格明确排除大规模 RAG | 缺口；Runtime 边界明确排除 RAG 与向量数据库 |
| 后台执行与恢复 | 缺口：P0-04 仍未实现，当前调查在请求生命周期内执行 | 缺口：没有 crash-safe resume、Attempts 或 reconciliation |
| 云原生与生产规模 | 直接实现证据：Docker/Compose/CI，但没有云部署、K8s 或真实负载指标 | 缺口：本地 CLI Runtime，没有 hosted control plane |

Forge Harness 的第一份可比较离线回归报告是 `REGRESSED`，不能写成“回归全部通过”。可以写：项目建立了固定场景、版本基线和非补偿式比较规则，并保留了 compaction ordering 下降的红色结果，没有重复采样到绿色为止。这个事实反而适合在面试中说明评测诚信。

MeterDesk 也有必须守住的边界。P0-04 Async Agent Runtime、provider resilience、observability、networked mock tool boundary 和 structured context 仍是缺口或后续工作。简历不能把 roadmap 当成当前能力。

## 投递组合

| JD 特征 | 主项目 | 辅助项目 | 开场重点 |
| --- | --- | --- | --- |
| Agent 应用、业务工作流、LLM 集成 | MeterDesk | Forge Harness | 先讲 ticket、evidence、decision、approval、eval，再讲底层工具治理 |
| Agent Runtime、MCP、Coding Agent、上下文 | Forge Harness | MeterDesk | 先讲 Runtime-owned invariants，再说明这些机制如何落到受监管业务 |
| AI 平台后端、Python API、状态与审计 | MeterDesk | Forge Harness | 先讲事务、幂等、RBAC、Postgres 测试，再讲执行边界与验证 |
| AI Native 全栈、Agent 产品工程 | MeterDesk | Forge Harness | 先演示完整产品路径，再用 Forge 解释 Agent 机制 |
| Java/Spring AI 后端 | 两者都只能作辅助 | 无 | 只有具备独立 Java 证据时再主投 |
| RAG/知识库占核心比重 | 两者都不完全匹配 | 无 | 诚实说明缺口，不把 policy lookup 冒充 RAG |

两个项目不要在同一份简历里重复写“做了工具调用、多 Agent、eval”。MeterDesk 负责回答“为什么这个 Agent 产品可信”；Forge Harness 负责回答“Runtime 如何阻止未经验证的完成和未经授权的动作”。

## 包装建议

### 项目标题和一句话

MeterDesk：`Governed Agent Billing Support Workbench`

> 使用 Next.js、FastAPI 和 Postgres 构建的账单支持工作台；Agent 通过后端受控工具调查证据，高风险退款或 credit 必须经过人工审批，结果和执行路径进入离线评测。

Forge Harness：`TypeScript Coding-Agent Runtime with Governance, Isolation, and Evals`

> 从零实现的 TypeScript coding-agent Runtime，覆盖工具权限、上下文压缩、Session Trace、验证恢复、Worktree 隔离、MCP/插件信任、多 Agent 协调和完成门。

### 面向应用 Agent 岗的简历要点

MeterDesk 可以使用以下信息组织 bullet，数字应只引用仓库中已有测试或固定样本：

- Built a ticket-first billing support workbench with Next.js, FastAPI, and Postgres; the agent gathers billing and policy evidence through permission-scoped tools and routes mock financial actions to human approval.
- Implemented server-owned RBAC, idempotent workflow commands, row-locked approval decisions, and atomic workflow/approval/mutation/trace writes; verified rollback and concurrency behavior against Postgres.
- Designed an offline Eval Lab that scores outcome, required evidence, policy citation, approval routing, and workflow terminal state with deterministic checks.

Forge Harness 在这份简历中保留一到两条：

- Built a TypeScript coding-agent Runtime with explicit tool policy, bounded context projection, append-only Session Trace, and verifier-gated completion.
- Implemented MCP/plugin trust and isolated child/teammate workflows with Git Worktrees, TaskGraph evidence, verification receipts, and CompletionGate invariants.

### 面向 Runtime / Coding Agent 岗的简历要点

Forge Harness 放在第一位：

- Built a TypeScript coding-agent Runtime where model completion is treated as a candidate until permission, pending-work, TaskGraph, Git-integration, and verifier obligations pass.
- Implemented bounded observations and repeated context compaction while keeping the original task pinned and Session Trace separate from the model's current decision view.
- Added Worktree-isolated child Sessions and long-lived teammates with actor-owned evidence, review, source fingerprints, exact verification commands, Git receipts, and a cross-system CompletionGate.
- Built a 13-attempt offline behavioral regression suite with versioned experiment identity and non-compensating assertion counts; retained the first comparable regressed result for auditability.

MeterDesk 只保留能证明业务使用价值的 bullet：

- Applied governed-tool, human-approval, audit-trace, and deterministic-eval patterns to a full-stack billing support workflow.

这些 bullet 是信息结构，不是最终简历成稿。正式使用前应按目标 JD 压缩到每个项目两至三条，并再次核对数字。

## 补强优先级

### 现在就做：包装和可访问证据

1. 在求职组合仓库做一个双项目入口页，提供两条投递路径：Applied Agent 与 Agent Runtime。
2. 为两个项目各准备一个 90 秒录屏和一张架构图。录屏要展示失败边界，不要只展示成功页面。
3. 把所有简历 claim 链接到具体测试、Trace、截图或 regression report。没有证据的形容词删掉。
4. 对外统一说明 seeded demo、live model run、deterministic smoke 和 offline behavioral eval 的区别。

### 下一轮工程工作

1. MeterDesk 按现有路线完成 P0-04 Async Agent Runtime，再做 provider resilience 与 observability。这个顺序正好补招聘中反复出现的进度、重试、失败恢复和运行可见性，但不能提前写进简历。
2. 给 MeterDesk 增加可复现的延迟、失败恢复和并发证据，避免使用“高性能”“生产级”这类没有数字的词。
3. Forge Harness 先处理五个超过 1,000 行模块的维护压力，保留行为与 Trace 语义，再考虑是否批准 crash-safe resume 或 hosted 方向。不要绕过课程边界直接堆分布式组件。
4. 如果目标 JD 把 RAG 当作硬门槛，单独做一个小而可评测的检索项目或实验。不要把 RAG 塞进 MeterDesk，也不要改写 Forge Harness 的 Runtime 边界。

### 不建议投入

- 为匹配关键词同时接入多个 Agent 框架。当前项目已经能证明机制理解。
- 把 mock mutation 改成真实支付。它会引入新的合规和运维风险，却不会解决当前求职证据的主要缺口。
- 为了“多 Agent”标签改造 MeterDesk。Forge Harness 已经承担这部分证明责任。
- 声称高可用、低延迟、生产安全、分布式协调或大规模用户验证，除非后续有可复现数据。

## 可用与不可用的 claim

可以直接使用：

- MeterDesk 是 ticket-first、approval-gated、trace-aware 的 Agent 产品。
- MeterDesk 的后端拥有工具执行、确定性决策、审批和 mock mutation 权限。
- Forge Harness 实现了本地 TypeScript coding-agent Runtime、MCP/插件信任、Worktree 隔离、多 Agent 协调和 verifier-gated completion。
- 两个项目都有确定性测试和行为/治理评测证据。

验证后再使用：

- 当前分支的精确测试数量、CI 状态、容器 smoke 结果和运行耗时。
- 任何延迟、吞吐、token、成本或失败恢复数字。
- 在线 demo 的可用性和部署环境。

不能使用：

- 生产级支付、真实客服集成、自动发送客户回复。
- MeterDesk 已有异步 worker、crash recovery、MCP server、RAG 或多 Agent Runtime。
- Forge Harness 已有分布式 worker、操作系统沙箱、高可用、跨运行恢复或 hosted control plane。
- Forge Harness 的模型行为回归已经全部通过。

## 来源与限制

所有入样岗位、访问日期、页面粒度和项目证据映射都在 [JD 样本表](data/2026-08-jd-samples.csv) 中。代表性公开来源包括 [BOSS 北京 AI 开发岗位页](https://www.zhipin.com/zhaopin/4bf879c1368205460nB_39q7Fg~~/)、[BOSS 杭州 AI 开发岗位页](https://www.zhipin.com/zhaopin/2265e608aefd780f0nF62t24Fw~~/)、[BOSS 广州 AI 开发岗位页](https://www.zhipin.com/zhaopin/694c682c6021630e0nB82Nu-FQ~~/)、[绿联 AI Agent 前端开发完整 JD](https://www.liepin.com/job/1983680297.shtml) 和 [申通 React + Java + AI Agent 全栈 JD](https://www.liepin.com/job/1981454911.shtml)。

这不是招聘市场普查。平台搜索排序、反爬和登录墙会影响可见内容，岗位也会随时关闭。报告没有统计薪资，没有评价公司质量，也没有结合候选人的学历、实习和工作经历。后续投递时应重新打开目标 JD，并以当日正文为准。
