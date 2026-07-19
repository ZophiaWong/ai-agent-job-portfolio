# 后端面试资料

后端题要回答出运行时行为、数据边界、失败处理和可验证证据。选择一个主题后，按
[统一练习协议](../practice-protocol.md)先独立作答和编码，再用运行结果或检查清单校验。

## 优先入口

- [Python 后端面试练习](../05-misc/python/README.md)：从 C01/C07 的 Python 基础到 asyncio、FastAPI、测试和交付证据。
- [Node.js 与 TypeScript 面试练习](../05-misc/nodejs/README.md)：C11 默认目标 2；运行时边界、可靠性、测试和框架取舍。
- [Python vs NodeJS](../05-misc/python-vs-nodejs.md)：以工作负载、运行时模型和团队约束做跨栈选择。
- [Python 后端工程实践](../../AI_Agent_System_Practical_Reference/Part_03_Python工程化与生产治理/08_Python后端视角的Agent工程实践.md)：服务边界、依赖、异步 I/O、配置与交付。
- [评测、监控、可观测性与 Bad Case 回流](../../AI_Agent_System_Practical_Reference/Part_03_Python工程化与生产治理/09_评测_监控_可观测性与BadCase回流.md)：指标、日志、trace 和问题闭环。
- [安全、权限、风控与 Human in the Loop](../../AI_Agent_System_Practical_Reference/Part_03_Python工程化与生产治理/10_安全_权限_风控与Human_in_the_loop.md)：权限、审计、幂等与高风险操作。

后端练习的规范答题路径是：先从服务边界和数据契约出发，再说明同步/异步 I/O、失败处理、
可观测性、测试与交付。跨语言取舍应围绕工作负载、运行时模型、团队约束和已有基础设施，
而不是只比较框架名称。

## 配套表达

- [项目设计模板与架构表达](../../AI_Agent_System_Practical_Reference/Part_04_项目与面试表达/11_项目设计模板与架构表达.md)
- [高频面试题与答题闭环](../../AI_Agent_System_Practical_Reference/Part_04_项目与面试表达/12_高频面试题与答题闭环.md)
- [项目证据索引](../../projects/README.md)
