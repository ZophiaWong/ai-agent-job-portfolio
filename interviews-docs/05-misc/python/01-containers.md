# list、dict、set、tuple

## 一句话答案

`list` 适合有序序列和按索引访问，`dict` 适合 key-value 映射，`set` 适合去重和成员判断，`tuple` 适合不可变记录和可哈希组合键；面试里不要只背定义，要能说出复杂度、可变性和典型坑。

## 核心机制

`list` 是动态数组，按索引读取是 O(1)，尾部 `append` 摊还 O(1)，中间插入或删除通常 O(n)。`dict` 和 `set` 基于 hash table，平均 O(1) 查询、插入、删除，但要求 key 或元素可哈希，且 hash/eq 语义稳定。现代 Python 的 `dict` 保持插入顺序，所以可以用于保序映射，但不要把它误解成排序结构。

`tuple` 本身不可变，只有当内部元素也可哈希时，整个 tuple 才能作为 dict key 或 set 元素。`list` 与 `dict` 是可变对象，函数默认参数、对象属性共享、浅拷贝时都容易引入隐式状态污染。

## 常见追问

- 为什么 `x in list` 和 `x in set` 性能不同？`list` 线性扫描，`set` 走 hash 查找，平均 O(1)。
- `dict` 是否线程安全？字节码“看起来原子”不是线程安全保证。业务的不变量往往跨多步读改写；跨线程共享可变状态时，用 `threading.Lock`、队列或消息传递把同步边界写清楚。即使是 free-threaded CPython 的内建容器内部锁，也是当前实现描述，不是业务同步契约。
- `tuple` 一定可哈希吗？不是，`(1, 2)` 可哈希，`([1], 2)` 不可哈希。
- 什么时候不用 `set`？需要保留重复次数、稳定排序、或元素不可哈希时，不该直接用 set。

## 代码例子

```python
from collections import Counter

items = ["rag", "agent", "rag"]

unique = set(items)
counts = Counter(items)
index = {name: i for i, name in enumerate(items)}

print(unique)          # {"rag", "agent"}
print(counts["rag"])   # 2
print(index["agent"])  # 1
```

```python
cache_key = ("tenant-a", "embedding-v1")
cache = {cache_key: [0.1, 0.2]}

bad_key = (["tenant-a"], "embedding-v1")
# cache[bad_key] = []  # TypeError: unhashable type: 'list'
```

## 易错点

- 用 `list` 做频繁成员判断，数据量上来后会退化明显。
- 以为 `tuple` 内部对象也不可变，实际 tuple 只保证自身槽位不可变。
- 依赖 `set` 的遍历顺序输出业务结果，容易产生不可预测表现。
- 用可变对象作为 dataclass 或函数默认值，需要用 `default_factory` 或 `None` 哨兵。

## 实战判断

面试回答时可以按访问模式选容器：需要索引用 `list`，需要唯一性和成员判断用 `set`，需要按 key 查配置、连接、缓存用 `dict`，需要不可变组合标识用 `tuple`。如果数据会跨请求复用，重点说明可变性边界和拷贝策略。

## 可执行证据

写一个两线程都执行 10,000 次“读计数、加一、写回”的小脚本：先不加锁，再用
`threading.Lock` 包住整个读改写；运行多次并记录结果。练习结论不是依赖某次恰好得到
20,000，而是解释为何只有锁把这段复合操作的业务不变量写成了同步契约。

## 自测题

1. 为什么 `set` 查询通常比 `list` 快？
   答：`set` 基于 hash table，平均 O(1)；`list` 需要逐个比较，O(n)。
2. `tuple` 能不能作为 `dict` key？
   答：可以，但前提是 tuple 内部所有元素都可哈希。
3. `dict` 的插入顺序能不能用于业务排序？
   答：可以保留插入顺序，但如果业务要求排序，应显式 `sorted` 或使用更清楚的数据结构。

## 参考链接

- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python free-threading 的线程安全说明](https://docs.python.org/3.13/howto/free-threading-python.html)（访问日期：2026-07-19）
