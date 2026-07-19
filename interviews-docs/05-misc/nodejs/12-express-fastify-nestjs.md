# Express、Fastify 或 NestJS 的基本工作方式

## 一句话答案

Express、Fastify、NestJS 都是在 Node HTTP 生命周期上提供框架抽象：Express 轻量 middleware 链，Fastify 强调 schema 和性能，NestJS 强调模块化、依赖注入和装饰器架构。面试重点是知道框架如何组织请求，而不是只会写路由。

## 核心机制

Express 的核心是 middleware pipeline。请求按注册顺序经过 middleware 和 route handler，错误通过 `next(error)` 进入错误处理中间件。**仅从 Express 5 开始**，route handler 或 middleware 返回的 Promise 若 reject（成为 **rejected Promise**）或 throw，框架会自动调用 `next(value)`；Express 4 不应假设这个行为，仍要显式把异步错误交给 `next`（或使用已验证的包装器）。它生态成熟、灵活，但 schema、类型和结构约束更多靠团队规范。

Fastify 以 plugin、hook、schema validation 和 serialization 为核心。它鼓励为路由声明 schema，既能做输入校验，也能优化响应序列化。Fastify 的封装上下文让插件边界更清晰。

NestJS 是更重的应用框架，借鉴 Angular 风格，使用 module、controller、provider、decorator 和 dependency injection。它适合大型团队和复杂业务结构，但抽象层更多，理解底层 HTTP 和 DI 生命周期很重要。

## 常见追问

- middleware 顺序重要吗？重要，请求按注册顺序执行，错误处理也依赖顺序。
- Fastify 为什么常被认为性能好？schema 驱动校验和序列化、较低开销的路由和封装设计。
- NestJS 的 provider 是什么？由 DI 容器管理的可注入服务、repository、client 等对象。
- 框架能解决 async 错误吗？Express 5 能转发返回 Promise 的 rejection；任何版本都要求 Promise 留在框架链路中，脱离链路的后台任务仍须自行处理。

## 代码例子

```js
// requires express
import express from "express";

const app = express();

app.use(express.json());
app.get("/health", (req, res) => res.json({ ok: true }));
app.use((error, req, res, next) => {
  res.status(500).json({ error: error.message });
});
```

```js
// requires fastify
import Fastify from "fastify";

const app = Fastify();

app.get("/health", {
  schema: {
    response: { 200: { type: "object", properties: { ok: { type: "boolean" } } } },
  },
}, async () => ({ ok: true }));
```

## 易错点

- Express middleware 顺序写错，鉴权、body parser 或错误处理不生效。
- async handler 错误没有返回到框架，导致 unhandled rejection。
- 在 NestJS provider 中保存 request-scoped 状态，造成并发污染。
- 只会用框架 API，无法解释底层 HTTP、stream、timeout 和错误边界。

## 实战判断

小服务、BFF、快速原型用 Express 足够；追求 schema、性能和插件边界可以选 Fastify；大型团队、复杂模块和 DI 结构明显时选 NestJS。面试回答可以强调：框架选择要看团队规模、约束需求、性能瓶颈和生态，不是简单比较谁更先进。

## 自测题

1. Express 的核心执行模型是什么？
   答：按注册顺序执行 middleware 和 route handler。
2. Fastify 的 schema 有什么价值？
   答：输入校验、响应序列化优化和接口契约表达。
3. NestJS 适合什么场景？
   答：模块多、依赖复杂、团队需要统一架构约束的中大型服务。

## 参考链接

- [Express 5 Error Handling](https://expressjs.com/en/guide/error-handling/)
- [Fastify Documentation](https://fastify.dev/docs/latest/)
- [NestJS Documentation](https://docs.nestjs.com/)

访问日期：2026-07-19。
