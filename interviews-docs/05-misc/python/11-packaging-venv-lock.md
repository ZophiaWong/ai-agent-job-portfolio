# packaging、虚拟环境和依赖锁定

## 一句话答案

虚拟环境解决项目隔离，packaging 解决项目元数据和构建，依赖锁定解决可复现安装；面试里要能说明“我本地能跑”到“别人和线上也能跑”的工程链路。

## 核心机制

Python 虚拟环境用独立解释器路径和 site-packages 隔离依赖，常见命令是 `python -m venv .venv`。激活后安装的包进入当前环境，不污染系统 Python。线上和 CI 不应依赖手工激活，而应显式使用环境中的 Python 或工具链。

现代 packaging 通常围绕 `pyproject.toml`，声明项目元数据、构建后端、依赖和工具配置。应用项目更关注锁定依赖，库项目更关注版本范围和兼容性。锁文件的意义是记录解析后的精确版本，减少“今天安装”和“明天安装”不一致。

`pip freeze` 输出的是**当前环境快照**，不是由 solver 从声明的输入计算出的依赖锁；它会把环境里已有但未必属于项目的包也带进来，默认还会省略部分 bootstrap 工具。可把快照用于诊断或复现一个已知环境，但不要把它误称为计算得出的依赖锁。若采用 `pip lock`，注意它在当前 pip 文档中仍标为 experimental，且生成文件只保证当前 Python 版本与平台；团队应把实际采用的解析/锁定工具、Python 版本与 CI 安装命令一起提交和验证。（访问日期：2026-07-19）

常见工具包括 `pip` + `requirements.txt`、`pip-tools`、Poetry、uv。无论工具是什么，原则都是区分直接依赖和传递依赖，锁定线上环境，定期升级和跑测试。

## 常见追问

- `requirements.txt` 和 lock file 区别？前者常是安装输入，lock file 应记录完整解析结果和精确版本。
- 为什么不建议用系统 Python？不同项目依赖会互相污染，权限和复现也差。
- 应用和库的依赖策略有什么不同？应用倾向锁死版本，库倾向声明兼容范围。
- 依赖冲突怎么排查？看直接依赖约束、传递依赖树、Python 版本要求，再逐步升级或收窄版本。

## 代码例子

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install fastapi uvicorn
python -m pip freeze --all  # 审计当前环境快照，不是求解生成的 lock
```

```toml
[project]
name = "agent-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi",
  "pydantic",
]
```

## 易错点

- 把系统 Python、全局 pip 和项目依赖混在一起。
- 只 pin 直接依赖，不锁传递依赖，CI 或部署时解析出不同版本。
- 不记录 Python 版本，结果依赖支持范围不一致。
- 盲目升级依赖，不跑测试也不看 breaking changes。

## 实战判断

面试中可以从复现链路回答：本地用 venv 隔离，项目用 `pyproject.toml` 声明元数据，应用用锁文件固定完整依赖图，CI 从锁文件安装并运行测试，部署镜像中固定 Python 版本。这样能体现你理解依赖不是安装命令，而是交付可靠性的一部分。

## 可执行证据

在干净 venv 中执行 `python -m pip freeze --all > environment-snapshot.txt`，再安装一个临时包并重跑，
用 `diff` 说明它只是“已安装状态”变化。然后针对本项目实际选择的锁定工具，从 `pyproject.toml`/直接依赖
重新解析完整依赖图，在同一 Python 与平台上安装并运行测试；记录解析命令、锁文件、Python 版本和测试结果。

## 自测题

1. 虚拟环境解决什么问题？
   答：隔离不同项目的解释器路径和第三方依赖。
2. 为什么应用项目需要锁文件？
   答：保证 CI、同事机器和线上安装到一致的完整依赖版本。
3. `pyproject.toml` 的价值是什么？
   答：集中声明项目元数据、构建系统、依赖和工具配置。

## 参考链接

- [venv](https://docs.python.org/3/library/venv.html)
- [Writing `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)（访问日期：2026-07-19）
- [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)（访问日期：2026-07-19）
- [pip lock](https://pip.pypa.io/en/stable/cli/pip_lock/)（访问日期：2026-07-19；experimental）
