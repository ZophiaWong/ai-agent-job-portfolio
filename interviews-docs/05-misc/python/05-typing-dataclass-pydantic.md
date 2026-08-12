# typing、dataclass、Pydantic

## 一句话答案

`typing` 用来表达静态类型意图，`dataclass` 用来减少普通数据对象样板代码，Pydantic 用来做运行时数据校验和解析；后端面试里要能区分“给人和工具看的类型”和“真正执行的校验”。

## 核心机制

Python 类型注解默认不会在运行时强制校验，它主要服务 IDE、mypy/pyright、文档和团队协作。`list[str]`、`dict[str, int]`、`Literal`、`Protocol`、`TypedDict` 等可以把接口契约表达得更清楚，但运行时仍可能传入错误类型。

`dataclass` 自动生成 `__init__`、`__repr__`、`__eq__` 等方法，适合内部数据结构和领域对象。需要不可变语义时可以用 `frozen=True`，可变默认值要用 `field(default_factory=...)`。`frozen=True` 只是浅层冻结：它禁止重绑定字段，不会递归冻结字段指向的 `list`、`dict` 等对象；值对象应优先选择 `tuple`、`frozenset` 或真正不可变的内部类型。

Pydantic 适合外部输入边界，比如 HTTP request、配置、LLM tool schema、消息队列 payload。Pydantic v2 的 `BaseModel` 会在运行时解析和校验字段，失败时给出结构化错误。它比 dataclass 更重，但更适合不可信输入。

## 常见追问

- Type hint 会提升运行速度吗？通常不会，主要提升可维护性和静态检查能力。
- dataclass 和 Pydantic 怎么选？内部可信数据用 dataclass，外部不可信输入用 Pydantic。
- `Optional[str]` 和 `str | None`？Python 3.10+ 推荐 `str | None`，表达值可以为 None。
- Pydantic 会不会修改输入类型？会做解析，例如把 `"1"` 解析成 int，是否接受取决于字段和配置。

## 代码例子

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ToolSpec:
    name: str
    timeout_s: float = 10.0
    tags: tuple[str, ...] = ()

@dataclass(frozen=True)
class UnsafeToolSpec:
    tags: list[str] = field(default_factory=list)

unsafe = UnsafeToolSpec()
unsafe.tags.append("retrieval")
assert unsafe.tags == ["retrieval"]  # frozen 阻止重绑定，不会冻结内部 list
```

运行前提：下面示例需要安装 Pydantic。

```python
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)

request = SearchRequest.model_validate({"query": "rag", "top_k": "3"})
print(request.top_k)  # 3
```

## 易错点

- 以为类型注解等于运行时校验，导致接口边界没有真实保护。
- dataclass 字段使用可变默认值，多个实例共享同一对象。
- Pydantic 解析过度宽松时，没有意识到输入被自动转换。
- 把所有对象都做成 Pydantic model，导致内部代码耦合框架和校验成本。

## 实战判断

AI 后端项目可以按边界分层：API request、tool input、配置文件使用 Pydantic；业务内部的数据快照或值对象用 dataclass；公共函数和服务接口用 typing 表达契约。面试里这样回答能体现你理解类型、校验和工程成本的边界。

## 可执行证据

按[统一练习协议](../../practice-protocol.md)把这段 dataclass 示例保存为 `freeze_demo.py` 并运行，
在 `freeze-evidence.txt` 记录命令、`ToolSpec` 的失败重绑定尝试、`UnsafeToolSpec` 的 append 结果和原因。
随后运行 Pydantic 示例，分别传入 `{"top_k": "3"}` 与 `{"top_k": 0}`，记录转换成功和校验失败的结果。

## 自测题

1. Python 类型注解默认会在运行时拦截错误类型吗？
   答：不会，需要静态检查工具或运行时校验库。
2. dataclass 的可变默认值怎么写？
   答：用 `field(default_factory=list)` 这类工厂函数。
3. Pydantic 最适合放在哪一层？
   答：外部输入边界，例如 API、配置、消息、LLM tool schema。

## 参考链接

- [typing](https://docs.python.org/3/library/typing.html)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)（访问日期：2026-07-19）
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)（访问日期：2026-07-19；当前稳定文档为 v2）
