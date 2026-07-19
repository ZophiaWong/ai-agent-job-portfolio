# decorator、context manager

## 一句话答案

Decorator 用函数包装函数，适合日志、鉴权、重试、缓存等横切逻辑；context manager 用 `with` 管理资源生命周期，保证进入和退出逻辑成对执行。面试重点是能写出最小实现，并说明不要隐藏业务副作用。

## 核心机制

Decorator 本质是高阶函数：接收一个函数，返回一个新函数。`@decorator` 只是语法糖，等价于 `func = decorator(func)`。为了保留原函数名、docstring 和调试信息，应该使用 `functools.wraps`。

Context manager 有两种写法：实现 `__enter__` / `__exit__`，或使用 `contextlib.contextmanager`。`with` 块进入时调用 `__enter__`，退出时调用 `__exit__`；即使块内抛异常，也会执行退出逻辑。`__exit__` 返回 true 会吞掉异常，通常不要这么做，除非明确要把异常转成业务结果。

在 FastAPI、pytest、数据库连接、文件操作中，这两个机制都很常见：decorator 处理横切行为，context manager 处理资源边界。

## 常见追问

- Decorator 会不会改变函数签名？包装不当会影响 introspection、依赖注入和测试，至少要用 `wraps`。
- 多个 decorator 执行顺序？离函数最近的先包装，调用时最外层先执行。
- `__exit__` 的三个参数是什么？异常类型、异常值、traceback。
- context manager 和 `try/finally` 的关系？`with` 是结构化的 `try/finally` 资源管理写法。

## 代码例子

```python
from functools import wraps
from time import perf_counter

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__} took {perf_counter() - start:.3f}s")
    return wrapper

@timed
def run_tool(name: str) -> str:
    return name.upper()
```

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name: str):
    print(f"open {name}")
    try:
        yield name
    finally:
        print(f"close {name}")

with managed_resource("vector-client") as resource:
    print(resource)
```

## 易错点

- decorator 不用 `wraps`，导致 FastAPI 依赖、pytest 名称、日志和文档生成拿到错误元信息。
- 在 decorator 中捕获所有异常但不重新抛出，隐藏真实失败。
- context manager 的退出逻辑里又抛新异常，覆盖原始异常。
- 把业务逻辑塞进 decorator，导致控制流不透明。

## 实战判断

适合 decorator 的是稳定、通用、可组合的横切逻辑，例如 retry、metrics、auth。适合 context manager 的是必须成对释放的资源，例如连接、临时文件、锁、trace span。回答时要补一句：框架层可以用 decorator，业务核心路径更要保持显式，避免调试困难。

## 自测题

1. `@d` 的本质是什么？
   答：`func = d(func)`，把原函数替换为 decorator 返回的新对象。
2. 为什么要用 `functools.wraps`？
   答：保留原函数元信息，避免调试、文档、依赖注入和测试识别出错。
3. `with` 块内抛异常时会执行清理吗？
   答：会，`__exit__` 或 `finally` 逻辑仍会执行。

## 参考链接

- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- [contextlib](https://docs.python.org/3/library/contextlib.html)
