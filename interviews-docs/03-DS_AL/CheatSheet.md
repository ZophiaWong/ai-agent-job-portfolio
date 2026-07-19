# DS/AL Python 面试速查

这个文件只放可快速回忆的模板、复杂度和易错点。完整讲解看同目录下 7 个章节。

## 题型到模式

| 信号 | 优先模式 |
| --- | --- |
| 查找是否出现、计数、分组 | `dict` / `set` |
| 连续子数组、连续子串、最长/最短 | 滑动窗口 |
| 已排序数组、两数和、原地去重 | 双指针 |
| 区间和、子数组和等于 K | 前缀和 + 哈希计数 |
| 括号、最近未匹配、下一个更大 | 栈 / 单调栈 |
| 层序、扩散、无权最短路 | `deque` BFS |
| Top K、动态极值 | `heapq` |
| 已排序、边界、最小可行值 | 二分 |
| 所有组合/排列/子集 | 回溯 |
| 最值、方案数、可达性、重复子问题 | 动态规划 |

## 常用复杂度

| 结构/操作 | 复杂度 |
| --- | --- |
| `x in set` / `dict[key]` | 均摊 `O(1)` |
| 排序 | `O(n log n)` |
| 双指针扫描 | `O(n)` |
| 滑动窗口 | `O(n)`，每个元素最多进出一次 |
| BFS / DFS | `O(V + E)` 或网格 `O(mn)` |
| `heapq.heappush/heappop` | `O(log n)` |
| 大小为 k 的 Top K 堆 | `O(n log k)` |
| 二分查找 | `O(log n)` |
| 回溯枚举 | 通常指数级，取决于输出规模 |

## Python 模板

### 哈希计数

```python
from collections import defaultdict

counter = defaultdict(int)
for x in nums:
    counter[x] += 1
```

### 前缀和计数

```python
from collections import defaultdict

counter = defaultdict(int)
counter[0] = 1
prefix = 0
answer = 0

for x in nums:
    prefix += x
    answer += counter[prefix - target]
    counter[prefix] += 1
```

### 滑动窗口

前提：固定窗口要求 `1 <= k <= len(nums)`；下面的可变窗口只适用于 `nums` 为非负数、窗口和具有单调性的题。含负数的区间和题改用前缀和等方法。

```python
left = 0
state = 0

for right, x in enumerate(nums):
    state += x
    while not valid(state):
        state -= nums[left]
        left += 1
    update_answer(left, right, state)
```

### 二分左边界

前提：`nums` 必须已按升序排序；本模板使用半开区间 `[left, right)`，返回第一个不小于 `target` 的下标（可能等于 `len(nums)`）。

```python
left, right = 0, len(nums)
while left < right:
    mid = (left + right) // 2
    if nums[mid] < target:
        left = mid + 1
    else:
        right = mid
```

### BFS

```python
from collections import deque

queue = deque([start])
seen = {start}

while queue:
    node = queue.popleft()
    for nxt in graph[node]:
        if nxt not in seen:
            seen.add(nxt)
            queue.append(nxt)
```

### 回溯

```python
result = []
path = []

def dfs(start):
    result.append(path[:])
    for i in range(start, len(nums)):
        path.append(nums[i])
        dfs(i + 1)
        path.pop()
```

### Top K 小根堆

```python
import heapq

heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)
```

## 易错点索引

- 前缀和计数要先放 `counter[0] = 1`。
- 滑动窗口题先确认是否存在单调性，负数数组不一定能套。
- 链表改 `next` 前先保存后继节点。
- 树的递归返回值和全局答案不要混在一起。
- 0/1 背包一维优化通常倒序遍历容量。
- 回溯保存结果时用 `path[:]`。
- `deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`。
- Python `heapq` 是小根堆。
- 二分的返回值必须和区间定义一致。
- 需要保留原数组时，不要把排序、反转或网格标记直接写回调用方输入；先复制或明确说明会原地修改。
- Python 递归深度有限；退化链状树或大网格优先改用显式栈/队列。
