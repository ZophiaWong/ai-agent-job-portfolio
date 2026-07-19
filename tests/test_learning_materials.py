import io
import re
import unittest
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = (
    REPO_ROOT
    / "AI_Agent_System_Practical_Reference"
    / "00_README_学习路线与资料使用说明.md"
)
PLACEHOLDER_INDEXES = [
    REPO_ROOT / "interviews-docs" / "01-AI" / "README.md",
    REPO_ROOT / "interviews-docs" / "02-后端" / "README.md",
]
OBSOLETE_FILES = [
    REPO_ROOT / "learning-materials" / "LangGraph.md",
    REPO_ROOT / "learning-materials" / "PostgreSQL-crash.md",
    REPO_ROOT / "learning-materials" / "RAG-basis.md",
    REPO_ROOT / "learning-materials" / "python-crash.md",
    REPO_ROOT / "best-practice" / "Harness-Engineering" / "openai-harness-engineering.md",
    REPO_ROOT / "best-practice" / "top-players" / "agents-design-from-lidangzzz.md",
    REPO_ROOT / "best-practice" / "top-players" / "claude-code-leakage.md",
    REPO_ROOT / "interviews-docs" / "05-misc" / "gap-year-explanation.md",
    REPO_ROOT / "interviews-docs" / "05-misc" / "python.md",
    REPO_ROOT / "interviews-docs" / "05-misc" / "nodejs.md",
]
PRACTICE_SEQUENCE = "冷启动 → 澄清约束 → 独立作答/编码 → 执行或检查 → 解释权衡 → 迁移题 → 延迟复测"
DSA_DIR = REPO_ROOT / "interviews-docs" / "03-DS_AL"
DSA_CHAPTERS = (
    "01_数组与双指针.md",
    "02_滑动窗口.md",
    "03_链表.md",
    "04_二叉树.md",
    "05_动态规划.md",
    "06_回溯与搜索.md",
    "07_堆栈队列二分.md",
)
PYTHON_DIR = REPO_ROOT / "interviews-docs" / "05-misc" / "python"
NODE_DIR = REPO_ROOT / "interviews-docs" / "05-misc" / "nodejs"


def python_fences(text: str) -> list[str]:
    return re.findall(r"```python\n(.*?)```", text, re.DOTALL)


class LearningMaterialsTest(unittest.TestCase):
    def test_material_indexes_are_real_navigation_pages(self):
        for index in PLACEHOLDER_INDEXES:
            with self.subTest(index=index.relative_to(REPO_ROOT)):
                text = index.read_text(encoding="utf-8")
                self.assertNotIn("NEED TO PLAN", text)
                self.assertNotIn("Example:", text)
                self.assertRegex(text, re.compile(r"\[[^\]]+\]\([^)]+\)"))

    def test_obsolete_materials_and_redirect_pages_are_absent(self):
        for page in OBSOLETE_FILES:
            with self.subTest(page=page.relative_to(REPO_ROOT)):
                self.assertFalse(page.exists(), f"obsolete redirect remains: {page}")

    def test_practice_protocol_defines_shared_sequence(self):
        protocol = REPO_ROOT / "interviews-docs" / "practice-protocol.md"
        self.assertTrue(protocol.is_file(), "missing shared practice protocol")
        self.assertIn(PRACTICE_SEQUENCE, protocol.read_text(encoding="utf-8"))

    def test_handbook_links_every_chapter_and_role_path(self):
        text = HANDBOOK.read_text(encoding="utf-8")
        for chapter in range(1, 17):
            with self.subTest(chapter=chapter):
                self.assertRegex(
                    text,
                    re.compile(rf"\[[^\]]*{chapter:02d}[^\]]*\]\([^)]+\)"),
                )
        self.assertRegex(text, re.compile(r"\[[^\]]*RAG[^\]]*\]\([^)]+\)"))
        self.assertRegex(text, re.compile(r"\[[^\]]*LangGraph[^\]]*\]\([^)]+\)"))

    def test_dsa_practice_lane_has_navigation_and_executable_evidence(self):
        readme = (DSA_DIR / "README.md").read_text(encoding="utf-8")
        self.assertRegex(
            readme, re.compile(r"\[统一练习协议\]\(\.\./practice-protocol\.md\)")
        )
        self.assertRegex(readme, re.compile(r"\[C12\.02\]\([^)]+\)"))
        self.assertRegex(readme, re.compile(r"\[C12\.03\]\([^)]+\)"))
        self.assertRegex(
            readme,
            re.compile(
                r"可运行代码.{0,12}执行输出.{0,36}"
                r"(?:手动 trace/check|手动.*(?:trace|检查))",
                re.DOTALL,
            ),
        )

        for chapter in DSA_CHAPTERS:
            with self.subTest(chapter=chapter):
                self.assertIn(f"](./{chapter})", readme)
                text = (DSA_DIR / chapter).read_text(encoding="utf-8")
                self.assertIn("## 可执行证据", text)
                self.assertIn("边界 case", text)
                self.assertIn("复杂度", text)

        dp_text = (DSA_DIR / "05_动态规划.md").read_text(encoding="utf-8")
        self.assertNotIn("def one_dim_dp", dp_text)
        self.assertRegex(
            dp_text,
            re.compile(r"定义\s*`dp\[i\]`\s*表示.{0,60}最高金额", re.DOTALL),
        )
        self.assertRegex(dp_text, re.compile(r"dp\[i\]\s*=\s*max\("))

        robber_match = re.search(
            r"### House Robber（一维 DP）.*?```python\n(.*?)```", dp_text, re.DOTALL
        )
        self.assertIsNotNone(robber_match, "missing House Robber Python template")
        namespace = {}
        exec(robber_match.group(1), namespace)
        rob = namespace["rob"]
        for nums, expected in (
            ([], 0),
            ([7], 7),
            ([2, 1], 2),
            ([2, 7, 9, 3, 1], 12),
            ([0, 0, 0], 0),
        ):
            with self.subTest(nums=nums):
                self.assertEqual(rob(nums), expected)

        cheatsheet = (DSA_DIR / "CheatSheet.md").read_text(encoding="utf-8")
        window_section = cheatsheet.split("### 二分左边界", maxsplit=1)[0]
        self.assertRegex(window_section, re.compile(r"nums.{0,24}非负"))
        self.assertRegex(window_section, re.compile(r"limit\s*>=\s*0"))
        self.assertRegex(
            window_section, re.compile(r"移动左边界.{0,36}恢复.{0,12}合法")
        )

        array_text = (DSA_DIR / "01_数组与双指针.md").read_text(encoding="utf-8")
        linked_list_text = (DSA_DIR / "03_链表.md").read_text(encoding="utf-8")
        tree_text = (DSA_DIR / "04_二叉树.md").read_text(encoding="utf-8")
        search_text = (DSA_DIR / "06_回溯与搜索.md").read_text(encoding="utf-8")
        self.assertRegex(array_text, re.compile(r"intervals\.sort.*原地"))
        self.assertRegex(linked_list_text, re.compile(r"原地修改.*`next`"))
        self.assertRegex(search_text, re.compile(r"grid.*改成.*\"0\""))
        self.assertRegex(search_text, re.compile(r"Python 递归深度"))
        self.assertRegex(tree_text, re.compile(r"Python 递归深度"))
        self.assertRegex(tree_text, re.compile(r"LeetCode 236.*保证.*p.*q.*存在"))
        self.assertRegex(tree_text, re.compile(r"p.*q.*有效"))
        self.assertRegex(tree_text, re.compile(r"(?:迁移题|契约设计).{0,80}目标节点不存在"))

    def test_python_backend_series_states_current_concurrency_boundaries(self):
        containers = (PYTHON_DIR / "01-containers.md").read_text(encoding="utf-8")
        dataclass = (
            PYTHON_DIR / "05-typing-dataclass-pydantic.md"
        ).read_text(encoding="utf-8")
        asyncio = (PYTHON_DIR / "07-asyncio-blocking.md").read_text(
            encoding="utf-8"
        )
        gil = (PYTHON_DIR / "08-thread-process-gil.md").read_text(encoding="utf-8")

        self.assertNotIn("单个字节码级操作", containers)
        self.assertRegex(containers, re.compile(r"字节码.{0,50}(?:不是|不等于).{0,24}线程安全"))
        safe_and_unsafe_fences = [
            fence
            for fence in python_fences(dataclass)
            if "class ToolSpec" in fence and "field(default_factory=list)" in fence
        ]
        self.assertTrue(safe_and_unsafe_fences, "missing executable shallow-freeze example")
        safe_and_unsafe = safe_and_unsafe_fences[0]
        self.assertRegex(
            safe_and_unsafe,
            re.compile(r"@dataclass\(frozen=True\).*?tags: tuple\[str, \.\.\.\] = \(\)", re.DOTALL),
        )
        self.assertRegex(
            safe_and_unsafe,
            re.compile(
                r"@dataclass\(frozen=True\).*?field\(default_factory=list\).*?\.append\(",
                re.DOTALL,
            ),
        )
        namespace = {}
        exec(safe_and_unsafe, namespace)
        self.assertEqual(namespace["unsafe"].tags, ["retrieval"])
        self.assertRegex(dataclass, re.compile(r"(?:冻结|frozen).{0,56}浅层"))
        for construct in (
            "async with asyncio.timeout",
            "async with asyncio.TaskGroup",
            "group.create_task",
        ):
            with self.subTest(construct=construct):
                self.assertIn(construct, asyncio)
        self.assertRegex(asyncio, re.compile(r"CancelledError.{0,72}(?:传播|重新抛出)", re.DOTALL))
        structured_examples = [
            fence
            for fence in python_fences(asyncio)
            if "async with asyncio.timeout" in fence
        ]
        self.assertTrue(structured_examples, "missing runnable structured-concurrency example")
        structured_example = structured_examples[0]
        self.assertIn("finally", structured_example)
        compile(structured_example, "asyncio-example", "exec")
        with redirect_stdout(io.StringIO()):
            exec(structured_example, {})
        self.assertRegex(gil, re.compile(r"默认.{0,24}GIL.*(?:启用|enabled)"))
        self.assertRegex(gil, re.compile(r"Python 3\.13.{0,80}实验", re.DOTALL))
        self.assertRegex(
            gil,
            re.compile(r"Python 3\.14\+.{0,120}(?:正式支持|不再.*实验).{0,72}可选", re.DOTALL),
        )
        self.assertNotRegex(gil, re.compile(r"3\.13\+.{0,80}实验", re.DOTALL))

    def test_python_foundation_chapters_have_protocol_linked_evidence_tasks(self):
        expected_artifacts = {
            "02-reference-copy.md": "copy-evidence.txt",
            "03-iterator-generator.md": "generator-evidence.txt",
            "04-decorator-context-manager.md": "resource-evidence.txt",
            "06-exceptions.md": "exception-evidence.txt",
        }
        for filename, artifact in expected_artifacts.items():
            with self.subTest(filename=filename):
                text = (PYTHON_DIR / filename).read_text(encoding="utf-8")
                self.assertIn("[统一练习协议](../../practice-protocol.md)", text)
                self.assertIn("## 可执行证据", text)
                self.assertIn(artifact, text)

    def test_python_backend_series_has_executable_practice_and_dependency_boundary(self):
        readme = (PYTHON_DIR / "README.md").read_text(encoding="utf-8")
        pytest = (PYTHON_DIR / "09-pytest-mock-fixture.md").read_text(
            encoding="utf-8"
        )
        fastapi = (PYTHON_DIR / "10-fastapi-lifecycle-di.md").read_text(
            encoding="utf-8"
        )
        packaging = (PYTHON_DIR / "11-packaging-venv-lock.md").read_text(
            encoding="utf-8"
        )
        backend_index = (REPO_ROOT / "interviews-docs" / "02-后端" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "[统一练习协议](../../practice-protocol.md)",
            readme,
        )
        self.assertIn("C01", readme)
        self.assertIn("C07", readme)
        self.assertLess(readme.count("| P0 |"), readme.count("| P"))
        self.assertRegex(
            backend_index,
            re.compile(r"\[Python[^\]]*\]\(\.\./05-misc/python/README\.md\)"),
        )
        self.assertRegex(packaging, re.compile(r"pip freeze.{0,72}环境快照", re.DOTALL))
        self.assertRegex(packaging, re.compile(r"pip freeze.{0,96}(?:不是|并非).{0,36}锁", re.DOTALL))
        for text, required in ((pytest, "pytest -q"), (fastapi, "TestClient")):
            with self.subTest(required=required):
                self.assertIn("## 可执行证据", text)
                self.assertIn(required, text)

    def test_node_series_has_versioned_boundaries_and_executable_practice(self):
        readme = (NODE_DIR / "README.md").read_text(encoding="utf-8")
        event_loop = (NODE_DIR / "01-event-loop.md").read_text(encoding="utf-8")
        promise_errors = (
            NODE_DIR / "03-promise-async-await-errors.md"
        ).read_text(encoding="utf-8")
        commonjs_esm = (NODE_DIR / "05-commonjs-esm.md").read_text(
            encoding="utf-8"
        )
        retry = (NODE_DIR / "10-timeout-cancel-retry-idempotency.md").read_text(
            encoding="utf-8"
        )
        testing = (NODE_DIR / "11-testing-mock-integration.md").read_text(
            encoding="utf-8"
        )
        frameworks = (NODE_DIR / "12-express-fastify-nestjs.md").read_text(
            encoding="utf-8"
        )
        comparison = (
            REPO_ROOT / "interviews-docs" / "05-misc" / "python-vs-nodejs.md"
        ).read_text(encoding="utf-8")
        backend_index = (
            REPO_ROOT / "interviews-docs" / "02-后端" / "README.md"
        ).read_text(encoding="utf-8")

        self.assertIn("[统一练习协议](../../practice-protocol.md)", readme)
        self.assertRegex(readme, re.compile(r"C11.*P2", re.DOTALL))
        self.assertIn("libuv 1.45.0（Node.js 20）", event_loop)
        self.assertRegex(
            event_loop, re.compile(r"timers.{0,56}poll.{0,56}之后", re.DOTALL)
        )
        self.assertRegex(
            commonjs_esm,
            re.compile(r"v20\.17\.0.{0,88}v20\.19\.0", re.DOTALL),
        )
        self.assertRegex(
            commonjs_esm,
            re.compile(r"完全同步.{0,64}top-level await", re.DOTALL),
        )
        self.assertRegex(
            frameworks,
            re.compile(r"Express 5.{0,100}rejected Promise.{0,100}next", re.DOTALL),
        )
        self.assertRegex(
            promise_errors,
            re.compile(r"Node 15\+.{0,96}--unhandled-rejections", re.DOTALL),
        )

        retry_fences = re.findall(r"```js\n(.*?)```", retry, re.DOTALL)
        bounded_retry = next(
            (
                fence
                for fence in retry_fences
                if "retryable" in fence and "Retry-After" in fence
            ),
            None,
        )
        self.assertIsNotNone(bounded_retry, "missing bounded retry example")
        self.assertIn("AbortSignal", bounded_retry)
        self.assertIn("attempt === attempts", bounded_retry)
        self.assertLess(
            bounded_retry.index("attempt === attempts"),
            bounded_retry.index("await sleep"),
        )
        self.assertRegex(bounded_retry, re.compile(r"2 \*\*.*Math\.random", re.DOTALL))
        self.assertRegex(
            bounded_retry,
            re.compile(r"if \(!retryable\(error\)\) throw error"),
        )

        self.assertRegex(
            testing,
            re.compile(r"class .*Service.*constructor\(.*client", re.DOTALL),
        )
        self.assertRegex(
            testing,
            re.compile(r"new .*Service\(fakeClient\).{0,120}service\.", re.DOTALL),
        )
        self.assertRegex(
            comparison,
            re.compile(r"Python 3\.13.{0,88}实验", re.DOTALL),
        )
        self.assertRegex(
            comparison,
            re.compile(
                r"Python 3\.14\+.{0,120}(?:正式支持|不再.*实验).{0,72}可选",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            backend_index,
            re.compile(
                r"\[Node(?:\.js|JS)?[^\]]*\]\(\.\./05-misc/nodejs/README\.md\)"
            ),
        )
        self.assertRegex(
            backend_index,
            re.compile(r"\[Python vs NodeJS\]\(\.\./05-misc/python-vs-nodejs\.md\)"),
        )


if __name__ == "__main__":
    unittest.main()
