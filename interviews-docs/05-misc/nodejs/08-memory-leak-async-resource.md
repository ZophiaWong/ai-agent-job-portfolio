# 内存泄漏与异步资源

## 一句话答案

Node 内存泄漏常见来源不是“忘记 free”，而是对象仍被引用：未清理 timer、listener、闭包、全局 cache、未结束 stream、未释放异步资源。排查要从引用链、堆快照和资源生命周期入手。

## 核心机制

V8 使用垃圾回收，只要对象不可达就能回收；泄漏意味着对象仍然从 root 可达。Node 服务长期运行，任何请求级对象如果被全局结构、timer、event listener、Promise 闭包或 AsyncLocalStorage 错误持有，都可能越积越多。

常见异步资源包括 socket、stream、timer、interval、EventEmitter listener、数据库连接、AbortController、文件句柄。它们不一定只占 JS heap，还可能占 native memory 或 OS 资源。因此排查时不能只看 heapUsed，也要看 RSS、句柄数、连接数和 event loop delay。

线上处理通常包括：限制 cache 大小、清理 listener、给 stream/error 路径做 destroy、请求结束后释放上下文、使用 heap snapshot 对比增长对象。

## 常见追问

- EventEmitter 泄漏有什么表现？同一 emitter 上 listener 越来越多，可能触发 MaxListenersExceededWarning。
- cache 为什么容易泄漏？无上限 Map 会持续持有 key/value，GC 无法回收。
- timer 为什么会泄漏？interval 持有回调和闭包变量，不 clear 就一直存活。
- 如何定位？观察指标、复现增长、heap snapshot diff、查引用链和资源生命周期。

## 代码例子

```js
const timers = new Set();

function startJob(jobId) {
  const timer = setInterval(() => {
    console.log("poll", jobId);
  }, 1000);
  timers.add(timer);
  return timer;
}

function stopJob(timer) {
  clearInterval(timer);
  timers.delete(timer);
}
```

```js
import { EventEmitter } from "node:events";

const bus = new EventEmitter();

function handleRequest(id) {
  const listener = () => console.log(id);
  bus.on("done", listener);
  return () => bus.off("done", listener);
}
```

## 易错点

- 把每个请求的数据放入全局 Map，没有 TTL 和容量限制。
- 对同一个 EventEmitter 每次请求都 `on`，请求结束不 `off`。
- stream 失败时没有 destroy，文件句柄或 socket 悬挂。
- 只看 JS heap，不看 RSS、句柄和外部资源。

## 实战判断

面试里可以按生命周期回答：请求级资源必须随请求结束释放，应用级 cache 必须有上限和淘汰策略，后台任务必须有取消和清理路径，所有 stream/socket/timer 都要处理 error 和 close。排查时用指标定位趋势，再用 heap snapshot 找引用链。

## 自测题

1. GC 语言为什么还会内存泄漏？
   答：对象仍然被可达引用持有，GC 不能回收。
2. MaxListenersExceededWarning 说明什么？
   答：同一 EventEmitter 上 listener 过多，可能存在未清理监听器。
3. cache 防泄漏的基本策略是什么？
   答：设置容量、TTL、淘汰策略，并避免用请求对象当长期 key。

## 参考链接

- [EventEmitter](https://nodejs.org/api/events.html)
- [Node.js Diagnostics: Memory](https://nodejs.org/en/learn/diagnostics/memory)
