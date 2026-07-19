# Node.js 面试练习

这组资料面向 AI/Python 后端候选人的跨栈工程补充。目标是让你能解释 NodeJS 运行时、TypeScript 类型、HTTP 服务和异步错误处理，而不是把 Node 生态背成大全。

建议先理解 event loop 和 Promise 错误传播，再看 HTTP、超时取消重试和 stream/backpressure。它们最容易和真实项目深挖连接起来。

本系列使用[统一练习协议](../../practice-protocol.md)。能力 C11（Node.js、TypeScript 与跨运行时
取舍）的**默认目标为 2**：能在给定版本、负载和失败约束下讲清楚一个正确边界，并完成最小可检查
示例；框架名和冷门 API 不是默认背诵目标。

## 优先级

| 优先级 | 专题 | 面试价值 |
| --- | --- | --- |
| P0 | [event loop](01-event-loop.md) | Node 运行时最核心的追问入口 |
| P0 | [Promise、async/await 和错误传播](03-promise-async-await-errors.md) | 线上异常、unhandled rejection、并发任务处理高频 |
| P0 | [HTTP 生命周期](09-http-lifecycle.md) | 后端服务基本功，能连接 Express/Fastify/NestJS |
| P0 | [超时、取消、重试和幂等性](10-timeout-cancel-retry-idempotency.md) | 外部 API、Agent tool call、可靠性常问 |
| P0 | [stream 和 backpressure](04-stream-backpressure.md) | 大文件、代理、日志、响应流场景高频 |
| P1 | [microtask 和 task](02-microtask-task.md) | 解释 Promise、timer、nextTick 顺序 |
| P1 | [TypeScript 类型收窄、泛型和结构化类型](06-typescript-types.md) | TS 工程质量和 API 契约基础 |
| P1 | [Node 进程、worker 和 child process](07-process-worker-child-process.md) | 并发、并行、隔离和 CPU 任务选择 |
| P1 | [内存泄漏与异步资源](08-memory-leak-async-resource.md) | 线上排查和稳定性 |
| P2 | [CommonJS 与 ESM](05-commonjs-esm.md) | 模块系统、构建和包兼容常问 |
| P2 | [测试、mock 和 integration test](11-testing-mock-integration.md) | C11 默认目标 2 的可检查工程证据 |
| P2 | [Express、Fastify 或 NestJS 的基本工作方式](12-express-fastify-nestjs.md) | 框架理解和项目表达 |

## 复习路线

1. 先过 P0：event loop、Promise 错误、HTTP、超时取消重试、stream/backpressure。
2. 再补 P1：microtask/task、TypeScript 类型、worker/process、内存泄漏。
3. 面试前速扫每篇的 `一句话答案`、`易错点` 和 `自测题`。
4. 被问 Python 与 Node 取舍时，配合阅读 [Python vs NodeJS](../python-vs-nodejs.md)。

## 回答原则

- 先说 Node 是单主线程事件循环模型，再补充 libuv、线程池和 worker 的边界。
- 讨论并发时区分 I/O concurrency 和 CPU parallelism。
- 讨论可靠性时主动提 timeout、cancellation、retry budget、idempotency。
- TypeScript 题不要只背语法，要落到 API contract、narrowing 和类型边界。

## 练习交付物

每篇按协议留下一个可检查结果：例如 event-loop 顺序解释、`AbortSignal` 取消路径、retry 分类表，或
服务通过 injected fake 的测试。若本机没有 Node，不伪造运行结果；改为记录代码结构检查和待在目标
Node 版本执行的命令。
