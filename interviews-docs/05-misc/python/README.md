# Python 后端面试练习

这组资料面向 AI Agent / Python 后端技术面试。目标不是把 Python 写成百科，而是让你能在项目深挖、运行时追问、工程实践题里给出清楚、可复述、能落到代码的回答。

建议每个专题按[统一练习协议](../../practice-protocol.md)完成一次：先独立作答或编码，再执行代码/检查证据，最后做迁移题和延迟复测。这里主要服务两项能力：**C01**（写、测、调试并解释 Python）和 **C07**（交付 Python 后端）；容器或类型等基础专题是它们的支撑，不会因为读完就自动成为 P0。

## 优先级

| 优先级 | 专题 | 面试价值 |
| --- | --- | --- |
| P0 | [asyncio 与同步阻塞](07-asyncio-blocking.md) | 判断你是否真的理解 async 后端、Agent 工具调用和 I/O 调度 |
| P1 | [thread、process 和 GIL 的边界](08-thread-process-gil.md) | 高频追问：并发模型、CPU/IO 任务选择、性能瓶颈 |
| P0 | [FastAPI 请求生命周期和依赖注入](10-fastapi-lifecycle-di.md) | Python 后端项目深挖常见入口 |
| P1 | [typing、dataclass、Pydantic](05-typing-dataclass-pydantic.md) | AI 后端数据契约、配置、schema 校验常问 |
| P0 | [pytest、mock、fixture](09-pytest-mock-fixture.md) | 证明工程质量和可测试性 |
| P1 | [异常处理](06-exceptions.md) | 错误边界、重试、可观测性、接口语义基础 |
| P1 | [decorator、context manager](04-decorator-context-manager.md) | 框架、依赖、资源管理和横切逻辑基础 |
| P1 | [iterator、generator](03-iterator-generator.md) | 流式处理、懒加载、内存控制基础 |
| P1 | [引用、浅拷贝、深拷贝](02-reference-copy.md) | 可变对象、默认参数、数据污染高频坑 |
| P2 | [list、dict、set、tuple](01-containers.md) | 基础快问快答和复杂度表达 |
| P2 | [packaging、虚拟环境和依赖锁定](11-packaging-venv-lock.md) | 交付、复现、线上问题排查 |

## 复习路线

1. 先过 P0：`asyncio`、FastAPI、pytest；各做一次可执行证据任务。
2. 再过 P1：GIL/并发、typing/Pydantic、异常、decorator/context manager、iterator/generator、copy。
3. 面试前 30 分钟只扫每篇的 `一句话答案`、`易错点` 和 `自测题`。
4. 如果被问跨栈选择，配合阅读 [Python vs NodeJS](../python-vs-nodejs.md)。

## 回答原则

- 先给结论，再解释机制，不要一开始陷进实现细节。
- 每个回答都尽量落到项目场景：API、Agent tool call、后台任务、测试、配置或部署。
- 遇到性能题先区分 I/O-bound、CPU-bound、memory-bound，再选择 async、thread、process 或外部队列。
- 不确定版本细节时说明基线：Python 3.11+，常见现代后端项目。
