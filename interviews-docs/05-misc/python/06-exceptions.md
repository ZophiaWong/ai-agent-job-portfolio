# 异常处理

## 一句话答案

异常处理的目标不是“把错误吞掉”，而是把错误分类、补充上下文、在合适边界恢复或失败；后端面试里要能讲清楚捕获范围、异常链、资源释放和对外错误语义。

## 核心机制

Python 异常继承自 `BaseException`，业务代码通常捕获 `Exception`，不要捕获 `BaseException`，因为 `KeyboardInterrupt`、`SystemExit` 也在其中。`try/except/else/finally` 中，`except` 处理异常，`else` 只在无异常时执行，`finally` 无论成功失败都执行，适合释放资源。

异常链用 `raise NewError(...) from exc` 保留原始原因，能让日志和排查更完整。自定义异常适合表达业务错误，例如 `ToolTimeoutError`、`InvalidEmbeddingInput`，但不要为每个小分支都创建异常类。

在 API 层，异常要转成稳定的 HTTP 状态码和错误响应；在内部服务层，异常要保留足够上下文；在任务或 Agent 调用层，需要区分可重试错误、不可重试错误和用户输入错误。

## 常见追问

- 为什么不建议裸 `except:`？它会捕获过宽，包括中断信号，容易隐藏问题。
- `raise` 和 `raise exc` 有什么区别？在 `except` 中直接 `raise` 保留原 traceback；`raise exc` 可能改变 traceback。
- `finally` 里 return 有什么坑？会覆盖 try/except 中的 return 或异常，通常应避免。
- 什么时候自定义异常？当调用方需要按错误类型做分支处理，而不是只看字符串时。

## 代码例子

```python
class ToolCallError(Exception):
    pass

def call_tool(payload: dict) -> str:
    try:
        return payload["name"].upper()
    except KeyError as exc:
        raise ToolCallError("tool payload missing name") from exc
```

```python
def parse_limit(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        return 10
    else:
        return min(value, 100)
    finally:
        print("parse_limit finished")
```

## 易错点

- 捕获异常后只打印日志不重新抛出，调用方误以为成功。
- 把所有异常都转成同一个错误码，导致用户输入错误和系统故障无法区分。
- 在底层库函数里直接返回 HTTP response，破坏层次边界。
- 过度使用异常控制普通流程，导致可读性和性能都变差。

## 实战判断

可以按边界回答：底层补充上下文并保留异常链，服务层决定是否重试或降级，API 层转成用户可理解的错误响应，后台任务层记录可观测日志并决定是否进入死信或告警。这样比单纯说 `try/except` 更像工程经验。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)把 `call_tool({})` 放进最小脚本并运行，让 traceback 输出到
`exception-evidence.txt`；标注新异常、原始 `KeyError` 和 `from` 链各自提供了什么排查信息。

## 自测题

1. 为什么业务代码通常捕获 `Exception` 而不是 `BaseException`？
   答：`BaseException` 包含系统退出和中断信号，捕获它会干扰进程控制。
2. `raise NewError from exc` 的价值是什么？
   答：保留原始异常链，同时提供更高层语义。
3. `finally` 适合做什么？
   答：释放资源、关闭连接、清理临时状态，不适合写会覆盖异常的 return。

## 参考链接

- [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
