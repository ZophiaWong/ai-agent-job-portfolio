# 测试、mock 和 integration test

## 一句话答案

Node 测试要分层：单元测试验证纯逻辑，mock 隔离外部依赖，integration test 覆盖路由、数据库、队列或第三方协议的真实协作；关键不是追求 mock 数量，而是让失败能说明真实问题。

## 核心机制

Node 现代项目可以使用内置 `node:test`，也可以使用 Jest、Vitest、Mocha 等测试框架。断言可以用 Node `assert` 或框架内置 expect。测试异步函数时必须 return/await Promise，否则测试可能提前结束，异步错误变成 unhandled rejection。

Mock 用于替代不可控依赖：HTTP API、时间、随机数、数据库、LLM 调用。过度 mock 会让测试只验证“实现按自己写的方式调用 mock”，而不是验证行为。Integration test 应尽量从公共接口进入，例如 HTTP 路由或 service API，并使用测试数据库、fake server 或容器化依赖。

对于 TypeScript 项目，还要确保测试运行路径与构建路径一致，避免 tsconfig、ESM/CJS、路径别名在测试和生产不一致。

## 常见追问

- async 测试最常见坑？忘记 await/return，测试在 Promise settle 前结束。
- mock 和 fake 区别？mock 关注调用断言，fake 是可工作的简化实现。
- integration test 是否一定打真实第三方？不一定，通常用本地 fake server 或契约测试。
- 为什么快慢测试要分开？单元测试快速反馈，integration test 覆盖协作但成本更高。

## 代码例子

```js
import test from "node:test";
import assert from "node:assert/strict";

async function add(a, b) {
  return a + b;
}

test("add", async () => {
  assert.equal(await add(1, 2), 3);
});
```

```js
class SearchService {
  constructor(client) {
    this.client = client;
  }

  async answer(query) {
    const result = await this.client.search(query);
    return result.text.trim();
  }
}

test("service normalizes the response from its injected client", async () => {
  const fakeClient = {
    async search(query) {
      return { text: ` result:${query} ` };
    },
  };
  const service = new SearchService(fakeClient);

  assert.equal(await service.answer("rag"), "result:rag");
});
```

这里 fake 只替代边界依赖；断言经过生产 `SearchService`，而不是直接调用 fake。若需要确认 HTTP
wire contract，再让 integration test 从路由或公开 service API 进入，并接本地 fake server。

## 易错点

- 异步测试没有 await，失败不会落到测试框架。
- mock 过度绑定内部调用顺序，重构实现就大量失败。
- integration test 不清理数据，测试之间互相污染。
- 测试环境和生产环境模块系统不同，线上才暴露 ESM/CJS 问题。

## 实战判断

后端项目可以保持测试金字塔：多写纯函数和服务层单元测试，关键路由做 integration test，少量端到端测试覆盖真实依赖。对 LLM/Agent 项目，推荐把模型调用包成接口，用 fake 固定响应，再单独做少量真实调用评测。

## 自测题

1. async 测试为什么必须 await 或 return Promise？
   答：否则测试函数会提前结束，异步失败不会被框架捕获。
2. mock 的主要风险是什么？
   答：测试过度耦合实现细节，不能发现真实集成问题。
3. integration test 的价值是什么？
   答：覆盖多个组件按真实接口协作，发现单元测试发现不了的问题。

## 参考链接

- [Node.js Test Runner](https://nodejs.org/api/test.html)
- [Node.js assert](https://nodejs.org/api/assert.html)

访问日期：2026-07-19。
