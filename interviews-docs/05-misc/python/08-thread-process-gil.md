# thread、process 和 GIL 的边界

## 一句话答案

Python thread 适合 I/O-bound 并发，process 适合 CPU-bound 并行；在默认的 GIL 启用 CPython 构建中，GIL 让同一进程内多个线程不能同时执行 Python bytecode，所以 CPU 密集任务通常不能靠多线程线性加速。

## 核心机制

GIL 是 CPython 的 Global Interpreter Lock，用来保护解释器内部状态。它不代表 Python 没有并发，也不代表所有操作都慢；它主要限制同一进程内多个线程同时执行 Python bytecode。线程在等待 I/O 时会释放 GIL，因此网络请求、文件 I/O、数据库调用这类 I/O-bound 任务仍可以用 thread 提升吞吐。

版本边界（访问日期：2026-07-19）：可选的 free-threaded CPython 3.13+ 构建仍属实验性，可在没有 GIL 时并行运行线程；它不是默认解释器语义，也不消除业务层的锁、队列和不变量设计。free-threaded 构建还可能因不支持它的扩展在运行时重新启用 GIL，因此部署前要确认实际构建和依赖兼容性。

CPU-bound 任务如果主要执行 Python 代码，多线程会互相争抢 GIL，通常应使用 `multiprocessing`、`ProcessPoolExecutor`、外部任务队列，或 NumPy 这类能释放 GIL 的 native extension。

Process 有独立内存空间，绕开 GIL，但进程启动、序列化和跨进程通信成本更高。Thread 共享内存，创建成本低，但要处理共享状态、锁和 race condition。

## 常见追问

- GIL 是否影响所有 Python 实现？这是 CPython 的特性，不应泛化到所有实现。
- 多线程是否完全没用？不是，I/O-bound 很有用，CPU-bound Python bytecode 才受限明显。
- Process 的代价是什么？内存隔离、启动成本、pickle 序列化和 IPC 成本。
- async、thread、process 怎么选？async 管高并发非阻塞 I/O，thread 包装阻塞 I/O，process 做 CPU 并行。

## 代码例子

```python
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

def fetch(url: str) -> int:
    with urlopen(url, timeout=5) as response:
        return response.status

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch, ["https://www.python.org"] * 4)))
```

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_work(n: int) -> int:
    return sum(i * i for i in range(n))

with ProcessPoolExecutor() as pool:
    print(list(pool.map(cpu_work, [1_000_000, 1_000_000])))
```

## 易错点

- 认为 GIL 让 Python 不能并发，忽略 I/O-bound 多线程和 asyncio。
- 在多线程中修改共享 dict/list，不做锁或队列隔离。
- 把大对象传给 process pool，序列化成本超过并行收益。
- 在 Web 请求线程里直接跑长 CPU 任务，拖慢整个服务。

## 实战判断

面试中先分类任务：外部 API、数据库、文件读取是 I/O-bound；embedding 后处理、纯 Python 排序/解析大数据可能是 CPU-bound。AI 后端里模型调用通常是远程 I/O，适合 async 或 thread；本地 heavy compute 更适合 process、GPU/native 库或异步任务系统。

## 可执行证据

用同一份纯 Python CPU 计算分别通过顺序循环、`ThreadPoolExecutor` 和 `ProcessPoolExecutor` 运行，记录
机器、Python 版本、输入规模和耗时；不要把一次基准当普遍结论。随后运行 `python -VV`，若使用
free-threaded 构建再检查 `sys._is_gil_enabled()`，并在报告中写明“默认 GIL 启用”还是“可选 free-threaded”运行边界。

## 自测题

1. GIL 限制的核心是什么？
   答：同一 CPython 进程内多个线程不能同时执行 Python bytecode。
2. 为什么 I/O-bound 仍可用多线程？
   答：线程等待 I/O 时会释放 GIL，其他线程可以继续运行。
3. process pool 的主要成本是什么？
   答：进程启动、内存占用、参数和结果序列化、跨进程通信。

## 参考链接

- [threading](https://docs.python.org/3/library/threading.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Python 3.13 free-threading](https://docs.python.org/3.13/howto/free-threading-python.html)（访问日期：2026-07-19）
