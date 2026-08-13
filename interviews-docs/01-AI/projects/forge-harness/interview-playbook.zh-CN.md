# Forge Harness 面试 playbook

> 用途：用于简历投递前压缩项目表述、面试前复习和现场 screen-share。技术路径均相对于 Forge Harness 仓库根目录。这里记录的是当前事实和可说的边界，不替代公开仓库中的 `README.md`、`docs/evidence-index.md` 或 case study。

## 使用前先校准口径

Forge Harness 是一个从零构建的 TypeScript coding-agent Runtime。它从一个可运行的 model-tool loop 开始，经过 22 个 runnable checkpoint，逐步加入工具治理、上下文管理、持久化运行证据、隔离委派、扩展信任和 c17c 协作完成协议。

本页把面试演示分成两种性质不同的模式。

| 模式 | 命令 | 适合的场景 | 能说明什么 | 不能说明什么 |
| --- | --- | --- | --- | --- |
| Deterministic | `npm run demo:portfolio -- --explain` | 正式 screen-share 的主线 | 三个固定 Runtime 边界在本地可重复检查 | 真实模型会稳定选择同一条工具路径 |
| Focused Live LLM | `npm run demo:portfolio:live` | 受控的私下面试 screen-share，且环境已经准备好 | 一次真实模型运行能否到达固定 fixture 的 Runtime 证据边界 | 可重复性、通用 coding 能力或生产稳定性 |

`demo:portfolio:live` 当前位于 Forge 的 `codex/add-recruiter-portfolio` 分支。在它合并前，不把它说成 `main` 上已经发布的能力。它不进入 CI，只适合受控的私下 screen-share，不能录制或作为公开证据。

Compaction P0 仍然开放。公开的独立比较证据只记录了 `compaction-retention` 从 baseline 的 `3/3` 到 candidate 的 `2/3`，且这个红色 candidate 已冻结、没有为了绿色结果重新抽样。源码提交 `a0146b2` 已处理 repeated compaction 的 summary rollover，并补了连续 compaction 测试；这不是 post-fix independent comparable candidate，也不是 P0 关闭证明。

## 简历中的项目表述

### 中文标题与三条 bullets

**Forge Harness | 从零构建的 TypeScript coding-agent Runtime**

- 从最小 model-tool loop 演进为五层 Runtime，覆盖工具执行、权限治理、有界 context、Session/Trace 证据与 verification/recovery；每个机制保留为可运行 checkpoint。
- 实现 c17c coordination protocol：TaskGraph ownership、teammate plan approval、Worktree-isolated child/teammate、source fingerprint、task verification、Git integration receipt 与 `CompletionGate`。
- 设计五个固定 offline-eval 场景和 13-attempt contract；保留 `compaction-retention` 的 `3/3 -> 2/3` 红色可比较结果，避免为偏好的 verdict 重抽样。

### 英文标题与三条 bullets

**Forge Harness | From-scratch TypeScript coding-agent Runtime**

- Built a five-layer Runtime from a minimal model-tool loop, covering governed tool execution, bounded context, Session/Trace evidence, and verification/recovery through runnable checkpoints.
- Implemented the c17c coordination protocol with TaskGraph ownership, plan approval, Worktree-isolated delegation, source fingerprints, verification, Git integration receipts, and a completion gate.
- Designed five fixed offline-eval scenarios with a 13-attempt contract; retained a comparable `3/3 -> 2/3` compaction regression rather than resampling for a preferred verdict.

简历只放这三条即可。`22 checkpoints` 是作品集或面试里的支撑事实，不需要塞进每一条 bullet。也不要把 `3/3 -> 2/3` 写成“修复已被独立验证”。

## 中文项目介绍

### 30 秒

口述：

> Forge Harness 是我从零构建的 TypeScript coding-agent Runtime。它从最小 model-tool loop 出发，逐步把工具治理、上下文、运行证据、Worktree 隔离和多 Agent 协作做成可检查的 Runtime 机制。当前实现到 c17c：一个 edit task 要经过 ownership、计划或委派、验证、Git integration 和 completion gate，才能让 root run 结束。

如果只剩一句补充，接着说：

> 我保留了每一步的 runnable checkpoint、focused test 和 smoke，所以可以分别讨论机制、失败路径和边界，而不是只展示一个成功截图。

### 90 秒

口述：

> Forge Harness 的起点很简单，模型提出 tool call，Runtime 执行并把结果带回下一轮。后面的问题才更像真实 coding agent：哪些动作可以执行，长对话该给模型看什么，发生过什么怎样复盘，子任务改出的代码怎样隔离和接回主线。
>
> 我把这些问题归到五层。L1 管 model loop 和 tool execution；L2 在 dispatch 前做 permission policy；L3 在 Session 初始化时组装稳定 instructions，并管理 bounded observation、每轮 model input 和 compaction；L4 把 Session、Trace、RuntimeState、verification 做成可检查的运行事实；L5 处理 background work、child、Worktree、TaskGraph 和 team completion。
>
> 当前 c17c 把五层接在一个 edit task 上。长期 teammate 要先提交 plan，Leader 批准后才有协议资格去写；one-shot edit child 则先经过 delegate approval，并在独立 Worktree 内逐次请求写入批准。提交结果后，还要让 Runtime 验证固定 command、比较 fingerprint、生成 Git receipt。`CompletionGate` 会拦住过早的 candidate；Gate ready 后进入 finalization，配置 root verifier 时还须 verifier pass 才写 final。项目明确没有 OS sandbox、崩溃后的 replay/resume/reconciliation 或分布式协调。

### 180 秒

口述：

> 我把 Forge Harness 当作一个从零演进的 Runtime 工程，而不是一个套框架的 agent demo。第一阶段先做真实的 model-tool loop，再把 tool registry、统一 `ToolResult` 和 file editing 拆开。这样后来加权限时，模型不会绕过一个隐藏的 handler 路径。
>
> 第二阶段解决 context 和可观测性。模型下一轮不应该吃完整 raw transcript，所以工具结果先变成有界 `Observation`，历史超过预算时用 compaction summary 交接。与此同时，`trace.jsonl` 保留 append-only 的 Runtime 事实，`RuntimeState` 是当前决策投影。它们职责不同：summary 可以有损，完成相关的事实不能只放在 summary 里。
>
> 第三阶段是隔离和协作。Worktree 把并行编辑和 base checkout 分开；child 有 fresh Session，长期 teammate 有 mailbox。到 c17c，TaskGraph 才成为 ownership 和 protocol 的权威来源。一个 edit task 从 `pending` 到 `completed`，不是模型说 done 就结束：先 assign 或 claim，teammate 的 plan 被 review；在注册的 source Worktree 编辑并交件；`task_verify` 用 contract 中冻结的 command 检查 source；`task_integrate` 创建 source commit、cherry-pick 到 Leader target，并记录 receipt。verification pass 后 task 仍是 `submitted`，只有 integration receipt 才能完成它。
>
> 最后是如何知道这些机制没在看不见的地方退化。我保留 source、focused test、deterministic smoke、经过整理的 live snapshot 和 offline eval 的不同证据层级。一个真实例子是 compaction-retention：固定 13-attempt 比较抓到 ordered reads 从 `3/3` 降到 `2/3`。红色 candidate 被保留而不是重抽样。源码已经补了 repeated-compaction 的处理和测试，但 post-fix 独立 candidate 还没有完成，所以我会明确说 P0 仍开放。面试中要把这层证据状态说清楚。

## c17c 端到端系统故事

这个故事适合在对方问“多 Agent 部分到底做了什么”时使用。先用一张心智图定住角色。

```text
Leader root Session
  -> TaskGraph 记录 contract、owner、revision、evidence、verdict、receipt
  -> long-lived teammate：claim -> submit_plan -> Leader review_plan -> edit
  -> one-shot child：Leader owns task -> delegate(profile=edit) -> isolated child
  -> source fingerprint -> task_verify -> task_integrate -> Git receipt
  -> CompletionGate ready
       -> 未配置 root verifier：final_answer
       -> 配置 root verifier：pass 后才 final_answer
```

### 2 到 3 分钟口述

> c17c 处理 multi-agent 场景中的 ownership、交接和完成条件。TaskGraph 是 root run 内的权威状态：谁拥有 task、contract 是什么、证据由谁提交、结果是否验证和是否集成，都写在这里。
>
> 以 edit task 为例。长期 teammate 的路径是先 claim，再提交 plan。Leader 的 `review_plan(approve)` 只是 TaskGraph 协议门，不等于它拿到永久写权限。真正的 `edit` 或 `write` 仍然走 permission policy，并且执行前会再检查当前 task 状态。one-shot edit child 则不同：Leader 先拥有 task，`delegate(profile=edit)` 经过人工批准后启动一个 fresh child Session。child 不是 TaskGraph owner，每一次文件修改也仍然需要 approval。
>
> child 或 teammate 交件后，Leader 不能相信模型提供的任意 workspace path。Runtime 从注册表解析 source，记录 Git fingerprint，用 task contract 里的 command 验证。如果 verification 通过，task 仍然停在 `submitted`，因为那只能说明 source 在该时刻通过检查。`task_integrate` 再创建 source commit、cherry-pick 到 Leader target，并写入 Git receipt，task 才变成 `completed`。
>
> root 模型即使先给了 candidate，`CompletionGate` 也会先检查 child、teammate、TaskGraph、background work 和 Git 状态。只要有待 verification、待 integration、未 shutdown 的 teammate 或 unread mailbox，它就返回 `incomplete`。所有义务收敛到 Gate ready 后才进入 finalization；如果配置 root verifier，它必须通过，未配置时 loop 直接记录 `final_answer` 与 `session_ended(completed)`。这套协议没有做 crash recovery 或分布式调度，所以发生 Git side effect 后崩溃的 reconciliation 是明确留给后续章节的问题。

### 可以给出的证据入口

| 想证明的点 | 优先入口 | 面试中怎么说 |
| --- | --- | --- |
| TaskGraph ownership 与状态机 | `src/domain/teamTask.ts`、`src/runtime/teamTaskStore.ts`、`test/runtime/teamTaskProtocol.test.ts` | contract、owner 和 revision 都是文件型协议状态，不是 prompt 中的约定。 |
| child 与 teammate 的差异 | `src/extensions/childSessions.ts`、`src/extensions/teammates.ts` | child 是 fresh、one-shot 的执行单元；teammate 是可持续寻址的参与者。 |
| 可信 source 与 Git receipt | `src/runtime/gitIntegration.ts`、`test/runtime/gitIntegration.test.ts` | source 由 registry 解析，verification 和 integration 分开。 |
| 完成条件 | `src/runtime/completionGate.ts`、`test/runtime/completionGate.test.ts`、`npm run smoke:c17c-capstone` | gate 读取各模块 projection，不替它们偷偷改状态。 |

## 三条可选深挖故事

### Permission before dispatch

适合的问题：为什么不让工具 handler 自己检查权限？

口述：

> 我把 permission 放在 dispatch 前，因为副作用一旦进入 handler，再做审计或补救都太晚。模型的 tool call 先进入 `PermissionPolicy`，结果只能是 `allow`、`ask` 或 `deny`。`ask` 才进入 approver，获批后才调用 owning handler。这样 unknown tool、危险 shell shape、越界 edit/write 和外部 MCP 都能走同一条 action boundary。
>
> 这也让测试能检查一个很直接的 invariant：被 deny 的 write 不能增加 handler 的 dispatch count。确定性 demo 的第一 scene 就是这个检查。它不是 OS sandbox。批准后的 plugin hook 仍在当前进程和 host 权限中运行，Worktree 也不隔离网络、credentials 或恶意本地进程。

追问与回应：

| 追问 | 回应要点 |
| --- | --- |
| 为什么 policy 不放在每个 tool 里？ | 规则会分叉，插件和 MCP adapter 更容易绕过。统一边界先做决策，再把执行交给对应 handler。 |
| `allow` 是否代表绝对安全？ | 不代表。它只是 Runtime policy 对已知 inspect action 的决策，不是内核级权限系统。 |
| evidence 在哪里？ | `src/governance/defaultPolicy.ts`、`src/core/minimalLoop.ts`、`test/governance/defaultPolicy.test.ts`、`test/portfolio/demo.test.ts`。 |

### Context 与 Trace 分离

适合的问题：为什么既有 context summary 又要保存 Trace？

口述：

> 这两个对象服务的读者不同。context 是给下一轮模型决策用的，所以需要有界、可以压缩。`Observation` 只保留工具名、状态、摘要和受限内容；compaction summary 可以用来交接较早的对话。Trace 是运行账本，按 Session、sequence 和 timestamp 记录有序 Runtime event，不会因为 prompt 预算缩小而被压缩。
>
> 这区分也约束了完成逻辑。一个 summary 里可能遗漏细节，所以 completion-critical facts 不能只留在模型 context。TaskGraph、RuntimeState 或 Trace 才是 Runtime 要读取的地方。`RuntimeState` 又不是 Trace 的替代品，它只是从事件投影出的当前决策视图，不是可 crash-safe replay 的历史数据库。

追问与回应：

| 追问 | 回应要点 |
| --- | --- |
| 为什么不用完整 transcript？ | 长 session 会不断增加输入；模型需要的是下一步决策所需的有界事实，不是完整原始输出。 |
| compaction 丢事实怎么办？ | 用明确 summary contract、pinned task 和测试降低风险；关键 completion 事实不依赖 summary。 |
| 有 replay/resume 吗？ | 没有。当前 Trace 是 durable evidence，不是 crash-safe event-sourcing/reconciliation 实现。 |

证据入口：`src/context/projection.ts`、`src/context/compaction.ts`、`src/runtime/trace.ts`、`src/runtime/state.ts`、`test/context/compaction.test.ts`。

### Offline eval 发现 compaction regression

适合的问题：你怎样处理一个模型评估变红？

口述：

> 我没有把红色结果当成需要清掉的噪音。offline eval 用五个固定场景组成 13-attempt contract，其中 compaction-retention 要求按顺序读取三个 token、触发自动 compaction，并返回准确组合结果。当前公开比较里 baseline 是 `3/3`，candidate 是 `2/3`，所以 `ordered-reads` 少了一次。比较器不会让别的场景变好来抵消这项下降，报告保持 `REGRESSED`，也不为得到绿色 verdict 重抽样。
>
> 随后的源码检查定位到 repeated compaction 的 summary rollover：第二次 compaction 不能只用新 raw rounds 替换先前 summary。`a0146b2` 让已有 `compacted_context` 进入下一次 source，并补了连续三次 compaction 的测试。这是 source-level 修复和 deterministic coverage。后修复的独立 comparable candidate、promotion 和 P0 closure 仍未完成，所以我不会说回归已经被 eval 证明修复。

追问与回应：

| 追问 | 回应要点 |
| --- | --- |
| 13 attempts 会不会太少？ | 它是固定的行为 contract，不是统计显著性的 benchmark。结果用于发现和比较明确场景的变化。 |
| 为什么不重跑到绿？ | 重抽样会改变 experiment identity，让报告选择性偏向想要的 verdict。只有 provider、evidence 或 config invalid 才有理由处理失效 attempt。 |
| eval 能证明什么？ | 固定 identity 下的行为计数与 hard invariants。它不证明通用 coding 能力、生产稳定性或 deterministic model reasoning。 |

证据入口：`docs/offline-eval.md`、`docs/assets/evidence/offline-eval-regression-report.md`、`src/eval/`、`test/eval/`、`src/context/compaction.ts`。

## Deterministic 3 分钟 screen-share

### 开始前

在面试前完成依赖安装和 build，不把等待 package registry 的时间放进视频或现场主线。准备环境是 Linux、macOS 或 WSL2，Node.js `>=20.19`、Git 和 Bash。

```bash
npm ci
npm run build
git status --short
```

`npm ci` 可能访问 package registry。演示命令本身不调用模型、不读取 `.env`、不访问网络。开始 screen-share 后只运行：

```bash
npm run demo:portfolio -- --explain
```

它会创建并清理临时 Git repository/Worktree。三个 scene 彼此独立，不能说成一次连续的 live Session。

### 时间线与旁白

| 时间 | 屏幕上的动作 | 口述重点 |
| --- | --- | --- |
| `0:00-0:20` | 显示 `README.md` 首段或 `PORTFOLIO.zh-CN.md` 五层表 | “这是从 minimal loop 演进到 c17c 的 Runtime。下面三个 scene 不是完整能力清单，而是三个可重复的边界检查。” |
| `0:20-0:35` | 输入命令 | “这个命令不使用模型、`.env` 或网络，因此面试时它给的是稳定基线；真实模型演示是后面的可选扩展。” |
| `0:35-1:00` | 指向 `scene.action-boundary` 和对应 explain 行 | “一个 write request 在 policy 被 deny，dispatch count 是 0。重点不是它被拒绝，而是 handler 根本没开始执行。” |
| `1:00-1:35` | 指向 verification scene | “scripted candidate 先触发真实 verification loop。第一次失败后 Runtime 注入 recovery；第二次通过才接受 final。” |
| `1:35-2:25` | 指向 coordination scene | “这个 scene 按 c17c 顺序给出 task/plan、Worktree 写入、early incomplete gate、fingerprint、verification、integration receipt 和 ready gate。” |
| `2:25-2:45` | 打开 `src/portfolio/demo.ts` 或 `test/portfolio/demo.test.ts` | “这些短 receipt 来自实际 scene，测试固定了事件顺序。” |
| `2:45-3:00` | 回到 `docs/evidence-index.md` 或 `npm run smoke:c17c-capstone` 的命令位置 | “如果需要更完整的 c17c 闭环，smoke 覆盖 TaskGraph、Git integration 和 CompletionGate。模型行为仍然需要和 deterministic smoke 分开看。” |

本次输出应有以下稳定内容：

```text
scene.action-boundary PASS deny-before-dispatch
scene.verification-recovery PASS recovery-before-final
scene.coordination-completion PASS receipt-before-ready
explain.action-boundary policy=denied dispatches=0
explain.verification-recovery verification=failed recovery=attempted verification=passed final=accepted
explain.coordination-completion task=approved gate=incomplete worktree=written fingerprint=captured verification=passed integration=recorded gate=ready
```

### 静态 evidence fallback

如果 screen-share 终端不可用，不现场修环境。直接转到以下静态入口：

1. `src/portfolio/demo.ts`：三个 scene 从哪里运行，receipt 如何从真实执行结果提取。
2. `test/portfolio/demo.test.ts`：默认输出、`--explain` 输出顺序和脱敏约束。
3. `test/smoke/c17cCapstone.test.ts`：无模型的 c17c TaskGraph、verification、Git receipt 与 ready gate 闭环。
4. `docs/evidence-index.md`：不同 claim 分别由 source、focused test、smoke、live snapshot 或 eval 支撑。

一句切换话术：

> 我不会在面试中花时间排查终端。这里的主张有 deterministic test 和 source evidence，我先用它们把控制流讲清楚；Live 模式只在环境已经准备好时再展示。

## Focused Live LLM 5 到 8 分钟 walkthrough

### 先确认是否值得运行

满足以下条件才运行。缺任何一项就不启动。

- 当前 checkout 是包含该命令的 `codex/add-recruiter-portfolio` 分支或其后续合并结果。
- 有 interactive TTY、Git、Bash、Node.js `>=20.19`。
- Forge 根目录 `.env` 已显式配置 `OPENAI_API_KEY` 和 `OPENAI_MODEL`；可选 `OPENAI_BASE_URL` 已按 provider 要求配置。
- 已接受本次调用可能使用网络和 provider token，也接受模型可能失败。
- 已确认这是一次受控的私下 screen-share，不录制、不把 transcript 或截图保留为公开证据；失败时不会现场排查。

Live child 使用 `stdio: "inherit"` 直接继承当前 terminal，因此屏幕上可能出现可变的 model/tool text、provider failure 和 Runtime path。它只能用于受控的私下 screen-share，绝不录制，也不把 transcript、截图或结果当作公开 evidence。如果出现意外的敏感值、绝对路径或错误内容，立刻停止共享或中断命令，改用 deterministic walkthrough。不要 `cat .env`，不要共享 API key。

命令读取 Forge 根目录 `.env`，并把模型过程交给现有 CLI。wrapper 只在原始 Runtime transcript 前后打印少量 `[demo]` 说明，不打印内部 reason、环境值、API key、authorization header、raw exception、raw Trace 或绝对临时路径；这不代表 inherited terminal 已经被整体脱敏。

```bash
npm run demo:portfolio:live
```

### fixture 和 Runtime 路径

Live 命令通过 `fs.mkdtemp()` 在系统临时目录现场生成独立 Git fixture，不复制模板、不解压文件，也不依赖外部仓库。它不加载当前项目的 plugin/MCP 配置，也不修改 Forge checkout。fixture 是无外部依赖的小 Node 项目：

- `.gitignore` 提交 `.forge/`，避免 Session 文件让 fixture 在 root Worktree 创建前变成 dirty；
- `src/errors.mjs` 定义 transient/permanent error，`src/retry.mjs` 包含有意留下的 retry-policy 缺陷；
- `node:test` 检查首次成功只调用一次、transient failure 重试后成功、`maxAttempts` 是总执行次数、permanent failure 立即停止；
- 初始 `npm test` 必须失败；
- 成功、失败、中断或超时后都会尝试清理临时仓库。

模型收到自然的 coding task 和最小 c17c 约束，没有拿到 bug 原因、文件定位、代码答案、task ID、标题、acceptance、tool 参数或逐步调用脚本。演示只固定一个 edit task 和一个同步 `profile=edit` child，以控制面试时长、协作拓扑和证据归属；这不是 Runtime 的能力上限。模型自行决定 task 文案、阅读哪些文件、怎样修改 `src/**`、编辑次数和具体 protocol call 顺序。

Child 负责阅读与修改，不具备 Bash。Leader 使用 child 的注册 source 提交结果，在该 source 上通过 `task_verify` 运行 `npm test`，再用 `task_integrate` 记录 Git receipt。集成后，根级 verifier 再运行一次 `npm test`，`CompletionGate` 控制 finalization。

### Evidence validator 要求的四类 protocol approval

下面四项是 `validateLivePortfolioEvidence()` 要求存在的协议审批类别。它们不是一次 Live run 中全部可能出现的审批。

| 顺序 | 动作 | 为什么需要 approval | 应讲的重点 |
| --- | --- | --- | --- |
| 1 | `delegate(profile=edit)` | 要启动有写入能力的隔离 child | 这批准的是创建 child，不是批准全部后续写入。 |
| 2 | child 的 `edit` 或 `write` | 实际修改 fixture 文件 | 每一次文件 mutation 仍回到 child 的 permission/approver。 |
| 3 | `task_verify` | 在注册 source Worktree 中运行 contract command | verification command 由 task contract 冻结，不能临时换成更容易通过的命令。 |
| 4 | `task_integrate` | 创建 source commit 并 cherry-pick 到 Leader target | pass 只证明 source；receipt 才证明改动已进 target。 |

child 的 `edit`/`write` 可以有一次或多次，具体 mutation 数量可变，每次 mutation 都要逐次审批。固定的是 action boundary 和 validator 要求的四类 protocol approval，不是总审批次数。

### 5 到 8 分钟时间线

| 时间 | 操作 | 讲解 |
| --- | --- | --- |
| `0:00-0:30` | 说明这是一条 optional Live path | “前面的 deterministic demo 是主线。这里用一次真实模型运行检查同一个项目中的 focused c17c path。” |
| `0:30-1:00` | 运行命令，说明 wrapper 已先检查 fixture 的初始红测 | “这是现场生成的 retry-policy 小项目，测试把总尝试次数和可重试错误边界写清楚。初始红测是启动模型前的前置检查。” |
| `1:00-3:30` | 逐次审批 delegate 与 child mutation | “Runtime 先批准具体动作，再执行。child 在独立 Worktree，Leader 不相信模型自己报的 workspace path。” |
| `3:30-5:30` | 审批 `task_verify` 与 `task_integrate` | “两步分开。source 先跑 `npm test`，fingerprint 没 drift 才能整合；Git receipt 使 target 的事实可以被检查。” |
| `5:30-6:30` | 观察 wrapper 的最终说明 | “wrapper 读取 root Trace 和 TaskGraph，语义核对唯一 completed edit task、同步 child source、manual approvals、fingerprint、verification、Git receipt、root final 和 completed Session。它不另造 Runtime event。” |
| `6:30-8:00` | 如果对方继续追问，打开 `src/portfolio/live.ts` | “这里验证的是一个临时 fixture 的证据边界，不验证模型 reasoning，也不把这次结果升级为长期开源 evidence。” |

### 失败切换话术

| 发生什么 | 现场回应 |
| --- | --- |
| 缺少凭据或 interactive terminal | “这个模式刻意要求已准备好的交互环境。我切回 deterministic walkthrough，它覆盖同样的 Runtime 边界且不依赖 provider。” |
| provider 或模型 child 失败 | “这是 variable Live path 的预期风险，不在面试中调试。静态的 source、tests 和 deterministic demo 才是这次解释的基础。” |
| approval 被拒绝 | “拒绝本身说明 action boundary 生效。这次 live run 应按非零状态退出并清理 fixture，我不会把它当成功证据。” |
| 出现意外的敏感值、绝对路径或 provider/Runtime error | “我现在停止共享或中断命令，不保留这段输出。接下来切回不读取 `.env`、不调用模型的 deterministic walkthrough。” |
| 收到 `SIGINT`/`SIGTERM` | “wrapper 会把中断传给 child 并清理临时仓库。接下来直接回到 deterministic 命令。” |
| 超过 10 分钟 | “launcher 会先发 `SIGTERM`，两秒后仍未退出再发 `SIGKILL`，然后清理 fixture。我现在切回 deterministic walkthrough。” |

## 25 道核心题

### L1 Loop & Execution

| 问题 | 回答锚点 |
| --- | --- |
| 1. 为什么先做最小 model-tool loop？ | 先把模型请求、function call、tool result 和下一轮输入的闭环做真实，后续边界才能插入具体位置。 |
| 2. `ToolResult` 为什么是统一类型？ | 让 built-in、MCP 和插件动作返回统一的 status、summary、content 与 metadata，避免 core loop 认识每个工具细节。 |
| 3. unknown tool 如何处理？ | fail closed，不能因为模型给出一个名字就路由到任意实现。 |
| 4. 为什么一轮只处理一个 tool call？ | 教程优先选择可观察的控制流，代价是复杂任务可能增加 round 数。 |
| 5. candidate 和 final 为什么分开？ | candidate 只是模型当前回答；final 要等 pending work 收敛、`CompletionGate` ready，配置 root verifier 时还要通过 verifier。 |

### L2 Governance & Action Boundary

| 问题 | 回答锚点 |
| --- | --- |
| 6. permission policy 在什么位置？ | `ToolRuntime.execute()` 前，policy 决策和必要的 approver 都完成后才 dispatch。 |
| 7. `allow`、`ask`、`deny` 各代表什么？ | Runtime 对当前调用的执行决定；`ask` 是显式人类动作，`deny` 不进入 handler。 |
| 8. 为什么 MCP annotations 不足够？ | 外部 metadata 不能替代本地 Runtime 的统一 policy，MCP tool 仍要经过 Forge action boundary。 |
| 9. path boundary 防的是什么？ | file tool 不能把模型提供的相对路径悄悄解释成 checkout 之外的目标。 |
| 10. 这是否等于 sandbox？ | 不是。它是进程内治理；host 权限、网络、credentials 和恶意 local process 都没有隔离。 |

### L3 Context & Knowledge

| 问题 | 回答锚点 |
| --- | --- |
| 11. 为什么不把 raw tool output 全回填？ | 大输出会耗尽输入预算；`Observation` 留模型下一步确实需要的有界内容。 |
| 12. prompt assembly 与每轮 model input 分别包含什么？ | `assemblePrompt()` 在 Session 初始化时从 task 和 prompt assets 组装稳定 instructions；每轮 `modelInput()` 则使用 pinned task、summary、recent rounds 和当前 notification。 |
| 13. compaction 如何避免丢 pinned task？ | 原任务独立固定在 model input；压缩的是可替换的旧 rounds。 |
| 14. repeated compaction 的风险是什么？ | 第二次压缩不能丢掉第一次 summary 的事实，因此 current `compacted_context` 要参与下一次 source。 |
| 15. summary 可以当 evidence 吗？ | 不可以。它是有损决策 handoff；Trace、RuntimeState 和 TaskGraph 承担不同的持久事实。 |

### L4 State, Evidence & Reliability

| 问题 | 回答锚点 |
| --- | --- |
| 16. Trace 和 RuntimeState 的关系？ | Trace 是 append-only 有序账本；RuntimeState 是事件投影出的当前决策视图。 |
| 17. verifier 失败后怎么办？ | 记录 verification result，把 failure summary 回传给下一轮，允许一次默认 recovery；耗尽后不写 final。 |
| 18. 为什么 Trace 不等于 crash-safe replay？ | 当前没有 durable `state.json`、event replay、attempt identity 或 Git side-effect reconciliation。 |
| 19. evidence 由谁记录？ | Runtime event 由 recorder 记录；TaskGraph evidence 还要保留 actor identity，不能由 Leader 替 child/teammate 伪造。 |
| 20. `INVALID` 和行为失败有何不同？ | eval 的 provider/config/evidence 无效不能伪装成模型行为结论；有效行为失败才进入比较。 |

### L5 Coordination & Scale

| 问题 | 回答锚点 |
| --- | --- |
| 21. one-shot child 与 teammate 的区别？ | child 是 fresh、一次性 Session；teammate 是可持续寻址、带 mailbox 的参与者。 |
| 22. plan approval 与 delegate approval 的区别？ | 前者批准 teammate 的 TaskGraph plan，后者批准启动一个 write-capable child；两者都不代替每次写入 approval。 |
| 23. 为什么 source 要用 fingerprint？ | 防止 verified source 与 later integration source 不一致，也检测 verifier 意外改动 source 的 drift。 |
| 24. verification pass 后为什么仍不是 completed？ | verification 只证明 source command；Git integration receipt 才证明改动已进入 Leader target。 |
| 25. CompletionGate 检查什么？ | task terminal 状态、graph health、background/child、teammate shutdown/unread mailbox 与 cherry-pick 状态；它在 root finalization 前执行，配置 verifier 时也在 verifier 前执行。 |

## 10 道压力题

| 问题 | 不夸大的回应 |
| --- | --- |
| 1. 为什么不直接使用 LangGraph 或 AutoGen？ | 目标是把 Runtime control flow 拆成可运行教程 checkpoint，并不否认框架在产品工程中的价值。当前仓库刻意不把框架作为 core dependency。 |
| 2. file-backed TaskGraph 的并发边界是什么？ | 文件锁、temporary write 和 atomic rename 适合单 root run 本地协调；它不是 distributed lock service。 |
| 3. 模型不按 prompt 走怎么办？ | Runtime 的 policy、task protocol、validator 和 CompletionGate 仍会限制结果。模型偏离不自动变成成功。 |
| 4. 为什么 offline eval 只有 13 attempts？ | 它是五个固定行为场景的 contract，不是统计显著性研究。要扩大结论需要更多样本和事先定义的实验设计。 |
| 5. P0 修复了吗？ | 源码与 deterministic regression coverage 已补；post-fix independent comparable candidate 与 promotion 还没有完成，P0 仍开放。 |
| 6. Worktree 是否是安全隔离？ | 只隔离 Git 改动和 source provenance，不隔离进程、credentials、network 或 host permissions。 |
| 7. verifier 会不会被模型绕过？ | finalization 流程在 Runtime 内调用 configured verifier；不过 verifier 只证明它实际运行的 command，不能证明所有业务属性。 |
| 8. Git integration 崩溃后怎么办？ | 当前没有 reconciliation。source commit 成功与 receipt 写入之间的 crash 是明确未实现的 c18 压力。 |
| 9. 为什么拒绝审批也算有价值？ | 它能验证 deny/ask 的 action boundary，但不是用户任务完成的证据；live run 会非零退出并清理。 |
| 10. 下一步会做什么？ | 先闭合 compaction P0 的 post-fix evidence，再考虑 attempt/reconciliation 或更强隔离；不把它们说成当前已具备能力。 |

## English speaking material

### 30-second introduction

> I built Forge Harness as a TypeScript coding-agent Runtime from scratch. It starts with a real model-tool loop and grows through runnable checkpoints into governed execution, bounded context, durable Session and Trace evidence, Worktree-isolated delegation, and the c17c coordination protocol. The current boundary is local and inspectable rather than a hosted agent platform.

### 90-second introduction

> I built Forge Harness to make the control flow of a coding agent explicit. The Runtime has five responsibilities: the model and tool loop, action governance before dispatch, bounded model context, durable runtime evidence, and coordination across child sessions, Worktrees, and team tasks.
>
> The c17c protocol joins those responsibilities around an edit task. A task has an owner and a frozen verification contract. A teammate needs plan approval before it can write, while a one-shot edit child needs a separate delegation approval and still requests approval for each file mutation. The source is fingerprinted, verified, integrated through Git, and recorded with a receipt. A completion gate blocks a premature candidate until the remaining obligations settle. Once it is ready, finalization can proceed; if a root verifier is configured, it must pass before the final answer.
>
> I also kept deterministic tests and offline evaluations separate from live model observations. One fixed compaction comparison fell from three ordered reads to two. I kept that red comparable result rather than resampling it, and I do not claim post-fix independent validation yet.

### Eight high-frequency answers

| Question | Spoken answer |
| --- | --- |
| Why build a Runtime instead of a prompt wrapper? | I wanted the execution boundary to be inspectable. A prompt can request good behavior, but the Runtime decides whether a tool call dispatches, what enters the next model input, and what evidence is required before finalization. |
| What is the most important design boundary? | It depends on the failure mode. For side effects, it is permission before dispatch. For long sessions, it is separating model context from the Trace ledger. For coordination, it is separating a submitted source from verified and integrated work. |
| How do you handle model variability? | I do not hide it behind a passing screenshot. Deterministic tests cover Runtime invariants, live snapshots record one observation, and the offline eval has a fixed contract. Each evidence type has a narrower claim. |
| Why separate a child from a teammate? | A child is a fresh, one-shot execution unit. A teammate is long-lived and addressable through a mailbox. They solve different lifecycle problems, so they should not share one vague delegation abstraction. |
| Why does verification not complete an edit task? | Verification checks a registered source at a point in time. Integration must still create the source commit, move it into the Leader target, and record the receipt. |
| What did the compaction regression teach you? | It showed that a source-level fix and a behavioral claim are different. The frozen comparison found the regression. The current fix has deterministic coverage, but post-fix independent comparison is still pending. |
| Is this a security sandbox? | No. It has in-process policy, approval, path checks, and Worktree isolation. It does not isolate the operating system, credentials, network access, or malicious local code. |
| What would you build next? | I would close the open compaction evidence chain first. After that, crash-safe attempts and reconciliation are a meaningful next boundary because Git side effects can succeed before durable protocol state is recorded. |

## 不得声称

以下表述不要出现在简历、面试或公开介绍中。

| 不得声称 | 更准确的说法 |
| --- | --- |
| “Forge 已经是安全 sandbox。” | Forge 提供进程内 policy、approval、path boundary 和 Worktree 隔离，不是 OS sandbox。 |
| “模型不能越权。” | Runtime 可以在已覆盖的 action boundary 拒绝或要求审批；approved plugin 和 host-level side effect 仍有明确边界。 |
| “Trace 支持 replay/resume。” | Trace 是 durable evidence；crash-safe replay、resume 和 reconciliation 尚未实现。 |
| “Worktree 隔离了一切。” | Worktree 隔离 Git 改动和 source provenance，不隔离进程、网络、credentials 或 host permissions。 |
| “13-attempt eval 证明通用能力或统计显著性。” | 它比较固定场景中的行为和 hard invariant，不推出更广泛结论。 |
| “compaction 已经通过 post-fix eval 验证。” | 当前只有 frozen `3/3 -> 2/3` 红色 candidate；源码修复和测试存在，但 post-fix independent comparable candidate 未完成。 |
| “candidate 一出现就完成。” | candidate 仍要经过 pending work 收敛和 `CompletionGate`；配置 root verifier 时，还必须通过 verifier。 |
| “verification pass 就代表 edit 已经集成。” | verification pass 后仍是 `submitted`；Git integration receipt 才让 task `completed`。 |
| “Live demo 是稳定证据。” | Live 命令是一次可变的 operator walkthrough，不进 CI，也不作为可复用 evidence。 |
| “P1 branch 的命令已经在 main 发布。” | `demo:portfolio:live` 目前在 `codex/add-recruiter-portfolio` 分支，合并前应按分支状态描述。 |

## 面试前两分钟检查

1. 确认要讲的是当前源码事实，不把计划或下一步当作已交付。
2. 背下 `3/3 -> 2/3`、22 checkpoints、五层和 c17c 的 verify/integrate 区分。
3. 默认只跑 deterministic walkthrough；Live 只在 preflight 已完成且面试官要求时使用。
4. 能清楚说出四个边界：不是 OS sandbox、不是 crash-safe replay/resume/reconciliation、不是 distributed coordination、不是 hosted platform。
5. 对 P0 使用同一句收口：源码与 deterministic test 已补，独立 post-fix comparable evidence 尚未完成。
