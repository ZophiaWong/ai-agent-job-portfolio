# asyncio 与同步阻塞

## 一句话答案

`asyncio` 是单线程协作式并发，适合高并发 I/O，不会自动让阻塞代码变快；真正的关键是所有等待点都必须 `await` 非阻塞操作，否则一个同步阻塞调用就能卡住整个 event loop。

## 核心机制

Event loop 负责调度 coroutine、task、I/O 回调和 timer。`async def` 调用后得到 coroutine，只有被 `await`、`create_task()` 或事件循环驱动时才会执行。`await` 的意义是把控制权还给 event loop，让其他 task 可以继续运行。

如果在 async 函数里调用 `time.sleep()`、同步 HTTP client、同步数据库驱动或 CPU 密集计算，event loop 会被阻塞，其他请求也不能推进。正确做法是使用 async 版本库，例如 `httpx.AsyncClient`、async database driver；无法避免同步阻塞时，用 `asyncio.to_thread()` 或 executor 把阻塞 I/O 移出 event loop。

`asyncio` 不适合 CPU-bound 加速。CPU 密集任务应考虑 process pool、外部 worker，或能释放 GIL 的 native extension。

对一组彼此相关的并发子任务，Python 3.11+ 优先用 `asyncio.TaskGroup` 表达结构化并发：一个子任务失败会取消尚未完成的同组任务，并在退出时汇总异常。为请求或一组操作设置范围明确的 `asyncio.timeout()`；超时和上游取消会以 `CancelledError` 进入 coroutine。清理完成后通常要继续**取消传播**，不要吞掉 `CancelledError`，否则 TaskGroup/timeout 的控制流可能失真。

## 常见追问

- `async` 是否等于多线程？不是，默认仍在一个线程里协作调度。
- `await` 的作用是什么？暂停当前 coroutine，把控制权交回 event loop。
- `create_task` 和直接 `await` 区别？`create_task` 让 coroutine 并发推进，直接 `await` 是等待它完成后再继续。
- async 函数里能不能调用同步库？能调用，但如果它阻塞，就会阻塞整个 event loop。

## 代码例子

```python
import asyncio
import time

async def bad() -> None:
    time.sleep(1)  # blocks the event loop

async def good() -> None:
    await asyncio.sleep(1)

async def main() -> None:
    await asyncio.gather(good(), good())

asyncio.run(main())
```

```python
import asyncio
from pathlib import Path

def read_big_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

async def load_config(path: str) -> str:
    return await asyncio.to_thread(read_big_file, path)
```

```python
import asyncio

async def fetch_one(name: str) -> str:
    try:
        await asyncio.sleep(0.1)
        return name
    finally:
        print(f"cleanup {name}")

async def fetch_all() -> list[str]:
    async with asyncio.timeout(1):
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(fetch_one(name)) for name in ("rag", "tools")]
    return [task.result() for task in tasks]

print(asyncio.run(fetch_all()))
```

## 易错点

- 写了 `async def`，内部却全是同步阻塞调用，吞吐不会提升。
- 创建 task 后不 await、不收集异常，导致后台失败被忽略。
- 对共享状态并发读写，以为单线程就没有 race condition；await 点之间仍可能交错。
- 在请求生命周期里启动无限后台 task，没有取消、超时和关闭逻辑。

## 实战判断

Agent 后端常见场景是并发调用工具、模型、检索服务和外部 API。可以用 `asyncio.gather` 并发 I/O，但要配合 timeout、semaphore 限流、取消传播和错误聚合。回答时先判断任务类型：I/O-bound 用 async，阻塞 I/O 用 thread 兜底，CPU-bound 用 process 或外部任务队列。

## 可执行证据

把 `fetch_one` 的一个调用改成 `raise RuntimeError("upstream failed")`，运行 `fetch_all()`；确认同一
`TaskGroup` 的慢任务打印 cleanup 并被取消。再把 `asyncio.timeout(1)` 改成 `asyncio.timeout(0.01)`，
确认超时发生。口头解释异常组、清理和取消传播各自负责什么。

## 自测题

1. `asyncio` 为什么能提升 I/O 并发？
   答：等待 I/O 时 coroutine 主动让出控制权，event loop 调度其他任务继续执行。
2. async 函数里调用 `time.sleep()` 会怎样？
   答：阻塞 event loop，其他 coroutine 无法推进。
3. CPU 密集任务适合直接放进 event loop 吗？
   答：不适合，应使用 process、外部 worker 或释放 GIL 的实现。

## 参考链接

- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)（访问日期：2026-07-19；TaskGroup/timeout 需要 Python 3.11+）
