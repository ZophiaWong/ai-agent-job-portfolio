# iterator、generator

## 一句话答案

Iterator 是实现 `__iter__()` 和 `__next__()` 的对象，generator 是一种更方便创建 iterator 的方式；它们的价值在于懒加载、流式处理和控制内存，而不是一次性把所有数据放进 list。

## 核心机制

Iterable 表示“可被迭代”，调用 `iter(obj)` 后得到 iterator。Iterator 每次 `next()` 返回一个值，结束时抛 `StopIteration`。`for` 循环内部就是不断调用 `iter()` 和 `next()`，直到捕获 `StopIteration`。

Generator function 使用 `yield`，调用函数时不会立即执行函数体，而是返回 generator object。每次 `next()` 执行到下一个 `yield` 暂停，并保留局部变量状态。Generator expression 类似 list comprehension，但不会立即构造完整列表。

在 AI 后端里，iterator/generator 常用于读取大文件、分页拉取数据、流式返回 tokens、批处理 embeddings。关键 tradeoff 是：generator 节省内存，但通常只能顺序消费一次，调试和错误定位也要注意延迟执行。

## 常见追问

- Iterable 和 Iterator 有什么区别？Iterable 能产生 iterator；Iterator 自己也是 iterable，并能逐个吐出值。
- Generator 为什么省内存？它按需计算，每次只保留当前执行状态，不构造完整结果集。
- Generator 能重复遍历吗？同一个 generator 通常只能消费一次；要重复遍历，需要重新创建 generator。
- `yield from` 的作用？把子 iterator 的值转发出来，简化嵌套生成器。

## 代码例子

```python
def batched(items: list[str], size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]

for batch in batched(["a", "b", "c", "d", "e"], 2):
    print(batch)
```

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print(list(Countdown(3)))  # [3, 2, 1]
```

## 易错点

- 把 generator 转成 `list()` 后，内存优势消失。
- 同一个 generator 被日志、调试或校验提前消费，后续业务拿不到数据。
- 在 generator 中抛异常会延迟到消费时出现，不一定在创建 generator 时暴露。
- 误以为 generator 自带并发能力；它只是惰性迭代，不等于 async。

## 实战判断

如果数据量可控且需要随机访问，用 list 更简单。如果数据大、来自网络/文件/分页 API，或需要边计算边输出，用 generator 更合理。面试里可以主动补一句：流式 API 如果涉及异步 I/O，应考虑 async generator，而不是普通 generator。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)把 `batched` 示例保存为 `generator_demo.py`，先消费一次、
再尝试复用同一个 generator；把命令、两次消费现象和适用场景记入 `generator-evidence.txt`。

## 自测题

1. `iterable` 和 `iterator` 的核心区别是什么？
   答：Iterable 能返回 iterator；Iterator 实现 `__next__()`，保存迭代状态。
2. Generator function 调用时会执行函数体吗？
   答：不会，调用只返回 generator，消费时才执行到 `yield`。
3. 为什么同一个 generator 通常不能遍历两次？
   答：它保存单向消费状态，结束后不会自动重置。

## 参考链接

- [Python Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Python Generators](https://docs.python.org/3/tutorial/classes.html#generators)
