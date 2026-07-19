# HTTP 生命周期

## 一句话答案

Node HTTP 请求从 TCP 连接进入，经过解析 request、读取 headers/body、路由和业务处理、写 response、处理 keep-alive 或关闭连接；框架只是把这条链路包装成 middleware、handler 和 error handler。

## 核心机制

Node 的 `http` 模块基于 socket 处理 HTTP。连接建立后，请求头被解析成 `IncomingMessage`，响应由 `ServerResponse` 写出。请求 body 是 stream，不会天然一次性出现在对象里；Express/Fastify 等框架会通过 body parser 或内置机制把它解析成 JSON、form 或 buffer。

典型框架生命周期是：全局 middleware 或 hook、路由匹配、参数解析、鉴权、schema 校验、业务 handler、响应序列化、错误处理。HTTP keep-alive 让同一个 TCP 连接复用多个请求，提升性能，但也需要合理设置 timeout，避免慢连接占用资源。

面试里要能说明：headers 先到，body 可能分块到达；response 可以流式写出；一旦开始写 headers，很多错误就不能再改状态码。

## 常见追问

- request body 为什么是 stream？因为 body 可能很大或分块到达，不能假设一次性读完。
- keep-alive 的价值是什么？复用 TCP 连接，减少握手成本。
- headers sent 后还能改 status code 吗？通常不能，响应头已经发出。
- 框架错误处理中间件处理不了什么？已经脱离 Promise 链、未 await 的异步错误，或响应已开始后的错误。

## 代码例子

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  res.writeHead(404);
  res.end("not found");
});

server.listen(3000);
```

```js
async function readBody(req) {
  let body = "";
  for await (const chunk of req) {
    body += chunk;
  }
  return JSON.parse(body || "{}");
}
```

## 易错点

- 以为 body 已经自动解析，忽略 stream 和大小限制。
- 不设置 request timeout、headers timeout、body size limit，容易被慢请求拖住。
- 异步 handler 里错误未 return/await，框架错误处理拿不到。
- response 已经开始写出后才发现业务错误，状态码无法正常表达。

## 实战判断

回答项目经验时可以把框架抽象还原成 HTTP 生命周期：入口做 trace 和限流，body parser 有大小限制，schema 校验在业务前，handler 调服务层，错误统一转响应，长响应或文件走 stream，服务级 timeout 防止连接无限占用。

## 自测题

1. Node 中 request body 为什么不能默认当普通对象用？
   答：它是 stream，需要框架或代码读取并解析。
2. keep-alive 解决什么问题？
   答：复用 TCP 连接，减少连接建立成本。
3. headers sent 后错误处理有什么限制？
   答：通常不能再修改状态码和响应头，只能结束或销毁连接。

## 参考链接

- [Node.js HTTP](https://nodejs.org/api/http.html)
- [Anatomy of an HTTP Transaction](https://nodejs.org/en/learn/modules/anatomy-of-an-http-transaction)
