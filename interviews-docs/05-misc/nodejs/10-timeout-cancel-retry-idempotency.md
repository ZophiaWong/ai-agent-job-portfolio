# 超时、取消、重试和幂等性

## 一句话答案

可靠的异步调用必须同时考虑 timeout、cancellation、retry 和 idempotency：超时控制等待上限，取消释放资源，重试处理瞬时失败，幂等性保证重复请求不会造成重复副作用。

## 核心机制

Timeout 是调用方给外部依赖设置的最大等待时间，避免请求无限挂起。Cancellation 是把“不再需要结果”的信号传给下游，让 fetch、stream、数据库查询或后台任务尽快停止。Node 和 Web API 常用 `AbortController` / `AbortSignal` 表达取消。

Retry 只适合瞬时错误，例如网络抖动、429、部分 5xx。重试必须有次数上限、退避、最好加 jitter，避免把下游打崩。不是所有请求都能安全重试：GET、幂等 PUT/DELETE 通常更安全；POST 创建资源、扣款、发送消息等需要 idempotency key 或业务去重。

在 Agent tool call 场景，重试还要考虑副作用：搜索可以重试，发邮件或下单必须谨慎。

## 常见追问

- timeout 和 cancellation 是一回事吗？不是，timeout 是触发条件，cancellation 是传播停止信号。
- 哪些错误适合重试？瞬时网络错误、超时、限流、部分服务端错误；参数错误不应重试。
- 为什么重试要退避？避免失败时所有客户端立刻同时重试，扩大故障。
- 幂等性怎么实现？业务唯一键、idempotency key、去重表、状态机保护。

## 代码例子

```js
async function fetchWithTimeout(url, ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);

  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}
```

```js
import { setTimeout as sleep } from "node:timers/promises";

function retryable(error) {
  if (error?.name === "AbortError") return false;
  if (["ECONNRESET", "ETIMEDOUT", "EAI_AGAIN"].includes(error?.code)) return true;
  return error?.status === 429 || (error?.status >= 500 && error?.status < 600);
}

function retryAfterMs(value, now = Date.now()) {
  if (!value) return 0;
  const seconds = Number(value);
  if (Number.isFinite(seconds)) return Math.max(0, seconds * 1000);
  const at = Date.parse(value);
  return Number.isNaN(at) ? 0 : Math.max(0, at - now);
}

async function retry(operation, { attempts = 3, baseDelayMs = 100, signal } = {}) {
  // `signal` is an AbortSignal supplied by the request/deadline owner.
  if (!Number.isInteger(attempts) || attempts < 1) throw new RangeError("attempts >= 1");

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    signal?.throwIfAborted(); // do not invoke an operation after pre-abort
    try {
      return await operation({ signal }); // fetch/client must pass this signal downstream
    } catch (error) {
      if (signal?.aborted) throw signal.reason ?? error;
      if (!retryable(error)) throw error;
      if (attempt === attempts) throw error; // never sleep after the final failure

      const exponential = baseDelayMs * 2 ** (attempt - 1);
      const fullJitter = Math.floor(Math.random() * exponential);
      // Respect a server Retry-After value; otherwise use exponential backoff + jitter.
      const delayMs = Math.max(fullJitter, retryAfterMs(error.retryAfter));
      await sleep(delayMs, undefined, { signal });
    }
  }
}
```

`Retry-After` can be seconds or an HTTP date; capture it from a 429/503 response in the client error object. Abort is
not retryable: it propagates to the operation and to the backoff sleep. A production caller should also bound the
whole request by a deadline and attach an idempotency key before retrying a write.

## 易错点

- 只设置服务端总超时，不给每个外部依赖设置 timeout。
- 超时后不取消底层请求，导致资源继续占用。
- 对不可幂等操作无脑重试，造成重复写入或重复副作用。
- 无限重试或固定间隔重试，故障时放大流量。

## 实战判断

回答时可以给出策略：每个外部调用都有 timeout 和 AbortSignal；只对明确瞬时失败重试；重试有预算、指数退避和 jitter；写操作必须有 idempotency key 或业务去重；调用链上层取消时向下游传播取消信号。

## 自测题

1. timeout 后为什么还要 cancellation？
   答：否则调用方不等了，但底层请求可能仍在运行和占资源。
2. 哪类操作不能随便重试？
   答：有副作用且不幂等的写操作，如扣款、发消息、创建资源。
3. 重试为什么要有上限和退避？
   答：控制延迟和流量，避免把下游故障放大。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)用 fake operation 依次抛 503、429（带 `Retry-After`）、400 和 abort，
记录调用次数与等待决策。若无 Node，手动 trace retryable 分类、attempts 边界、pre-abort 和最后一次失败路径。
可检查结果：四行重试决策表，证明 400/abort 不重试且最后一次失败没有 sleep。

## 参考链接

- [Node.js Timers Promises API](https://nodejs.org/api/timers.html#timers-promises-api)
- [Node.js Global `fetch`](https://nodejs.org/api/globals.html#fetch)

访问日期：2026-07-19。
