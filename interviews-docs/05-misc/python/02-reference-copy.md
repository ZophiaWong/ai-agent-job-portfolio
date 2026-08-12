# 引用、浅拷贝、深拷贝

## 一句话答案

Python 变量保存的是对象引用，不是对象本身；浅拷贝只复制外层容器，深拷贝递归复制内部对象。面试重点是能解释可变对象共享、函数参数传递和嵌套结构被意外修改的问题。

## 核心机制

赋值语句只是让名字绑定到对象，例如 `b = a` 后，`a` 和 `b` 指向同一个 list。修改 list 内容时两个名字都会看到变化；但如果给 `b` 重新赋值，只是改变 `b` 的绑定，不影响 `a`。

浅拷贝可以用 `copy.copy()`、切片或 `list()` 创建外层新对象，但内部元素仍然共享。深拷贝用 `copy.deepcopy()`，会递归复制对象图，并用 memo 避免循环引用导致无限递归。深拷贝不是越多越好，它可能复制大量数据、破坏共享资源语义，甚至复制不该复制的连接、锁、文件句柄。

函数参数也是引用传递的一种表现：函数接收对象引用，能修改可变对象内容，但不能通过重新绑定参数名改变调用方变量指向。

## 常见追问

- Python 是值传递还是引用传递？更准确说是对象引用按值传递，函数拿到的是引用的副本。
- `copy.copy()` 和 `copy.deepcopy()` 区别？浅拷贝只复制一层，深拷贝递归复制嵌套对象。
- 为什么默认参数 `items=[]` 有坑？默认参数在函数定义时创建一次，后续调用共享同一个 list。
- 深拷贝什么时候危险？对象里有数据库连接、锁、文件句柄、模型实例或大量缓存时，深拷贝可能语义错误或代价过高。

## 代码例子

```python
import copy

original = {"tags": ["rag", "agent"]}
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow["tags"].append("eval")

print(original["tags"])  # ["rag", "agent", "eval"]
print(deep["tags"])      # ["rag", "agent"]
```

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag("rag"))
print(add_tag("agent"))
```

## 易错点

- 把赋值当成复制，导致多个变量共享同一个可变对象。
- 对嵌套 dict/list 只做浅拷贝，然后在请求处理中污染原始配置。
- 见到问题就用 `deepcopy`，忽略性能和资源语义。
- 在 dataclass 中写 `tags: list[str] = []`，应该使用 `field(default_factory=list)`。

## 实战判断

后端项目中最常见的是配置模板、请求 payload、工具调用参数被复用。回答时可以说：跨请求共享的对象应该不可变或只读；需要修改时先复制边界内的数据；深拷贝只用于确实需要隔离嵌套结构，资源对象不做深拷贝。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)把第一个示例保存为 `copy_demo.py` 并运行；在
`copy-evidence.txt` 留下运行命令、三份对象的 `id()`、修改前后观察和你的拷贝选择理由。

## 自测题

1. `b = a` 会创建新对象吗？
   答：不会，只是让 `b` 绑定到 `a` 指向的同一个对象。
2. 浅拷贝为什么仍会污染原对象？
   答：外层容器是新的，但内部可变元素仍然共享引用。
3. 默认参数为什么不能直接写空 list？
   答：默认参数只在函数定义时初始化一次，多次调用会共享同一个对象。

## 参考链接

- [Python copy module](https://docs.python.org/3/library/copy.html)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
