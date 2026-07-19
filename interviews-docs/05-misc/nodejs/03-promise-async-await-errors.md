# Promise、async/await 和错误传播

## 一句话答案

`async/await` 是 Promise 的语法糖：`async` 函数总是返回 Promise，函数内 throw 会变成 rejected Promise，`await` rejected Promise 会抛异常；面试重点是错误必须被 await、return 或 catch，否则会变成 unhandled rejection。

## 核心机制

Promise 有 pending、fulfilled、rejected 三种状态。一旦 settle 就不可再改变。`.then` 返回新 Promise，回调中 throw 会让新 Promise rejected，返回值会作为 fulfilled value，返回另一个 Promise 会发生展开。

`async function` 内部的 `return value` 等价于返回 fulfilled Promise，`throw error` 等价于返回 rejected Promise。`await` 会暂停当前 async 函数，等待 Promise settle；如果 rejected，就像同步 throw 一样进入 `try/catch`。

并发处理时要知道 `Promise.all` 会 fail fast，任一 rejected 就整体 rejected；`Promise.allSettled` 会等待全部完成并返回每个结果。后端调用多个外部工具时，选择 all 还是 allSettled 体现错误策略。

## 常见追问

- `try/catch` 能捕获未 await 的 Promise 错误吗？不能，必须 await 或 return Promise 链。
- `async` 函数 throw 后外层怎么处理？外层要 `await` 并 `try/catch`，或 `.catch()`。
- `Promise.all` 的风险是什么？一个失败会整体失败，其他任务可能仍在运行但结果被忽略。
- unhandled rejection 为什么危险？错误脱离业务边界，可能只被进程级事件捕获，导致状态不确定。

### 版本与运行配置边界

以下进程行为以 **Node 15+，且当前 Node 26.x 默认 `--unhandled-rejections=throw`** 为例：没有被处理的
rejection 会按未捕获异常处理。它不是业务恢复机制；若用 CLI 改成 `warn`、`none` 或 `strict`，进程结果会
不同。无论版本或 flag，都应在路由、任务入口或调用方 `await`/`.catch()`，并只把
`process.on("unhandledRejection")` 当作记录和有序退出的最后一道诊断措施。

## 代码例子

```js
async function loadUser(id) {
  if (!id) throw new Error("missing id");
  return { id };
}

async function main() {
  try {
    await loadUser("");
  } catch (error) {
    console.error("handled:", error.message);
  }
}

main();
```

```js
async function bad() {
  try {
    Promise.reject(new Error("not awaited"));
  } catch {
    console.log("will not run");
  }
}

async function good() {
  try {
    await Promise.reject(new Error("awaited"));
  } catch {
    console.log("caught");
  }
}
```

## 易错点

- 在 Express handler 中调用 async 函数但不 return/await，错误绕过错误处理中间件。
- `Array.prototype.forEach` 搭配 async callback，以为外层会等待所有任务。
- 对多个外部调用无脑 `Promise.all`，没有 partial failure 策略。
- 只监听 `unhandledRejection`，但不在业务边界处理错误。

## 实战判断

可靠的 Node 后端会在每个异步边界明确处理错误：路由 handler return Promise，服务层区分可重试和不可重试错误，并发调用根据业务选择 all、allSettled 或带限流的队列。Agent tool call 失败时要保留上下文，不能只丢一个字符串错误。

## 自测题

1. `async` 函数里 throw 会发生什么？
   答：返回一个 rejected Promise。
2. `try/catch` 为什么抓不到未 await 的 Promise rejection？
   答：错误发生在异步 Promise 链中，未被当前同步控制流等待。
3. `Promise.allSettled` 适合什么场景？
   答：需要等待所有并发任务完成，并分别处理成功和失败结果。

## 参考链接

- [Node.js process unhandledRejection](https://nodejs.org/api/process.html#event-unhandledrejection)
- [Node.js CLI `--unhandled-rejections`](https://nodejs.org/api/cli.html#--unhandled-rejectionsmode)

访问日期：2026-07-19。
