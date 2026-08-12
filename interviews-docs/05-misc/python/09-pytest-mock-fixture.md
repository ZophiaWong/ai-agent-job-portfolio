# pytest、mock、fixture

## 一句话答案

`pytest` 负责组织测试和断言，fixture 负责构造可复用测试上下文，mock 负责隔离外部依赖；面试重点是说明你测的是业务行为，不是把实现细节 mock 到失真。

## 核心机制

pytest 通过文件名和函数名发现测试，直接使用 `assert` 做断言，失败时会给出表达式级别的差异。fixture 用 `@pytest.fixture` 声明，可以被测试函数按参数名注入，支持作用域、依赖其他 fixture、yield 清理资源。

mock 用来替换网络、数据库、时间、随机数、LLM API 等不可控依赖。常见工具是 `unittest.mock.Mock`、`patch`，或 pytest 生态中的 `monkeypatch`。使用 mock 时要关注 patch 的位置：应该 patch 被测模块实际查找对象的位置，而不是对象定义的位置。

好的测试分层通常包括：纯函数单元测试、服务层 mock 外部依赖、API integration test 用测试客户端覆盖路由和依赖注入。

## 常见追问

- fixture 相比 setup 函数有什么优势？可组合、按需注入、作用域清楚、清理逻辑自然。
- mock 的风险是什么？过度 mock 实现细节，测试通过但真实集成失败。
- patch 应该 patch 哪里？patch 被测代码引用该对象的命名空间。
- 单元测试和 integration test 怎么区分？单元测试隔离依赖，integration test 覆盖多个组件真实协作。

## 代码例子

运行前提：下面示例需要安装 pytest。

```python
import pytest

@pytest.fixture
def sample_payload() -> dict:
    return {"query": "rag", "top_k": 3}

def test_payload_has_query(sample_payload: dict) -> None:
    assert sample_payload["query"]
```

```python
from unittest.mock import Mock

def answer(client, query: str) -> str:
    return client.search(query)["text"]

def test_answer_uses_client() -> None:
    client = Mock()
    client.search.return_value = {"text": "ok"}

    assert answer(client, "rag") == "ok"
    client.search.assert_called_once_with("rag")
```

## 易错点

- 只测 happy path，不测空输入、超时、异常、重试失败。
- mock 太深，连自己写的业务分支都 mock 掉，测试失去价值。
- patch 位置错误，测试没有真正替换依赖。
- fixture 作用域过大，测试之间共享可变状态互相污染。

## 实战判断

AI 后端测试要特别隔离 LLM、向量库、第三方 API 和时间。单元测试用 fake 或 mock 固定返回，integration test 覆盖 FastAPI 路由、依赖注入和错误响应，少量端到端测试再打真实服务。回答时强调可重复、快、失败原因清楚。

## 可执行证据

在空目录创建 `test_answer.py`，把下面代码完整写入后执行 `pytest -q test_answer.py`：

```python
import pytest

@pytest.fixture
def client():
    return {"answer": "retrieval result"}

def answer(client: dict, query: str) -> str:
    if not query:
        raise ValueError("query is required")
    return client["answer"]

def test_answer_returns_value(client: dict) -> None:
    assert answer(client, "rag") == "retrieval result"

def test_answer_rejects_empty_query(client: dict) -> None:
    with pytest.raises(ValueError, match="required"):
        answer(client, "")
```

把 fixture 改为返回空字典，观察失败信息；不要 mock `answer` 自己。随后把真实 HTTP/LLM client
替换为 fake 或在**被测模块查找对象的命名空间** patch，并补一个不使用 mock 的集成测试。

## 自测题

1. fixture 的核心作用是什么？
   答：构造和注入测试上下文，并可集中管理清理逻辑。
2. mock 外部 API 的主要目的是什么？
   答：让测试稳定、快速、可重复，并覆盖业务对外部结果的处理。
3. 为什么不能只依赖 mock 测试？
   答：mock 可能偏离真实协议，需要 integration test 兜住组件协作。

## 参考链接

- [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)（访问日期：2026-07-19）
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
