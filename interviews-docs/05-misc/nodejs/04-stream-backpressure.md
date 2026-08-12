# stream 和 backpressure

## 一句话答案

Stream 用分块方式处理数据，避免一次性把大文件或大响应放进内存；backpressure 是下游处理不过来时向上游施压，让读取速度降下来，防止内存无限增长。

## 核心机制

Node stream 常见类型有 Readable、Writable、Duplex、Transform。Readable 产生数据，Writable 消费数据，Transform 一边读一边写，例如压缩、解压、解析、加密。`pipe()` 会把可读流连接到可写流，并自动处理基本的 backpressure。

Writable 的 `write(chunk)` 返回 `false` 表示内部 buffer 达到 highWaterMark，上游应该暂停写入，等 `drain` 事件后再继续。如果忽略这个信号，生产速度大于消费速度时，内存会不断堆积。

后端常见场景包括文件上传下载、日志处理、代理上游响应、SSE/token streaming、大 CSV/JSONL 处理。Stream 的价值是稳定内存占用和降低首字节延迟。

## 常见追问

- stream 相比 buffer 的优势是什么？分块处理，内存稳定，可以边读边写。
- backpressure 怎么发生？下游写入缓冲区满，上游继续写会堆积数据。
- `pipe` 是否自动处理错误？基本数据流和 backpressure 会处理，但错误处理推荐用 `pipeline`。
- highWaterMark 是什么？内部缓冲区水位阈值，不是硬性内存上限。

## 代码例子

```js
import { createReadStream, createWriteStream } from "node:fs";
import { pipeline } from "node:stream/promises";

await pipeline(
  createReadStream("input.log"),
  createWriteStream("copy.log"),
);
```

```js
function writeMany(writable, chunks) {
  let index = 0;

  function write() {
    while (index < chunks.length) {
      if (!writable.write(chunks[index++])) {
        writable.once("drain", write);
        return;
      }
    }
    writable.end();
  }

  write();
}
```

## 易错点

- 用 `fs.readFile` 读取超大文件，导致内存峰值过高。
- 手动监听 `data` 事件后无视 `pause/resume` 或 backpressure。
- 只处理 `end`，不处理 `error`，流中途失败时请求挂住。
- 把 stream 转成完整字符串再处理，失去流式优势。

## 实战判断

如果数据小且需要完整解析，用 buffer 简单。如果数据大、响应要边生成边发送、或代理上游服务，用 stream。生产服务里优先使用 `pipeline`，因为它能统一处理完成、错误和销毁，减少资源泄漏。

## 自测题

1. backpressure 的本质是什么？
   答：消费者处理不过来时，把压力反馈给生产者，让生产速度降低。
2. `writable.write()` 返回 false 表示什么？
   答：内部缓冲区达到水位，应该等 `drain` 后再继续写。
3. 为什么推荐 `pipeline`？
   答：它统一处理流连接、错误传播和资源销毁。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)用小输入运行 `pipeline` 示例并确认生成 `copy.log`；同时让
`write()` 一次返回 false。若无 Node，手动 trace `write=false → once("drain") → 继续写 → end`。
可检查结果：`copy.log` 内容或这条 backpressure 状态转换记录。

## 参考链接

- [Node.js Streams](https://nodejs.org/api/stream.html)
- [Backpressuring in Streams](https://nodejs.org/en/learn/modules/backpressuring-in-streams)

访问日期：2026-07-19。
