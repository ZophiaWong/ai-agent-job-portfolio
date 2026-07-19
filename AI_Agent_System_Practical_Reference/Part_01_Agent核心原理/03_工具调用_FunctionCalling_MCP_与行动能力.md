# 03 工具调用、Function Calling、MCP 与行动能力

## 0. 章节元信息

- 主要能力：C04.03
- 关联能力：C04.01、C04.02、C08.01
- 练习协议：[统一练习协议](../../interviews-docs/practice-protocol.md)
- 参考基线：MCP 稳定规范 2025-11-25；访问日期 2026-07-19

本章回答两个问题：模型提出动作后，后端怎样把它变成受控执行；MCP 怎样在不放松权限的前提下，统一暴露工具、资源和提示模板。

## 1. 冷启动任务

先不要向下阅读。用 12 分钟完成 `mcp-boundary-design.md`，内容包括：

1. 画出 Host、Client、Server 的连接关系，并把数据层和传输层分开。
2. 写出连接从初始化到关闭的顺序，说明什么时候可以调用 `tools/list`。
3. 为“读取知识库”和“创建工单”分别选择 tool、resource 或 prompt，并解释控制权。
4. 给远程 HTTP Server 和本地 stdio Server 各写一套凭证边界。
5. 标出哪些输入来自 Server，哪些动作需要用户同意。

可检查产物必须有消息顺序、权限判断、失败分支和一条事实边界。阅读本章或复制示例不算独立证据。

### 迁移题

把约束改成“同一个 Host 同时连接一个本地文件 Server 和一个远程工单 Server”。更新设计，说明两个 Client 是否共享连接、远程访问令牌能否交给本地 Server，以及工单 Server 临时撤销 tools 能力时怎样处理。

### 延迟复测

隔天关掉资料，用 5 分钟重画生命周期和信任边界，保存为 `mcp-boundary-retest.md`。只有两份产物都能独立解释，才把它当作 C04.03 的候选证据。

<!-- MCP 参考分隔线：完成冷答后再继续 -->

## 2. Function Calling 的执行边界

Function Calling 让模型生成结构化调用意图，例如：

```json
{"name": "create_ticket", "arguments": {"title": "登录失败", "priority": "P2"}}
```

这不是一次已经发生的调用。后端仍要检查工具名、参数 schema、身份、数据范围、风险和幂等记录。模型的输出只能进入“提案”状态；工具返回也不能直接当作可信事实。

```text
模型提案 → 服务端校验 → 授权/审批 → 执行 → 验证结果 → 记录审计 → 回填模型
```

写工具要比读工具多考虑副作用。超时不等于失败，也可能是“服务端已经成功，但响应丢了”。因此重试前必须查幂等记录或业务状态。

## 3. MCP 参考模型

### MCP 的参与者

- MCP Host 是承载 AI 应用的进程，管理用户交互、安全策略和多个 MCP Client。
- MCP Client 是 Host 内的协议组件，维护到一个 Server 的专用连接并交换消息。
- MCP Server 暴露上下文或动作能力；它可以和 Host 同机运行，也可以是远程服务。

每个连接到的 MCP Server 都对应一个专用 MCP Client。一个 Host 可以创建多个 Client，但不要把多个 Server 描述成共享同一条 Client 连接。这里的“一对一”说的是 Client 连接关系，不是说远程 Server 只能服务一个 Client。

### MCP 的分层

MCP 的数据层使用 JSON-RPC 2.0，定义请求、响应、通知、生命周期和 primitives 的语义。传输层负责连接、消息承载、分帧以及传输相关的授权。

```text
数据层：JSON-RPC 2.0 + lifecycle + tools/resources/prompts
传输层：stdio 或 Streamable HTTP
```

分层的好处很实际：同一组 JSON-RPC 方法可以跑在不同传输上，但身份凭证和关闭方式要按传输处理。

### MCP 生命周期

稳定规范的顺序是：

1. Client 先发 `initialize`，携带 `protocolVersion`、`capabilities` 和实现信息。
2. Server 返回选定的协议版本、自己的 `capabilities` 和实现信息；无法协商兼容版本就终止连接。
3. Client 发 `notifications/initialized`，表示初始化完成。
4. 进入 operation 阶段。双方只能使用协商成功的能力；没有协商 tools，就不能发 `tools/list` 或 `tools/call`。
5. 结束时关闭传输。规范没有额外的通用 shutdown RPC：stdio 关闭子进程输入并等待退出；HTTP 关闭对应会话或连接资源。

能力协商不是一次“功能清单展示”。它是运行期契约。列表变化通知也只有在对应的 `listChanged` 子能力已经声明时才能使用。

### 标准传输

2025-11-25 稳定规范定义两个标准传输：

- `stdio`：Client 启动本地 Server 子进程，通过 stdin/stdout 交换 JSON-RPC 消息。stdout 不能混入日志。
- `Streamable HTTP`：Client 用 HTTP POST/GET 访问单一 MCP endpoint，Server 可以选择用 SSE 承载流式消息。

HTTP+SSE 是 2024-11-05 的旧传输，已被 Streamable HTTP 取代。SSE 仍可能是 Streamable HTTP 的承载方式，但“HTTP+SSE”不能再写成当前独立标准传输。

### Server primitives 的控制角色

- Tools 是模型控制（model-controlled）的可调用动作。模型可以提出调用，应用仍可要求确认或拒绝。
- Resources 是应用控制（application-driven）的上下文数据，以 URI 标识；Host 决定选择、搜索或自动纳入哪些资源。
- Prompts 是用户控制（user-controlled）的可复用消息模板，通常由用户在界面中显式选择。

三个 primitives 都要先通过能力协商，再按 `*/list` 发现。Resources 用 `resources/read` 读取，Prompts 用 `prompts/get` 获取，Tools 才用 `tools/call` 执行动作。把资源当工具会放大权限，把工具当资源则掩盖副作用。

### 信任与授权

Server 的描述、资源内容、工具结果和错误消息都是不可信输入。Host 要做输出大小限制、内容过滤、URI 与 MIME 检查，不能让 Server 返回的文字绕过本地策略。

治理至少覆盖这些边界：

- 只向 Server 暴露完成任务所需的最小权限和数据范围。
- 对 resource URI 做 scheme、host、path 和租户范围校验；对工具参数做 schema 与业务输入校验。
- 发送消息、删除数据、支付等敏感动作在执行前取得用户同意，并展示冻结后的动作参数。
- HTTP 传输按 MCP 授权规范使用面向目标资源的令牌；Server 必须校验 token audience。
- stdio 不套用 HTTP 授权流程，凭证通常从受控环境或进程配置取得，且不写入模型上下文。
- 不得做 token passthrough：Client 收到的令牌不能原样转交给下游服务。Server 应使用只对下游受众有效的独立凭证。

协议授权是传输层能力，不会替代业务授权。即使 OAuth 成功，后端仍需检查用户是否能读取某个 URI、是否能创建该租户的工单。

## 4. 工具可靠性与副作用

### Schema 和结果契约

工具说明要包含适用场景、禁用场景、参数范围、返回结构、错误类型、是否有副作用和审批规则。JSON Schema 能约束形状，不能证明业务语义正确。

后端可把错误分成：参数错误、权限错误、业务拒绝、暂时性基础设施错误和结果不确定。只有明确可重试的暂时性错误才进入有上限、带退避的重试。

### 幂等键

幂等键应绑定一次具体业务动作，例如：

```text
tenant + action_type + business_object_id + normalized_arguments + request_generation
```

只用 `task_id:tool_name` 不足。同一任务里两次给不同收件人发送通知会冲突，而重放同一动作时又可能生成不同 task。键、唯一约束、参数快照和执行结果要一起保存。

## 5. 设计示例的事实边界

下面是设计示例，未在本仓库执行或做集成验证：

```text
Host 收到“创建工单”
  → 对应 Client 已完成 initialize 和 tools 能力协商
  → tools/list 找到 create_ticket
  → 模型提出 arguments
  → Host 校验 schema、租户权限和风险
  → 用户确认冻结后的参数
  → 使用动作级幂等键调用 tools/call
  → 校验工具结果与业务状态
  → 成功后写审计并回填模型
```

如果把这段写进项目经历，必须另有源码、测试输出和 trace 支持。只有设计文档时，应称为“设计”或“练习”。

## 6. 面试自检

1. 为什么一个 Host 需要为每个 Server 建独立 Client？
2. `initialize` 返回后，为什么还要发 `notifications/initialized`？
3. Streamable HTTP 和旧 HTTP+SSE 的关系是什么？
4. Tools、Resources、Prompts 的控制权有何不同？
5. 为什么 MCP Server 的输出也是不可信输入？
6. HTTP 授权、stdio 凭证和业务授权分别解决什么问题？
