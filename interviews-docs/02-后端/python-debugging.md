# Python 调试：用证据缩小问题

主要能力：`C01.02`。本题按[统一练习协议](../practice-protocol.md)练习。

## 冷启动调试题

把下面代码保存为 `python-debugging.py`，不看参考区，先运行它：

```python
def average_latency(lines: list[str]) -> float:
    values = [int(line.removeprefix("latency_ms=")) for line in lines]
    return sum(values) / len(values)


if __name__ == "__main__":
    sample = ["request_id=a1", "latency_ms=80", "latency_ms=120"]
    print(average_latency(sample))
```

交付一份 `python-debugging-evidence.md`，按下列顺序记录：

1. 复现命令和完整 traceback；
2. 从 traceback 和输入数据中摘出两条证据，如果加日志，记下具体输出；
3. 写一个可被反证的假设；
4. 只做最小修复，运行原复现命令；
5. 添加回归测试，覆盖混合日志和“没有任何延迟行”的输入。

只有命令、输出、patch 和测试结果都对得上，才是可执行证据。

## 迁移题

上线后又出现一个问题：输入只有 `request_id=a1`。改变假设并定义新的行为契约。在“返回 0”、“返回 `None`”和“抛出有业务含义的异常”之间选一个，写下取舍和回归测试。

## 延迟复测与证据边界

48 小时后，不看答案，用同样的“复现 → 证据 → 假设 → 最小修复 → 回归测试”处理一个崭新故障，记录到 `python-debugging-retest.md`。读完参考代码不能作为掌握证据；提示后完成的修复也不算独立证据。

<!-- 练习分隔线：完成冷答后再继续 -->

## 参考调试记录

原程序会在 `int("request_id=a1")` 处抛出 `ValueError`。这条 traceback 把问题缩小到列表推导式；输入又显示函数收到了不同类型的日志行。可检验的假设是：代码没有在转换前筛选 `latency_ms=` 行。

下面是最小修复和回归测试。只用 Python 标准库，可直接运行。

```python
import unittest


def average_latency(lines: list[str]) -> float:
    prefix = "latency_ms="
    values = [int(line.removeprefix(prefix)) for line in lines if line.startswith(prefix)]
    if not values:
        raise ValueError("no latency samples")
    return sum(values) / len(values)


class AverageLatencyTest(unittest.TestCase):
    def test_ignores_unrelated_log_lines(self) -> None:
        lines = ["request_id=a1", "latency_ms=80", "latency_ms=120"]
        self.assertEqual(average_latency(lines), 100.0)

    def test_rejects_input_without_samples(self) -> None:
        with self.assertRaisesRegex(ValueError, "no latency samples"):
            average_latency(["request_id=a1"])


if __name__ == "__main__":
    unittest.main()
```

## 评分要点

| 等级 | 可观察表现 |
| --- | --- |
| 0–1 | 未复现就猜原因，或直接重写整个函数。 |
| 2 | 能定位异常行，但假设没有对应的输入证据或回归测试。 |
| 3 | 保留复现、traceback 和日志证据，用最小修复验证假设，并运行回归测试。 |
| 4 | 输入契约改变后仍能缩小故障，说明失败行为和可观测性取舍。 |

没有执行结果的“看起来对”只能记为待验证。
