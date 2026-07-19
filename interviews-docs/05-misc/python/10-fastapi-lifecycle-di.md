# FastAPI 请求生命周期和依赖注入

## 一句话答案

FastAPI 基于 ASGI：请求进入后经过 middleware、路由匹配、依赖解析、参数校验、endpoint 执行、响应序列化；依赖注入用于声明式构造共享能力，如鉴权、数据库会话、配置和客户端。

## 核心机制

FastAPI 运行在 ASGI server 上，例如 Uvicorn。一次请求大致流程是：ASGI server 接收连接，middleware 处理横切逻辑，FastAPI 匹配 path operation，解析 path/query/header/body/cookie 参数，Pydantic 校验输入，执行依赖函数，再调用 endpoint，最后把返回值序列化成 response。

依赖注入通过 `Depends` 声明。依赖可以依赖其他依赖，可以是 sync 或 async，也可以用 `yield` 在请求结束后做清理。常见用法包括获取当前用户、创建数据库 session、读取配置、注入 service 或 client。

生命周期管理推荐使用 lifespan，在应用启动时创建连接池、模型客户端、缓存，在关闭时释放资源。不要在每个请求里重复创建昂贵客户端，也不要把 request-scoped 状态放到全局变量里。

## 常见追问

- sync endpoint 和 async endpoint 区别？async endpoint 在 event loop 中执行，sync endpoint 通常被放入线程池，避免阻塞 loop。
- 依赖函数什么时候执行？请求处理时按依赖图解析，默认同一请求内可缓存依赖结果。
- `yield` dependency 适合什么？请求级资源的创建和释放，例如 DB session。
- middleware 和 dependency 怎么选？middleware 处理全局横切逻辑，dependency 处理路由相关的显式能力。

## 代码例子

运行前提：下面示例需要安装 FastAPI。

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_token() -> str:
    return "dev-token"

@app.get("/health")
def health(token: Annotated[str, Depends(get_token)]) -> dict:
    return {"ok": True, "token": token}
```

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model_client = object()
    yield
    app.state.model_client = None

app = FastAPI(lifespan=lifespan)
```

## 易错点

- async endpoint 内调用同步阻塞 HTTP/DB 客户端，阻塞 event loop。
- 在全局变量里存 request-scoped 用户、trace 或 session，导致并发污染。
- 每次请求创建昂贵客户端，没有连接复用。
- 依赖层级过深，业务逻辑隐藏在 dependency 中，测试和排查困难。

## 实战判断

回答项目深挖时可以说：请求级对象用 dependency，应用级资源用 lifespan，全局横切逻辑用 middleware；外部 I/O 选择 async client 或线程池隔离；测试时 override dependency 来替换数据库、鉴权或 LLM client。

## 可执行证据

安装 FastAPI、pytest 和 HTTPX 后，把下列两段放入 `main.py` 与 `test_main.py`，执行
`pytest -q test_main.py`。测试不启动真实 socket；`TestClient` 直接调用 ASGI app，
`app.dependency_overrides` 只在测试内替换外部依赖，结束后必须清空。

```python
# main.py
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_user() -> str:
    raise RuntimeError("real auth must not run in this test")

@app.get("/me")
def read_me(user: Annotated[str, Depends(get_user)]) -> dict[str, str]:
    return {"user": user}
```

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app, get_user

def test_me_uses_override() -> None:
    app.dependency_overrides[get_user] = lambda: "test-user"
    try:
        response = TestClient(app).get("/me")
        assert response.status_code == 200
        assert response.json() == {"user": "test-user"}
    finally:
        app.dependency_overrides = {}
```

迁移题：把依赖改成 `yield` 的请求级资源，用 `with TestClient(app)` 覆盖 lifespan，并断言清理在 client
上下文退出后发生。

## 自测题

1. FastAPI 输入校验主要依赖什么？
   答：类型注解和 Pydantic model。
2. `yield` dependency 的清理逻辑何时执行？
   答：请求处理完成后执行，适合释放请求级资源。
3. middleware 和 dependency 的边界是什么？
   答：middleware 面向全局请求链路，dependency 面向路由需要的显式依赖。

## 参考链接

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Lifespan](https://fastapi.tiangolo.com/advanced/events/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)（访问日期：2026-07-19）
- [FastAPI dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)（访问日期：2026-07-19）
- [ASGI Specification](https://asgi.readthedocs.io/en/latest/)
