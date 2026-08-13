# Forge Harness 技术学习指南

> 用途：面试前复盘架构、控制流、状态边界和证据口径。文中的路径均相对于 Forge Harness 仓库根目录；本文不依赖跨仓库相对链接。

## 先记住这句话

Forge Harness 是一个从零构建的 TypeScript coding-agent Runtime。它从最小的 model-tool loop 出发，用 22 个可运行 checkpoint 逐步补上治理、上下文、证据、隔离、扩展和协作。当前教程边界停在 `c17c Coordination / Completion Protocol`，不是托管平台，也没有实现崩溃恢复或分布式调度。

面试时不要把它讲成“模型会调用工具”。更准确的说法是：

```text
模型提出动作
  -> Runtime 判断能否执行
  -> 工具返回统一结果
  -> 结果进入有界上下文与持久 Trace
  -> 异步、任务、Git、验证义务全部收敛
  -> `CompletionGate` ready 后进入 finalization；若配置 root verifier，还须 verifier pass
```

## 一、从最小 loop 到 c17c：每个机制为什么出现

Forge 的演进不是功能清单，而是一串被具体失败逼出来的边界。

| 阶段 | 当时已经能做什么 | 暴露的痛点 | Runtime 接管的事实 |
| --- | --- | --- | --- |
| `c01-c04` 行动与治理 | 模型能调用 shell、读文件、改文件 | 路由会膨胀；副作用可能先执行再解释；文件修改难审查 | Tool registry、统一 `ToolResult`、`allow/ask/deny`、`edit/write` |
| `c05-c08` 上下文与可靠性 | 工具链可运行 | raw output 会挤满输入；运行结束后难复盘；模型自称完成并不可信 | `Observation`、`ContextProjection`、`Session`、`TraceEvent`、`RuntimeState`、verifier/recovery |
| `c09-c12` 长任务基础 | 单 Agent 能受治理地完成较长任务 | lifecycle 逻辑散落；计划不可见；prompt 组装随意；历史不断增长 | hooks、todo snapshot、prompt assembly、skills/memory、compaction |
| `c13a-c16b` 异步、隔离与扩展 | 单条工作线较完整 | 长命令阻塞；定时任务无持久入口；并行编辑污染 checkout；外部工具可能绕过治理 | background、cron、Git Worktree、child Sessions、MCP adapter、plugin preflight/trust |
| `c17a-c17c` 团队协议 | child 和 teammate 可以并行工作 | 共享状态不等于 ownership；handoff 不等于已验收；edit preview 不等于已集成；candidate 不等于 team completion | revisioned TaskGraph、mailbox、actor-owned evidence、plan/review、fingerprint、verification、Git receipt、CompletionGate |

这条因果链可以压缩成六问：

1. 模型输出怎样变成真实动作？
2. 动作执行前，谁判断边界？
3. 下一轮模型看到什么，哪些旧事实不能丢？
4. 运行中发生了什么，当前决策状态是什么？
5. 子任务和并行修改怎样隔离、交接、整合？
6. 谁能证明整个任务真的完成？

五个 Forge layer 分别回答这些问题，但它们不是目录，也不是章节顺序。

## 二、总控制流：一次 root run 怎样走

CLI 在第一次模型调用之前就准备 Runtime 边界：创建 root `Session` 和 TaskGraph，按需建立 root Worktree，解析 plugin/MCP 配置，完成 preflight 与本 Session 的 trust，再启动 loop。

一次常见 round：

```text
CLI / src/cli/index.ts
  -> createCliSessionTrace()                         # session.json + trace.jsonl
  -> assemblePrompt()                               # Session 初始化时组装稳定 instructions / memory / selected skill
  -> createInputHistoryManager().modelInput()       # 每轮：pinned task + summary + recent rounds + notifications
  -> responseCreate()                               # model request
  -> function_call?
       -> PermissionPolicy.decide()                 # allow / ask / deny
       -> PermissionApprover.approve()?             # ask 时才进入
       -> ToolRuntime.execute()
       -> ToolResult
       -> projectObservation()
       -> TraceRecorder.record() + RuntimeState
       -> 下一 round
  -> no tool / candidate answer
       -> settle background / child / teammate IPC
       -> CompletionGate                            # incomplete / failed / ready
       -> 配置 root verifier 时：verifier / recovery
       -> final_answer + session_ended
```

这里有三个经常被混淆的对象：

| 对象 | 作用 | 不是什么 |
| --- | --- | --- |
| `trace.jsonl` | append-only 历史账本，保存有序 Runtime events | 下一轮模型的 prompt |
| `RuntimeState` | 从事件投影出的当前决策视图 | 完整历史数据库或持久 `state.json` |
| compaction summary | 给下一次模型决策用的有损 handoff | 审计账本或完整恢复点 |

## 三、五层复习地图

### L1 Loop & Execution

| 复盘角度 | 要点 |
| --- | --- |
| 问题 | 模型给出的 function call 如何稳定地变成工具动作；没有工具时如何进入候选完成流程。 |
| 控制/数据流 | `responseCreate -> function_call -> governance -> ToolRuntime -> ToolResult -> Observation -> next model request`；无 tool 输出进入 candidate/finalization。 |
| 类型与模块 | `runMinimalLoop()`、`createMinimalLoopSession()`、`ResponseCreate` 位于 `src/core/minimalLoop.ts`；`ToolDefinition`/`ToolResult`/`ToolRuntime` 位于 `src/tools/`；`composeToolRuntimes()` 合并 built-in 与获批 MCP runtime。 |
| 不变量 | model 不直接调用工具实现；每个已执行调用都返回统一结果；duplicate tool name 在组合 runtime 时被拒绝；candidate 与 final 分开。 |
| 失败路径 | unknown tool fail closed；参数解析失败成为 tool result；工具超时/非零退出不伪装成完成；round budget 耗尽会失败。 |
| 取舍 | 显式 dispatcher 比框架路由啰嗦，但教程能直接展示 control flow；一个 round 只处理一个 tool call，简单但会增加协调轮次。 |
| 证据 | `test/core/minimalLoop.test.ts`、`test/tools/toolRuntime.test.ts`、`test/tools/compositeRuntime.test.ts`；`npm run test`、`npm run build`。 |

### L2 Governance & Action Boundary

| 复盘角度 | 要点 |
| --- | --- |
| 问题 | 合法工具调用仍可能越权；外部 MCP、plugin、delegate 和 Git 动作不能各自发明授权逻辑。 |
| 控制/数据流 | tool call 先进入 policy 分类，得到 `allow`、`ask` 或 `deny`；`ask` 再交给 approver；通过后才 dispatch。Plugin 在 import/MCP spawn 前先 preflight，再收集 per-Session trust。 |
| 类型与模块 | `PermissionDecisionAction`、`PermissionRisk`、`PermissionPolicy`、`PermissionApprover` 在 `src/governance/types.ts`；默认规则在 `src/governance/defaultPolicy.ts`；路径边界在 `src/tools/pathBoundary.ts`；plugin preflight 在 `src/extensions/pluginPreflight.ts`。 |
| 不变量 | 未知工具和已知 destructive shell shape 默认拒绝；inspect 与 mutation 分开；MCP annotations 不能取代 Forge policy；未获信任 plugin 不得贡献 skill、hook 或 MCP server。 |
| 失败路径 | `deny` 不执行；非交互终端无法批准 `ask`；plugin descriptor/component 任一 preflight 失败时不先 import 一半组件；路径越界在工具执行前拒绝。 |
| 取舍 | 这是进程内治理，不是 OS sandbox。获批 plugin hook 仍拥有当前进程权限；trust 只在当前 Session 有效，不是持久信任库。 |
| 证据 | `test/governance/defaultPolicy.test.ts`、`test/cli/approval.test.ts`、`test/governance/mcpPolicy.test.ts`、`test/extensions/pluginPreflight.test.ts`、`test/extensions/pluginActivation.test.ts`。 |

### L3 Context & Knowledge

| 复盘角度 | 要点 |
| --- | --- |
| 问题 | raw transcript、工具大输出、skills、memory、mailbox 和 handoff 会争夺 context window；下一轮既不能失忆，也不能无限增长。 |
| 控制/数据流 | `ToolResult -> projectObservation() -> bounded function_call_output`；`assemblePrompt()` 在 Session 初始化时组装稳定 instructions；每轮由 history manager 的 `modelInput()` 提供 pinned 原任务、summary、recent rounds 与新 notification，并用 summary 替换较早 rounds。 |
| 类型与模块 | `Observation`、`ContextProjection`、`assemblePrompt()`、`createInputHistoryManager()` 位于 `src/context/`；`ContextCompactionTrigger`、`CompactionSource`、`InputHistoryManager` 位于 `src/context/compaction.ts`。 |
| 不变量 | 原始 user task pinned；system prompt、memory、skill catalog 不被 conversation compaction 覆盖；当前 `compacted_context` 必须进入下一次 compaction source；Trace 不参与压缩。 |
| 失败路径 | summary 为空时显式 `context_compaction_failed`；reactive compact 后仍超过 hard budget 就停止；summary 可缺 heading，但缺项进入诊断 metadata。 |
| 取舍 | 字符预算稳定、易测试，但不等于 provider token accounting；summary 有损，所以 completion-critical facts 必须进入 RuntimeState、TaskGraph 或 Trace。 |
| 证据 | `test/context/contextProjection.test.ts`、`test/context/promptAssembly.test.ts`、`test/context/compaction.test.ts`；offline eval 的 `compaction-retention` 场景。 |

### L4 State, Evidence & Reliability

| 复盘角度 | 要点 |
| --- | --- |
| 问题 | 仅有对话无法回答“发生过什么”“当前卡在哪里”“哪个检查真正通过了”。 |
| 控制/数据流 | 每个 Runtime event 追加到 `trace.jsonl`；同一事件同步更新 `RuntimeState`；candidate 先经过 `CompletionGate`，配置 root verifier 时才进入 verifier；可恢复的 verifier failure 写入下一轮 repair signal。 |
| 类型与模块 | `SessionMetadata`、`TraceEventPayload`、`RecordedTraceEvent`、`RuntimeState`、`Verifier`；主要位于 `src/runtime/session.ts`、`src/runtime/trace.ts`、`src/runtime/traceRecorder.ts`、`src/runtime/state.ts`、`src/runtime/verification.ts`。 |
| 不变量 | Trace 按 Session ID、sequence、timestamp 有序；final answer 只能在 `CompletionGate` ready 后记录，配置 root verifier 时还必须先通过 verifier；TaskGraph evidence 要保留 actor identity；Git integration 要留下 receipt。 |
| 失败路径 | verifier fail 可以进入一次默认 recovery；blocked 或 recovery budget 耗尽时不记录 final；invalid Trace schema 会让 eval attempt 成为 `INVALID`，不冒充行为失败。 |
| 取舍 | 当前 projection 轻量、适合决策，但不能从 crash 后自动恢复；没有 event replay、resume、reconciliation 或持久 `state.json`。 |
| 证据 | `test/runtime/session.test.ts`、`traceRecorder.test.ts`、`state.test.ts`、`verification.test.ts`；`docs/assets/evidence/verification-recovery.json`。 |

### L5 Coordination & Scale

| 复盘角度 | 要点 |
| --- | --- |
| 问题 | 长命令、定时任务、child、长期 teammate、并行编辑和共享 task 会产生等待、归属、交接与收尾问题。 |
| 控制/数据流 | background/cron 扩展时间边界；Worktree 扩展文件边界；child 用 fresh Session 交回 handoff；teammate 用 mailbox 持续收发；TaskGraph 保存 ownership 与协议状态；CompletionGate 汇总完成义务。 |
| 类型与模块 | `AsyncChildSessionManager`、`TeammateManager`、`MailboxStore`、`TeamTask`、`TeamTaskStore`、`GitIntegrationService`、`CompletionGateResult`；位于 `src/extensions/`、`src/runtime/`、`src/domain/`。 |
| 不变量 | parent final 前 async child 必须 terminal；mailbox 自动处理 FIFO 且 at most once；TaskGraph mutation 在文件锁内原子写入并递增 revision；edit 完成必须有验证 verdict 和 integration receipt；所有 teammate stopped 且 unread=0。 |
| 失败路径 | child/teammate failure 写入结构化状态；owner failure 可 block 未提交任务；verification/drift 退回 `in_progress`；cherry-pick 冲突先 abort 再 block；CompletionGate 可能 `incomplete` 或 `failed`。 |
| 取舍 | 单 root-run、文件型协调状态便于检查，不是 distributed scheduler；Worktree 隔离改动，不隔离进程、凭据、网络和主机权限。 |
| 证据 | `test/extensions/childSessions.test.ts`、`teammates.test.ts`、`test/runtime/teamTaskProtocol.test.ts`、`gitIntegration.test.ts`、`completionGate.test.ts`、两条 c17c smoke。 |

## 四、c17c 完整路径

### 1. 先分清四种身份/事实

| 概念 | 权威来源 | 说明 |
| --- | --- | --- |
| Leader | root Session | 唯一协调者；可 assign、review、verify、integrate、shutdown。 |
| teammate owner | TaskGraph 的 `TeamTaskOwner` | 稳定身份 `{ role: "teammate", name }`，不是临时 session ID。 |
| one-shot child | child terminal registry | child 永远不是 owner；Leader 先拥有 task，child 只追加 actor-owned evidence。 |
| result source | trusted child/teammate registry | 保存 source Session、Worktree branch/path、changed files；模型不能自报 workspace path。 |

TaskGraph v2 的状态机：

```text
pending -> in_progress -> submitted -> completed
              ^              |
              +--------------+  review 或 verification failed

pending | in_progress | submitted -> blocked
```

`completed` 和 `blocked` 都是本次 root run 的终态。c17c 没有 `task_unblock`，也不会把失败 work 自动转给另一个 owner。

### 2. research task 路径

```text
create(kind=research)
  -> Leader assign，或 teammate 对 ready + unowned task 原子 claim
  -> owner / linked child 追加 actor-owned evidence
  -> submit_result
  -> Leader review_result(pass)
  -> completed
```

要点：

- `assign`/`claim` 在同一个文件锁内同时写入 owner 与 `in_progress`，并发 claim 只能有一个赢家。
- one-shot research child 不拥有 task。Leader 先 assign 给自己，再以 `taskId` delegate。
- Leader 不能替指定 actor 补 evidence 来“修绿”协议。
- review fail 会把 task 退回 `in_progress`，而不是伪造 completed。

### 3. long-lived edit teammate 路径

```text
create(kind=edit, verificationCommand)
  -> teammate claim
  -> submit_plan
  -> Leader review_plan(approve)
  -> teammate 在稳定 Worktree 中 edit/write
  -> task_add_evidence
  -> submit_result                         # source 由 registry 解析
  -> Leader task_get                       # diff / changedFiles / fingerprintStatus
  -> task_verify(exact contract command)   # 通过后仍是 submitted
  -> task_integrate                        # source commit + cherry-pick + receipt
  -> completed
  -> teammate_shutdown
```

contract 在 acquire 后冻结。`task_update` 只能修改或删除尚未 acquire 的 pending contract，不能直接写 status、owner、plan、verdict、receipt 或 blocker。ownership、plan 和 result submission 的状态变更走 `task_transition`；`task_verify` 与 `task_integrate` 是各自的专用工具。它们都按 actor role 二次校验。

### 4. one-shot edit child 路径

```text
Leader owns edit task
  -> delegate(profile=edit, taskId)
  -> fresh child Session + isolated Worktree
  -> child edit/write + actor-owned evidence + handoff
  -> terminal registry 固定 childSessionId 与 task/source
  -> Leader submit_result(childSessionId)
  -> task_verify
  -> task_integrate
  -> completed
```

Leader 提交时只能给 `childSessionId`，不能把模型传来的 workspace path 当可信来源。同一个 terminal child source 不能被另一个 task 重用。

### 5. 两种“批准”不能混为一谈

| 场景 | 批准的对象 | 批准者/机制 | 持久效果 | 后续写操作还要不要审批 |
| --- | --- | --- | --- | --- |
| long-lived teammate 的 plan approval | task owner 提交的执行计划 | Leader 通过 `review_plan` 更新 TaskGraph | plan 状态变为 `approved`；teammate 才具备请求写入的协议资格 | 要。broker 先检查 owner/status/plan，具体 `edit/write` 仍走 permission/approver，并在执行前再次检查 TaskGraph，防止 stale approval。 |
| one-shot edit child 的 delegate approval | 启动一个 write-capable child Session | parent 侧 policy 对 `delegate(profile=edit)` 返回 `ask` | 只允许创建这个隔离 child，不产生 TaskGraph plan approval | 要。child 内每次 `edit/write` 仍逐次 `ask`。one-shot child 不是 task owner，也不走 teammate 的 `submit_plan/review_plan`。 |

一句话记忆：teammate plan approval 是 TaskGraph 协议门禁；edit child delegate approval 是启动可写 child 的动作审批。两者都不是“一次批准全部写入”。

### 6. fingerprint、verification 与 integration

submitted edit 只说明 owner 交件，不说明结果可信。`GitIntegrationService` 把后半段拆成两个动作边界。

fingerprint 输入包括：source `HEAD`、排序后的 Git status、每个 changed path 的 mode/type/content hash，以及 deleted path 的 index mode 与删除标记。

`task_verify`：

- command 必须与 task contract 的 `verificationCommand` 完全一致；
- 在注册 source Worktree 中执行；
- 执行前后重算 fingerprint；
- verifier 若产生未忽略文件，视为 source drift，清除 submission 并退回 `in_progress`；
- pass 只写 verdict，task 仍是 `submitted`。

`task_integrate`：

- submission fingerprint 与 verification fingerprint 必须一致；
- Leader target 必须 clean，且不能有进行中的 cherry-pick；
- source identity、branch、path 和 Git author/committer identity 必须有效；
- source 先创建带 `Forge-Task`、`Forge-Owner`、`Forge-Source` trailers 的 commit；
- commit cherry-pick 到 Leader target；
- 成功后写 `TeamTaskIntegrationReceipt`，task 才变为 `completed`。

冲突时立即 `cherry-pick --abort`，保留 source commit，task 进入 `blocked`。c17c 不自动解冲突。

### 7. CompletionGate 到 final answer

模型给出 candidate 后，loop 先 event-driven 等待 background、child 和 teammate IPC 收敛。若有 terminal notification，先注入下一轮 context，不会在等待期间空转调用模型。

`createCompletionGate()` 读取各模块 projection，但不替它们改状态：

| 结果 | 条件/行为 |
| --- | --- |
| `incomplete` | 仍有可执行义务，例如 edit 待 verify/integrate、child 尚未 handoff、teammate 未停止；blocker 回到下一轮。 |
| `failed` | blocked task、degraded graph、owner failure、未清理 cherry-pick 等终止性问题；root run 失败。 |
| `ready` | 所有 task completed；graph healthy；无 pending background/child；teammates 全部 stopped 且 unread=0；无 cherry-pick in progress。随后进入 finalization；仅在配置 root verifier 时才运行它。 |

`final_answer` 与 `session_ended(completed)` 的前提是 Gate ready；若配置 root verifier，还需要其 pass。Gate ready 当前没有单独事件，要从完整不变量链、配置 verifier 时的根级 `verification_result`、`final_answer` 和 `session_ended` 推断。

## 五、c17c 常见失败路径

| 失败 | Runtime 行为 | 为什么不能直接重试/忽略 |
| --- | --- | --- |
| 两个 teammate 同时 claim | 文件锁内原子 acquire，只有一个成功 | ownership 必须只有一个权威状态。 |
| teammate 未获 plan approval 就写 | broker 拒绝；执行前还会二次检查 | 防止消息延迟或 stale approval 绕过协议。 |
| submitted/handoff 后继续写 | before-execute check 拒绝 | 交件后的 source 必须冻结，才能验证 fingerprint。 |
| 模型传入任意 workspace path | handler 不接受该参数，改从 registry 解析 | 路径字符串不能证明 task/source 归属。 |
| verifier 改了 source | 判定 drift，清 submission，回到 `in_progress` | 验证不能偷偷改变待集成对象。 |
| verification pass 后直接 completed | 不允许；仍保持 `submitted` | 验证只证明 source，receipt 才证明已进入 Leader target。 |
| cherry-pick 冲突 | abort，保留 source commit，task `blocked` | 自动解冲突会扩大本章边界，也可能破坏已审查 diff。 |
| teammate idle 但未 shutdown | CompletionGate 不 ready | idle 只是当前没跑 turn，不代表进程已退出。 |
| mailbox claimed batch 处理失败 | 不隐式 replay；显式 rejoin 才恢复 | 自动重放需要 idempotency/reconciliation，c17c 没有。 |
| Git 已成功但 receipt 写入前 crash | 当前无法判断是否已执行或执行到一半 | 这是留给 c18 的 Attempt/resume/reconciliation 问题。 |

## 六、22 个 runnable checkpoint 索引

索引里的“验证”优先写最短、最稳定的观察入口；完整 live prompt 请按 `docs/02-tutorial-roadmap.md` 回到 `docs/tutorial/` 下的对应章节。所有 checkpoint 共享仓库级检查：`npm run test`、`npm run typecheck`、`npm run build`。

### Part 1: Core Harness

| Checkpoint / layer | 迫使机制出现的痛点 | 最小机制 | 关键模块/类型 | 代表验证 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| `c01 Minimal Real Loop` / L1 | LLM 只能返回文本，不能行动 | 单 model call + 单 `bash` 路径 + tool round trip | `src/core/minimalLoop.ts`、`src/core/bashTool.ts` | `npm run start -- "inspect this project scaffold and summarize what is implemented"` | 第二个工具会让 loop routing 膨胀。 |
| `c02 Tool Runtime` / L1 | 每加一个工具都要改 core loop | tool definition、registry、dispatcher、统一 result；`bash/read/ls` | `src/tools/types.ts`、`src/tools/runtime.ts`、`src/tools/defaultRuntime.ts` | build 后让模型依次 `ls`、`read package.json` | 工具有副作用，但还没有统一 permission。 |
| `c03 Permission Governance` / L2 | model tool call 可能产生副作用 | risk、`allow/ask/deny`、approval | `src/governance/types.ts`、`src/governance/defaultPolicy.ts`、`src/cli/approval.ts` | read-only 自动执行；`touch` 触发审批 | 没有专门、可 review 的文件编辑。 |
| `c04 Reviewable File Editing` / L1+L2 | 只靠 shell 改文件难审查、难限制 | exact `edit`、`write`、diff-like result | `src/tools/editTool.ts`、`src/tools/writeTool.ts` | 用 `edit` 精确替换 demo 文本并观察 approval/result | 工具结果原样回填会挤压 context。 |
| `c05 Context Projection` / L3 | raw history、搜索和大输出挤满下一轮 | `grep/find`、`Observation`、`ContextProjection` | `src/context/observation.ts`、`src/context/projection.ts` | `find -> grep -> read`，观察 bounded output | 多轮历史仍无限增长；运行证据仍短命。 |
| `c06 Session / Trace` / L4 | 运行结束后无法检查发生过什么 | `Session` metadata、JSONL `TraceEvent` | `src/runtime/session.ts`、`src/runtime/trace.ts`、`src/runtime/traceRecorder.ts` | 运行 CLI 后检查 `.forge/sessions/<id>/session.json` 与 `trace.jsonl` | Trace 是历史，不是当前决策状态，也不能 resume/replay。 |
| `c07 Runtime State Model` / L4 | 每次决策都重扫 Trace 成本高且语义混乱 | `RuntimeState` event projection | `src/runtime/state.ts`、`applyRuntimeStateEvent()` | 观察 transcript 中 latest tool/error/check state | final 仍由模型自己声明。 |
| `c08 Verification / Recovery` / L4 | plausible final 不等于任务通过 | candidate、external verifier、failure summary、一次默认 repair | `src/runtime/verification.ts`、`src/core/minimalLoop.ts` | `npm run start -- --verify "npm run build" ...` | lifecycle 扩展点、显式任务计划还未抽离。 |

### Part 2: Scale & Extensions

| Checkpoint / layer | 迫使机制出现的痛点 | 最小机制 | 关键模块/类型 | 代表验证 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| `c09 Hooks` / L5+L4 | logging/metrics/notification 继续塞进 loop 会污染主控制流 | stable lifecycle events、observe-only hook runner | `src/extensions/lifecycle.ts`、`LifecycleEmitter` | `--hook-log --verify "npm run build"` | 长任务仍没有显式计划与 acceptance。 |
| `c10 Task / Todo` / L5+L4 | 复杂任务的计划、状态和验收只在自然语言里 | `todo` snapshot、`task_state_updated`、context/state projection | `src/runtime/task.ts`、`src/tools/todoTool.ts` | 运行 chapter handoff/read-only smoke 并观察 task snapshot | 全量 snapshot 消耗 token；prompt 知识入口仍零散。 |
| `c11 System Prompt / Skills / Memory` / L3 | instruction、skill、项目知识每次手写进 prompt | stable prompt assembly、selected skill、catalog、`.forge/memory.md` | `src/context/promptAssembly.ts` | 用 `/chapter-handoff` 等显式 skill invocation 运行 | conversation history 仍会超过 budget。 |
| `c12 Context Compaction` / L3+L4 | 长 Session 的 raw rounds 不断增长；连续压缩可能丢旧 summary | soft/hard budget、structured handoff、auto/reactive compact、summary rollover | `src/context/compaction.ts`、`InputHistoryManager` | 连续读取 c09-c11，观察 `context_compacted` | 字符预算不是精确 token accounting；无 `/compact` 和 resume。 |
| `c13a Background Tool Tasks` / L5+L4 | 长 bash 阻塞 foreground loop | session-scoped background bash、notification、pending gate | `src/runtime/backgroundTasks.ts` | 启动两个 `runInBackground=true` bash，同时执行 foreground `ls` | 只覆盖当前 Session，不支持稍后/定时唤醒。 |
| `c13b Scheduled Jobs / Cron` / L5+L4 | 工作需要稍后或周期执行 | durable schedule、cron worker、fresh scheduled run | `src/runtime/cron.ts`、`src/runtime/cronStore.ts`、`src/extensions/cronWorker.ts` | `npm run start -- --cron-worker-once` | scheduled edit 仍可能污染共享工作区。 |
| `c14 Worktree Isolation` / L2+L4+L5 | 并行或高风险修改污染 base checkout | root/session-bound Git Worktree、workspace metadata | `src/runtime/workspace.ts`、`src/runtime/sessionWorkspace.ts` | `npm run start -- --worktree ...`，比较 base 与生成 Worktree | 没有独立 child context 和结构化 handoff。 |
| `c15a Child Sessions / Handoff` / L5+L3+L4 | 子任务挤占 parent context，也需独立工具/工作区 | sync fresh child、research/edit profile、summary handoff | `src/extensions/childSessions.ts`、`src/tools/delegateTool.ts` | delegate research；delegate edit 后检查隔离 Worktree | 同步 child 会阻塞 parent；edit 只有 preview。 |
| `c15b Async Child Sessions / Parallel Handoff` / L5+L3+L4 | 多个独立 child 串行等待 | async registry、terminal notification、pending final gate、edit preview metadata | `AsyncChildSessionManager`、`createAsyncChildSessionManager()` | 两个 background research child，等待 handoff 后 final | parent/child 仍无共享 dependency、status、acceptance。 |
| `c16a MCP Tool Integration` / L1+L2+L4 | 外部 MCP tool 可能绕过既有 runtime 与治理 | strict config、startup trust、MCP adapter、动态 runtime | `src/extensions/mcpConfig.ts`、`src/extensions/mcpSession.ts`、`src/extensions/mcpToolAdapter.ts`、`src/governance/mcpPolicy.ts` | 调用本地 demo lookup/create_note，并观察 policy/result/trace | skills、hooks、MCP 仍缺统一 plugin loading boundary。 |
| `c16b Plugin Loading / Registration` / L2+L3+L4+L5 | 本地扩展组件各自接入，加载顺序和信任难追踪 | descriptor/component preflight、per-Session trust、namespace、activation snapshot | `src/extensions/pluginPreflight.ts`、`src/extensions/pluginActivation.ts`、`src/extensions/pluginDescriptors.ts` | 激活 `/issue-workflow:triage` 并调用 namespaced MCP tool | child/teammate 和 task 状态仍是分散的。 |
| `c17a Shared Team Task Graph` / L5+L4 | parent、sync/async child 各自维护 task snapshot | root-scoped file TaskGraph、dependency、role permission、acceptance/evidence、atomic revision | `src/domain/teamTask.ts`、`src/runtime/teamTaskStore.ts`、`src/tools/teamTaskTools.ts` | c17a 七步 smoke：not-ready 失败、child evidence、dependency ready | 没有 owner/assign/claim/verifier。 |
| `c17b Long-Lived Teammates / Mailbox` / L5+L3+L4 | one-shot child handoff 后退出，无法持续寻址 | named process、persistent mailbox、direct/broadcast、explicit rejoin | `src/extensions/teammates.ts`、`src/runtime/teamMailbox.ts`、`src/cli/teammateWorker.ts` | start -> follow-up；failure -> queued offline -> rejoin | mailbox 传消息但不建立 ownership，也不证明已集成。 |
| `c17c Coordination / Completion Protocol` / all | task graph/mailbox 仍不能决定归属、验收、集成和团队完成 | owner、assign/claim、plan/review、trusted source、fingerprint、verify/integrate receipt、shutdown、CompletionGate | `TeamTask`、`TeamTaskStore`、`GitIntegrationService`、`CompletionGateResult`、`TeammateManager` | `npm run smoke:c17c-capstone`；`npm run smoke:c17c-child` | crash-safe Attempt/resume/idempotency/reconciliation/event replay。 |

计数检查：Part 1 有 8 个，Part 2 有 14 个，共 22 个 runnable TypeScript checkpoints。`c00 Orientation` 是导读，不计入 runnable checkpoint；`c18` 是未来压力，不是当前能力。

## 七、证据怎么读，哪些话可以说

### 证据强度

```text
claim
  -> source implementation
  -> focused deterministic tests
  -> deterministic integration smoke
  -> sanitized live snapshot（可选）
  -> fixed offline behavioral comparison（真实模型，但非生产流量）
```

| 层级 | 能证明什么 | 不能证明什么 |
| --- | --- | --- |
| Source | 边界、类型、状态机和 ownership 写在哪里 | 实际路径一定被执行 |
| Focused tests | 单个边界与失败分支可重复 | 完整 CLI/model 协作一定成功 |
| Deterministic smoke | TaskGraph、Git、CompletionGate 等模块能集成闭环 | 模型会选对工具，或 tool schema/policy 全链经过 |
| Live snapshot | 某次真实模型 run 达到记录的不变量 | 未来每次 run 都相同 |
| Offline eval | 固定 experiment identity 下的行为计数变化 | 通用 coding 能力、统计显著性、生产稳定性 |

仓库级证据入口：

```bash
npm run docs:check
npm run typecheck
npm run test
npm run build
npm run smoke:c17c-capstone
npm run smoke:c17c-child
npm run eval -- run --model <model>
```

### 面试 Live launcher 的边界

`npm run demo:portfolio:live` 不是另一个 Runtime。它只是面试时使用的薄启动器：通过 `fs.mkdtemp()` 在系统临时目录现场生成独立的 retry-policy Git fixture，确认初始 `npm test` 失败，再用参数数组启动现有 Forge CLI：

```bash
forge-harness --worktree --verify "npm test" "<focused retry task>"
```

Fixture 提交 `.gitignore` 并忽略 `.forge/`，否则 Session 初始化先创建的 `.forge/` 会让后续 root Worktree dirty check 失败。这个修复只属于 disposable fixture，不放宽通用 workspace 检查。

演示固定一个 edit task 和一个同步 edit child，是为了控制时长、拓扑和证据归属，不代表 Runtime 只能处理一个任务。模型仍自行决定 task 文案、文件阅读、`src/**` 实现、编辑次数和协议调用顺序。Child 不具备 Bash；Leader 在 child source 上执行 `task_verify`，集成后 root verifier 再运行 `npm test`。

Launcher 使用 inherited terminal 显示原始 Runtime transcript 与人工审批，只在前后打印简短 `[demo]` 说明。它最多运行 10 分钟，超时先发 `SIGTERM`，两秒后再发 `SIGKILL`，并在所有结束路径清理 fixture。这个过程只是一次可变模型运行观察，不是 benchmark、CI 检查或可复用 evidence。

“offline” 只表示不承载真实用户流量。canonical eval 仍调用模型 API、需要凭据并消耗 token。固定套件是 `3 + 3 + 3 + 3 + 1 = 13` 次 attempts，场景包括 governed read-only、verification recovery、compaction retention、async child handoff 和 c17c team completion。v1 使用 deterministic grader，不使用 LLM-as-a-judge。

### 当前 P0：compaction 证据没有闭环

已提交的 regression report 是当前对外可引用的独立比较证据：baseline 的 `compaction-retention` 为 `3/3`，candidate 为 `2/3`，`ordered-reads` 少 1；同时 async child handoff 从 `2/3` 提升到 `3/3`。比较器不允许一项改善抵消另一项下降，所以 verdict 是 `REGRESSED`。

当前源码已经包含 repeated-compaction 修复（提交 `a0146b2`）：旧实现第二次压缩时可能用新 raw rounds 替换第一次 summary，导致更早事实丢失；修复让当前 `compacted_context` 进入下一次 compaction source，并用连续三次 compaction 的单元测试覆盖 summary rollover。这个描述是源码与测试的内部当前状态。

不能进一步声称：

- 修复后已经有新的独立 comparable candidate；
- `compaction-retention` 已恢复到 `3/3`；
- 新 candidate 已获 `UNCHANGED`/`IMPROVED`；
- baseline 已因本次修复重新 promotion；
- P0 已关闭。

面试时最稳妥的说法是：“真实模型基线比较抓到 `3/3 -> 2/3` 的 repeated-compaction 行为回归；源码根因和 deterministic regression coverage 已补，但修复后的独立 candidate 与 promotion 证据尚未完成，因此 P0 仍开放。”

## 八、源码与证据阅读路线

### 30 分钟快速路线

1. `README.zh-CN.md`：确认项目定位、五层、命令和边界。
2. `docs/engineering-case-study.md`：按痛点理解六个工程决定。
3. `docs/architecture-overview.md`：看当前 c17c 的模块 ownership 和 root runtime path。
4. `docs/tutorial/c17c-coordination-completion-protocol.md`：完整走一遍 task/edit/completion 协议。
5. `docs/evidence-index.md`：把每个能力映射到源码、测试、smoke 与限制。
6. `docs/assets/evidence/offline-eval-regression-report.md`：核对当前红色证据，不要只看摘要。

### 90 分钟源码路线

| 顺序 | 阅读路径 | 带着什么问题读 |
| ---: | --- | --- |
| 1 | `src/core/minimalLoop.ts` | round、permission、notification、candidate、gate 与按需运行的 verifier 的先后顺序是什么？ |
| 2 | `src/tools/runtime.ts`、`src/tools/compositeRuntime.ts`、`src/governance/defaultPolicy.ts` | policy 与 dispatch 怎样解耦，unknown/duplicate 怎样 fail closed？ |
| 3 | `src/context/projection.ts`、`src/context/promptAssembly.ts`、`src/context/compaction.ts` | tool result、instructions、history 各自怎样进入 model input？ |
| 4 | `src/runtime/session.ts`、`src/runtime/trace.ts`、`src/runtime/state.ts` | durable ledger 与 current projection 怎样分工？ |
| 5 | `src/extensions/childSessions.ts`、`src/extensions/teammates.ts`、`src/runtime/teamMailbox.ts` | fresh child 与 long-lived teammate 的生命周期差异是什么？ |
| 6 | `src/domain/teamTask.ts`、`src/runtime/teamTaskStore.ts` | TaskGraph contract、状态机、actor 权限和 revision 如何落地？ |
| 7 | `src/tools/teamTaskTools.ts` | 模型看到的 role-scoped tool surface 如何分别映射 ownership/plan/result transition 与 verification/integration mutation？ |
| 8 | `src/runtime/gitIntegration.ts`、`src/runtime/completionGate.ts` | source fingerprint、verification、receipt 和 final gate 如何闭环？ |
| 9 | 对应 `test/` 文件与两条 smoke | 正向路径和失败路径分别由什么 deterministic evidence 覆盖？ |
| 10 | `src/eval/`、`docs/offline-eval.md` | 行为结果、hard invariant、infrastructure invalid 和 comparability 怎样区分？ |

### 22 checkpoint 顺序路线

以 `docs/02-tutorial-roadmap.md` 为目录，从 `docs/tutorial/c01-minimal-real-loop.md` 读到 `docs/tutorial/c17c-coordination-completion-protocol.md`。每章固定抓五件事：

- 前一边界暴露了哪个具体痛点；
- 本章只加入哪个最小机制；
- 控制流在哪个位置改变；
- smoke run 应观察什么；
- 下一章为何不能提前合并进来。

## 九、明确边界：答到这里就停

| 当前没有 | 具体含义 |
| --- | --- |
| crash-safe replay/resume/reconciliation | 进程在 Git side effect 与 TaskGraph receipt 之间崩溃后，无法自动判断和对账；没有 Attempt identity、idempotent replay 或 event replay。 |
| distributed coordination | TaskGraph 是一个 root-run-scoped 文件图，不是分布式 scheduler；没有 remote worker、lease、consensus、leader election、failover 或 HA。 |
| OS sandbox | Permission、路径校验和 Worktree 都是进程内/仓库级边界；不隔离进程、凭据、网络、主机权限或恶意本地进程。 |
| hosted platform | 没有 Web UI、hosted control plane、multi-tenant service 或生产托管行为；仓库提供源码、CLI、测试和证据。 |

还应主动说明：

- approved plugin hook 是进程内可信代码；Forge 没有 plugin marketplace、downloader、package manager 或持久 trust database。
- mailbox 自动处理是 at most once。失败 batch 不会隐式 replay；rejoin 是显式动作。
- Worktree 解决改动隔离和 Git provenance，不是安全容器。
- verifier 只证明注册 command 的结果，不证明所有语义属性。
- live snapshot 和 13-attempt eval 都不能推出确定性模型行为或统计显著性。

## 十、面试自测

如果下面的问题不能在两分钟内答清，回到对应章节：

- 为什么 `ToolResult`、`Observation`、Trace event 不是同一个对象？
- 为什么 compaction summary 可以有损，而 TaskGraph/Trace 的完成事实不能只留在 summary？
- 为什么 `RuntimeState` 不能代替 `trace.jsonl`？
- 为什么 verification pass 后 edit task 仍是 `submitted`？
- one-shot child 为什么不能成为 TaskGraph owner？
- teammate plan approval 与 delegate approval 分别批准什么？
- source fingerprint 为什么要包含 `HEAD`、Git status 和文件内容 hash？
- CompletionGate 为什么必须在 root finalization 之前？配置 verifier 时，它为什么排在 verifier 之前？
- mailbox at-most-once 与 c18 reconciliation 的关系是什么？
- 当前 compaction P0 到底已有哪一层证据，缺哪一层证据？

可以这样收口：Forge 把模型容易含糊带过的授权、上下文、证据、归属、验证和完成条件，逐步变成 Runtime 可以检查的事实。“多 Agent”只是这条工程链后半段的问题。
