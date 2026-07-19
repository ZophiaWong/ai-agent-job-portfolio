# event loop

## 一句话答案

NodeJS 的 event loop 是单主线程上的异步调度机制，负责把 timer、I/O callback、check、close callback 等任务分阶段执行；它让大量 I/O 并发成为可能，但不会让 CPU 密集代码自动并行。

## 核心机制

NodeJS 运行 JavaScript 的主线程一次只执行一段 JS。异步 I/O 由操作系统、libuv 或线程池协助完成，完成后 callback 被放回 event loop 对应阶段。常见阶段包括 timers、pending callbacks、poll、check、close callbacks。`setTimeout` 的回调在 timers 阶段，`setImmediate` 在 check 阶段，网络和文件 I/O 回调主要与 poll 阶段相关。

每个阶段执行 callback 时，JS 调用栈必须先清空。Promise microtask 和 `process.nextTick` 会在阶段切换之间被清理，因此大量 microtask 可能饿死后续 I/O。面试里不需要死背所有细节，但必须能说清楚：event loop 负责调度，JS 执行仍是单线程，阻塞 CPU 会卡住所有请求。

**版本边界：**从 **libuv 1.45.0（Node.js 20）** 起，每轮 event loop 的 timers 在 **poll 阶段之后**运行；
较早版本会在 poll 前后处理 timers（为兼容性，1.45.0 在进入 event loop 前仍会先跑一次）。因此不要把
`setTimeout(..., 0)` 与 `setImmediate()` 的相对顺序写成跨版本、跨 I/O 上下文的保证。

## 常见追问

- Node 是单线程吗？JS 执行主线程是单线程，但 libuv 线程池、OS I/O、worker threads 都可能参与。
- `setTimeout(fn, 0)` 会立即执行吗？不会，只是尽快进入 timers 阶段，仍要等当前栈和 microtask 清空。
- CPU 密集循环会怎样？阻塞主线程，event loop 无法处理其他 callback。
- 为什么 Node 适合 I/O 高并发？等待 I/O 时主线程不阻塞，可以继续处理其他就绪任务。

## 代码例子

```js
console.log("start");

setTimeout(() => console.log("timeout"), 0);
setImmediate(() => console.log("immediate"));
Promise.resolve().then(() => console.log("promise"));

console.log("end");
```

```js
const start = Date.now();
while (Date.now() - start < 1000) {
  // CPU-bound work blocks the event loop.
}
console.log("other callbacks waited for this loop");
```

## 易错点

- 把 Node 的 I/O 并发误解成 JS 多线程并行。
- 在 HTTP handler 中跑大循环、压缩大文件或同步加密，导致整个进程响应变慢。
- 过度依赖 `setTimeout(..., 0)` 顺序，忽略 I/O 上下文和事件循环阶段差异。
- 大量递归创建 Promise microtask，导致 timer 和 I/O callback 长时间得不到执行。

## 实战判断

Node 后端适合 I/O 密集服务、API gateway、BFF、实时连接和流式代理。遇到 CPU-bound 工作，应考虑 worker threads、child process、独立服务或原生扩展。面试回答要把 event loop 与可靠性连接起来：任何同步阻塞都会影响同进程所有请求。

## 自测题

1. event loop 解决的核心问题是什么？
   答：在单主线程 JS 执行模型下调度异步 I/O 回调，让 I/O 等待期间可以处理其他任务。
2. Node 是否能自动并行执行 CPU 密集 JS？
   答：不能，CPU-bound JS 会阻塞主线程，需要 worker 或进程隔离。
3. `setTimeout(fn, 0)` 为什么不是立即执行？
   答：它要等当前调用栈、microtask 和事件循环阶段推进后才能运行。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)先独立解释示例的 `start/end/promise` 顺序，再运行
`node event-loop-evidence.mjs` 记录实际输出和 `node -p process.versions.uv`。若无 Node，手动检查
libuv 1.45.0/Node 20 的 timers-after-poll 边界，并写出两种 I/O 上下文为何不能保证 timer/immediate 顺序。
可检查结果：版本号、输出顺序或带版本前提的顺序解释。

## 参考链接

- [Node.js Event Loop Guide](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [libuv Design Overview](https://docs.libuv.org/en/v1.x/design.html)

访问日期：2026-07-19。
