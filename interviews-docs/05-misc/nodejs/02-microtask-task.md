# microtask 和 task

## 一句话答案

Task 是 event loop 阶段中的宏任务回调，如 timer、I/O、setImmediate；microtask 是当前 JS 栈清空后、进入下一个阶段前优先执行的任务，如 Promise reaction；Node 里还要特别注意 `process.nextTick` 优先级更高。

## 核心机制

浏览器和 Node 都有 task 与 microtask 的概念，但 Node 还包含 `process.nextTick` queue。一次同步代码执行完后，Node 会先清空 nextTick queue，再清空 Promise microtask queue，然后继续 event loop 阶段。因此 `process.nextTick` 如果递归排队，会比 Promise 更容易饿死 I/O。

Promise 的 `.then/.catch/.finally` 和 `await` 后续部分会进入 microtask。Timer、I/O callback、`setImmediate` 是 task。Microtask 的设计目的是在当前异步边界尽快处理状态延续，例如 Promise 结果传播；但滥用 microtask 会让事件循环没有机会处理外部 I/O。

面试中最重要的不是背输出顺序，而是解释“同步代码先执行，microtask 在当前 tick 末尾尽快执行，task 按 event loop 阶段执行”。

## 常见追问

- `await` 后面的代码什么时候执行？当前 awaited Promise settle 后，作为 microtask 继续执行。
- `process.nextTick` 和 Promise 谁先？Node 中 nextTick queue 通常先于 Promise microtask。
- microtask 会不会阻塞 I/O？大量连续 microtask 会推迟 event loop 进入后续阶段。
- `setImmediate` 和 `setTimeout(0)` 顺序固定吗？不总是固定，取决于调用上下文和 event loop 阶段。

## 代码例子

```js
console.log("sync 1");

process.nextTick(() => console.log("nextTick"));
Promise.resolve().then(() => console.log("promise"));
setTimeout(() => console.log("timeout"), 0);

console.log("sync 2");
```

```js
async function run() {
  console.log("a");
  await Promise.resolve();
  console.log("b");
}

run();
console.log("c");
// a, c, b
```

## 易错点

- 以为 Promise callback 和 timer 一样都是普通 task。
- 滥用 `process.nextTick` 做递归调度，导致 I/O starvation。
- 只背某段代码输出顺序，无法解释为什么在 I/O callback 中顺序可能变化。
- 用 microtask 承载长计算，阻塞后续请求。

## 实战判断

如果只是把当前调用栈后的状态传播出去，Promise microtask 很合适。如果要让 I/O 和 timer 有机会执行，不要用无限 microtask 链；可以使用 `setImmediate` 或分批调度。线上排查延迟时，要关注是否有同步 CPU、nextTick 递归或 Promise 链过长。

## 自测题

1. Promise `.then` 属于 task 还是 microtask？
   答：microtask。
2. Node 中 `process.nextTick` 和 Promise microtask 谁通常先执行？
   答：`process.nextTick` queue 先清空。
3. 大量 microtask 的风险是什么？
   答：推迟 event loop 进入 I/O、timer 等阶段，造成 starvation。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)运行本页第一个片段并记录 `sync 1/sync 2/nextTick/promise/timeout`
的队列顺序。若无 Node，手动 trace 同步栈、nextTick queue、Promise microtask queue 和 timers 的出队过程。
可检查结果：一张四步队列 trace，且说明递归 nextTick 为什么会饿死 I/O。

## 参考链接

- [Understanding process.nextTick](https://nodejs.org/en/learn/asynchronous-work/understanding-processnexttick)
- [Understanding setImmediate](https://nodejs.org/en/learn/asynchronous-work/understanding-setimmediate)

访问日期：2026-07-19。
