# Node 进程、worker 和 child process

## 一句话答案

Node 主进程适合调度 I/O，worker threads 适合在同一进程内跑 CPU 密集 JS 并共享部分内存，child process 适合更强隔离或调用外部程序；选择时看隔离性、通信成本和故障影响范围。

## 核心机制

单个 Node 进程有一个主 JS 线程和 event loop。对于 I/O-bound 服务，一个进程就能处理大量并发连接，但 CPU-bound 工作会阻塞 event loop。

`worker_threads` 在同一进程内创建独立 JS 线程，每个 worker 有自己的 event loop，可以通过 message passing 交换数据，也可以使用 SharedArrayBuffer 做共享内存。它适合图像处理、压缩、解析大数据、CPU-heavy 转换等需要并行的 JS 工作。

`child_process` 创建独立 OS 进程，可以运行 Node 脚本或外部命令。它隔离更强，崩溃影响较小，但启动和 IPC 成本更高。生产里也常用多进程部署或容器编排横向扩展。

## 常见追问

- worker thread 和 child process 最大区别？worker 在同一进程内，child 是独立进程，隔离更强。
- worker 能共享对象吗？普通对象通过结构化克隆或 transfer，SharedArrayBuffer 可共享内存但要处理同步。
- 为什么不用 worker 处理所有请求？线程创建和通信有成本，I/O 请求通常 event loop 足够。
- child process 适合什么？调用外部命令、隔离不可信任务、跑独立 CPU 作业。

## 代码例子

```js
// main.mjs
import { Worker } from "node:worker_threads";

const worker = new Worker(new URL("./worker.mjs", import.meta.url), {
  workerData: 1_000_000,
});

worker.on("message", (result) => console.log(result));
worker.on("error", (error) => console.error(error));
```

```js
// worker.mjs
import { parentPort, workerData } from "node:worker_threads";

const result = Array.from({ length: workerData }, (_, i) => i)
  .reduce((sum, n) => sum + n, 0);

parentPort.postMessage(result);
```

## 易错点

- 用 worker 处理普通数据库/HTTP I/O，增加复杂度但收益很小。
- 给 worker 或 child 传超大对象，序列化成本超过并行收益。
- 不处理 worker error/exit，后台失败悄悄丢失。
- 在 child process 中执行拼接出来的 shell 命令，引入注入风险。

## 实战判断

如果任务是等待外部 API，用 Promise 并发、stream 或连接池即可。如果任务是 CPU-heavy JS，考虑 worker threads。如果要运行外部程序、隔离崩溃或权限边界，考虑 child process。高可用服务还要用进程管理器、容器或平台能力做多实例部署。

## 自测题

1. worker threads 主要解决什么问题？
   答：把 CPU 密集 JS 工作放到独立线程，避免阻塞主 event loop。
2. child process 的主要优势是什么？
   答：进程级隔离强，可以运行外部程序或隔离故障。
3. 为什么传大对象给 worker 可能不划算？
   答：结构化克隆或 IPC 序列化成本可能抵消并行收益。

## 参考链接

- [worker_threads](https://nodejs.org/api/worker_threads.html)
- [child_process](https://nodejs.org/api/child_process.html)
