import asyncio
import io
import re
import subprocess
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = (
    REPO_ROOT
    / "AI_Agent_System_Practical_Reference"
    / "00_README_学习路线与资料使用说明.md"
)
REFERENCE_ROOT = REPO_ROOT / "AI_Agent_System_Practical_Reference"
ROLE_PATHS = REFERENCE_ROOT / "role_paths"
SURVEY = (
    REFERENCE_ROOT
    / "00_岗位调研与能力画像"
    / "01_AI_Agent应用岗位招聘调研报告.md"
)
CAPABILITY_MATRIX = (
    REFERENCE_ROOT
    / "00_岗位调研与能力画像"
    / "02_岗位核心能力矩阵.md"
)
SYSTEM_DESIGN = (
    REFERENCE_ROOT
    / "Part_04_项目与面试表达"
    / "11_项目设计模板与架构表达.md"
)
QUESTION_BANK = (
    REFERENCE_ROOT
    / "Part_04_项目与面试表达"
    / "12_高频面试题与答题闭环.md"
)
EVIDENCE_ROUTE = (
    REFERENCE_ROOT
    / "Part_04_项目与面试表达"
    / "13_总复习Checklist与学习计划.md"
)
MCP_CHAPTER = (
    REFERENCE_ROOT
    / "Part_01_Agent核心原理"
    / "03_工具调用_FunctionCalling_MCP_与行动能力.md"
)
LANGGRAPH_CHAPTER = (
    REFERENCE_ROOT
    / "Part_05_框架专项与实战Lab"
    / "14_LangGraph工程实战专项.md"
)
END_TO_END_LAB = (
    REFERENCE_ROOT
    / "Part_05_框架专项与实战Lab"
    / "16_端到端实战Lab与代码骨架.md"
)
REFERENCE_SOURCES = REFERENCE_ROOT / "references_参考来源.md"
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
NODE_CHAPTERS = tuple(f"{chapter:02d}-{name}.md" for chapter, name in (
    (1, "event-loop"),
    (2, "microtask-task"),
    (3, "promise-async-await-errors"),
    (4, "stream-backpressure"),
    (5, "commonjs-esm"),
    (6, "typescript-types"),
    (7, "process-worker-child-process"),
    (8, "memory-leak-async-resource"),
    (9, "http-lifecycle"),
    (10, "timeout-cancel-retry-idempotency"),
    (11, "testing-mock-integration"),
    (12, "express-fastify-nestjs"),
))
AI_INTERVIEW_DIR = REPO_ROOT / "interviews-docs" / "01-AI"
BACKEND_INTERVIEW_DIR = REPO_ROOT / "interviews-docs" / "02-后端"
LLM_FAILURE_BOUNDARIES = AI_INTERVIEW_DIR / "llm-failure-boundaries.md"
PYTHON_DEBUGGING = BACKEND_INTERVIEW_DIR / "python-debugging.md"
SQL_POSTGRESQL = BACKEND_INTERVIEW_DIR / "sql-postgresql.md"
LEARNING_REFERENCE_MARKER = "<!-- 练习分隔线：完成冷答后再继续 -->"


def python_fences(text: str) -> list[str]:
    return re.findall(r"```python\n(.*?)```", text, re.DOTALL)


class LearningMaterialsTest(unittest.TestCase):
    def assert_interview_module_contract(
        self, path: Path, competency_ids: tuple[str, ...]
    ) -> tuple[str, str]:
        text = path.read_text(encoding="utf-8")
        self.assertIn("[统一练习协议](../practice-protocol.md)", text)
        for competency_id in competency_ids:
            self.assertIn(competency_id, text)
        self.assertIn(LEARNING_REFERENCE_MARKER, text)
        cold_zone, reference_zone = text.split(LEARNING_REFERENCE_MARKER, maxsplit=1)
        self.assertRegex(cold_zone, re.compile(r"冷启动|冷答"))
        self.assertRegex(cold_zone, re.compile(r"迁移题"))
        self.assertRegex(cold_zone, re.compile(r"延迟复测"))
        self.assertRegex(cold_zone, re.compile(r"`[^`]+\.(?:py|sql|md|txt|json)`"))
        self.assertRegex(
            cold_zone,
            re.compile(
                r"(?:阅读|读完).{0,40}不(?:能|算).{0,24}(?:掌握|证据)",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            cold_zone,
            re.compile(r"提示.{0,40}不(?:能|算).{0,24}独立证据", re.DOTALL),
        )
        self.assertRegex(reference_zone, re.compile(r"参考|评分|rubric", re.IGNORECASE))
        return cold_zone, reference_zone

    def test_interview_modules_declare_exactly_one_primary_competency(self):
        expected_primary = {
            LLM_FAILURE_BOUNDARIES: "C02.01",
            PYTHON_DEBUGGING: "C01.02",
            SQL_POSTGRESQL: "C12.01",
        }
        for path, expected in expected_primary.items():
            with self.subTest(module=path.name):
                text = path.read_text(encoding="utf-8")
                primary_lines = re.findall(r"(?m)^主要能力：([^\n]+)$", text)
                self.assertEqual(len(primary_lines), 1, f"{path.name} needs one primary line")
                primary_ids = re.findall(r"C\d{2}\.\d{2}", primary_lines[0])
                self.assertEqual(
                    primary_ids,
                    [expected],
                    f"{path.name} must declare exactly one primary competency",
                )

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
        self.assertIn("[JD 差异层与实用入口](role_paths/README.md)", text)

    def test_handbook_uses_one_canonical_competency_route(self):
        handbook = HANDBOOK.read_text(encoding="utf-8")
        survey = SURVEY.read_text(encoding="utf-8")
        matrix = CAPABILITY_MATRIX.read_text(encoding="utf-8")

        self.assertRegex(handbook, re.compile(r"按.*(?:能力缺口|缺口能力).*查阅"))
        self.assertNotRegex(handbook, re.compile(r"按\s*Part\s*01\s*[→到-]\s*Part\s*05.*顺序读"))
        self.assertIn(".codex/skills/interview-prep-coach/references/competency-model.md", handbook)

        self.assertRegex(survey, re.compile(r"2026-04-29.*历史.*快照", re.DOTALL))
        self.assertRegex(survey, re.compile(r"国际.*中高级|中高级.*国际"))
        self.assertRegex(
            survey,
            re.compile(r"不是.*当前.*中国大陆.*初中级.*基线", re.DOTALL),
        )
        self.assertNotIn("中文语境求职为主，英文岗位为辅", survey)
        self.assertRegex(
            survey,
            re.compile(
                r"目标解读语境.*中国大陆.*"
                r"实际样本.*国际公司.*英文\s*JD.*为主"
            ),
        )

        for score in ("96", "94", "93", "91", "88", "86", "84", "82", "80", "79"):
            with self.subTest(score=score):
                self.assertNotRegex(matrix, re.compile(rf"(?<!\d){score}(?!\d)"))
        self.assertIn("C01–C13", matrix)
        self.assertIn("competency-model.md", matrix)
        self.assertRegex(matrix, re.compile(r"稳定\s*ID"))
        self.assertRegex(matrix, re.compile(r"JD.*覆盖|覆盖.*JD"))

        obsolete_routes = (
            CAPABILITY_MATRIX.with_name("03_章节重要性映射表.md"),
            CAPABILITY_MATRIX.with_name("04_学习优先级建议.md"),
        )
        for path in obsolete_routes:
            with self.subTest(path=path.name):
                self.assertFalse(path.exists(), f"stale route remains: {path.name}")

        self.assertEqual(
            sorted(path.name for path in ROLE_PATHS.glob("*.md")),
            ["README.md"],
        )
        role_index = (ROLE_PATHS / "README.md").read_text(encoding="utf-8")
        self.assertIn("C01–C13", role_index)
        self.assertRegex(role_index, re.compile(r"JD.*覆盖|覆盖.*JD"))
        self.assertIn("../Part_04_项目与面试表达/13_总复习Checklist与学习计划.md", role_index)

    def test_generic_system_designs_are_truth_safe_exercises(self):
        text = SYSTEM_DESIGN.read_text(encoding="utf-8")

        self.assertRegex(text, re.compile(r"通用设计.*(?:练习|提案)"))
        self.assertRegex(text, re.compile(r"不代表.*(?:已实现|真实项目)"))
        self.assertNotRegex(text, re.compile(r"我(?:设计并实现|做了|做的|加入了|实现了)"))
        top_level_numbers = [
            int(number)
            for number in re.findall(r"(?m)^## (\d+)\.", text)
            if number != "0"
        ]
        self.assertEqual(top_level_numbers, list(range(1, len(top_level_numbers) + 1)))

    def test_system_design_chapter_requires_cold_evidence_before_reference(self):
        text = SYSTEM_DESIGN.read_text(encoding="utf-8")
        marker = "<!-- 系统设计参考分隔线：先作答，再继续 -->"

        self.assertRegex(text, re.compile(r"主要能力.*C09\.01"))
        self.assertIn(marker, text)
        cold_zone, reference_zone = text.split(marker, maxsplit=1)
        self.assertRegex(cold_zone, re.compile(r"冷启动.*系统设计题"))
        self.assertIn("cold-system-design.md", cold_zone)
        self.assertIn("changed-constraint.md", cold_zone)
        self.assertIn("delayed-system-design.md", cold_zone)
        self.assertRegex(cold_zone, re.compile(r"改变约束|约束改变"))
        self.assertRegex(cold_zone, re.compile(r"延迟复测"))
        self.assertRegex(
            cold_zone,
            re.compile(r"阅读.*参考区.*勾选.*不算.*证据", re.DOTALL),
        )
        self.assertIn("项目模板一：企业知识库 RAG Agent", reference_zone)
        self.assertLess(text.index(marker), text.index("项目模板一"))

    def test_question_bank_hides_answers_until_after_cold_attempt(self):
        text = QUESTION_BANK.read_text(encoding="utf-8")
        marker = "<!-- 冷答分隔线：先作答，再继续 -->"
        answer_heading = "## 3. 参考答案与评分"

        self.assertIn(marker, text)
        self.assertIn(answer_heading, text)
        questions, answers = text.split(marker, maxsplit=1)
        self.assertGreaterEqual(len(re.findall(r"(?m)^### Q\d+：", questions)), 20)
        self.assertNotIn("推荐回答", questions)
        self.assertNotRegex(questions, re.compile(r"参考答案|评分标准|评分要点"))
        self.assertIn("<details>", answers)
        self.assertIn("评分要点", answers)
        self.assertNotRegex(text, re.compile(r"(?:看|读)(?:完|过).{0,12}答案.{0,12}(?:就是|算作|作为).{0,12}证据"))

    def test_chapter_13_is_the_only_public_two_to_three_week_evidence_route(self):
        text = EVIDENCE_ROUTE.read_text(encoding="utf-8")
        route_heading = re.compile(r"(?m)^## \d+\. 2–3 周.*证据路线$")

        self.assertEqual(len(route_heading.findall(text)), 1)
        for competency in range(1, 14):
            with self.subTest(competency=competency):
                self.assertRegex(text, re.compile(rf"\bC{competency:02d}\b"))
        self.assertRegex(text, re.compile(r"每个学习日.*可检查产物"))
        self.assertRegex(text, re.compile(r"私人.*\.local/interview-prep/.*日程", re.DOTALL))

        week_blocks = re.findall(
            r"(?ms)^### 第[123]周.*?(?=^### 第[123]周|^## |\Z)",
            text,
        )
        self.assertGreaterEqual(len(week_blocks), 2)
        for block in week_blocks:
            with self.subTest(week=block.splitlines()[0]):
                self.assertIn("可检查产物", block)
                self.assertRegex(block, re.compile(r"`[^`]+\.(?:py|md|json|txt|sql)`"))

        for artifact_type in ("代码", "设计", "冷答", "项目", "模拟"):
            with self.subTest(artifact_type=artifact_type):
                self.assertIn(artifact_type, text)

        historical_records = {REFERENCE_ROOT / "CHANGELOG.md"}
        public_route_files = sorted(
            path
            for path in REFERENCE_ROOT.rglob("*.md")
            if path not in historical_records
        )
        for path in public_route_files:
            with self.subTest(route_file=path.relative_to(REFERENCE_ROOT)):
                public_text = path.read_text(encoding="utf-8")
                self.assertNotRegex(
                    public_text,
                    re.compile(
                        r"(?:\d+|[一二三四五六七八九十]+)\s*天"
                        r"(?:学习|阅读|复习)?(?:计划|建议|路线)"
                    ),
                )
                sequential_day_headings = re.findall(
                    r"(?mi)^#{2,4}\s*(?:Day\s*\d+|第\s*\d+\s*天)",
                    public_text,
                )
                self.assertLess(
                    len(sequential_day_headings),
                    2,
                    f"sequential public day route in {path}",
                )

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

    def test_node_review_contracts_protect_evidence_and_runtime_boundaries(self):
        readme = (NODE_DIR / "README.md").read_text(encoding="utf-8")
        retry = (NODE_DIR / "10-timeout-cancel-retry-idempotency.md").read_text(
            encoding="utf-8"
        )
        testing = (NODE_DIR / "11-testing-mock-integration.md").read_text(
            encoding="utf-8"
        )
        frameworks = (NODE_DIR / "12-express-fastify-nestjs.md").read_text(
            encoding="utf-8"
        )
        promise_errors = (
            NODE_DIR / "03-promise-async-await-errors.md"
        ).read_text(encoding="utf-8")
        root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        interviews_index = (REPO_ROOT / "interviews-docs" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertRegex(
            readme,
            re.compile(r"能力 C11（Node\.js、TypeScript 与跨运行时\s*取舍）的\*\*默认目标为 2\*\*"),
        )
        for chapter in NODE_CHAPTERS:
            with self.subTest(chapter=chapter):
                text = (NODE_DIR / chapter).read_text(encoding="utf-8")
                self.assertIn("## 可执行证据", text)
                self.assertIn("[统一练习协议](../../practice-protocol.md)", text)
                self.assertRegex(text, re.compile(r"若无 Node.{0,160}(?:手动|检查|trace)", re.DOTALL))
                self.assertIn("可检查结果", text)
                self.assertIn("访问日期：2026-07-19。", text)

        retry_example = next(
            fence
            for fence in re.findall(r"```js\n(.*?)```", retry, re.DOTALL)
            if "async function retry" in fence
        )
        retryable_function = re.search(
            r"function retryable\(error\) \{(.*?)\n\}", retry_example, re.DOTALL
        )
        self.assertIsNotNone(retryable_function, "missing retry classifier")
        classifier = retryable_function.group(1)
        self.assertIn('error?.name === "AbortError") return false', classifier)
        self.assertIn(
            '["ECONNRESET", "ETIMEDOUT", "EAI_AGAIN"].includes(error?.code)) return true',
            classifier,
        )
        self.assertIn("error?.status === 429", classifier)
        self.assertIn("error?.status >= 500 && error?.status < 600", classifier)
        self.assertRegex(
            retry_example,
            re.compile(r"for \(let attempt = 1; attempt <= attempts; attempt \+= 1\)"),
        )
        attempt_start = retry_example.index("for (let attempt")
        abort_check = retry_example.index("signal?.throwIfAborted()")
        operation = retry_example.index("return await operation({ signal })")
        final_attempt = retry_example.index("if (attempt === attempts) throw error")
        retry_after_parse = retry_example.index("function retryAfterMs")
        retry_after_wait = retry_example.index("retryAfterMs(error.retryAfter)")
        delay = retry_example.index("await sleep(delayMs, undefined, { signal })")
        self.assertGreater(abort_check, attempt_start)
        self.assertLess(abort_check, operation)
        self.assertLess(operation, final_attempt)
        self.assertLess(retry_after_parse, retry_after_wait)
        self.assertLess(retry_after_wait, delay)
        self.assertLess(final_attempt, delay)
        self.assertIn("Math.max(fullJitter, retryAfterMs(error.retryAfter))", retry_example)

        service_class = re.search(
            r"class SearchService \{(.*?)\n\}", testing, re.DOTALL
        )
        self.assertIsNotNone(service_class, "missing production SearchService")
        self.assertIn("this.client.search(query)", service_class.group(1))
        self.assertRegex(
            testing,
            re.compile(
                r"new SearchService\(fakeClient\).*?await service\.answer\(\"rag\"\)",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            frameworks,
            re.compile(r"Express 5.{0,120}rejected Promise.{0,120}next", re.DOTALL),
        )
        self.assertRegex(frameworks, re.compile(r"Express 4.{0,80}不应", re.DOTALL))
        self.assertRegex(
            promise_errors,
            re.compile(
                r"Node 15\+.{0,120}Node 26\.x.{0,120}--unhandled-rejections=throw",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            promise_errors,
            re.compile(r"没有.{0,80}unhandledRejection.{0,120}listener", re.DOTALL),
        )
        self.assertRegex(
            promise_errors,
            re.compile(r"listener.{0,120}(?:改变|改变了).{0,80}(?:fallback|回退)", re.DOTALL),
        )
        self.assertNotIn("05-misc/nodejs/README.md", root_readme)
        self.assertNotIn("05-misc/python-vs-nodejs.md", root_readme)
        for text in (root_readme, interviews_index):
            self.assertNotRegex(
                text,
                re.compile(r"\[[^\]]*Node[^\]]*\]\([^)]*05-misc/nodejs/README\.md\)"),
            )
            self.assertNotRegex(
                text,
                re.compile(r"\[Python vs NodeJS\]\([^)]*05-misc/python-vs-nodejs\.md\)"),
            )

    def test_agent_assisted_development_materials_keep_evidence_boundaries(self):
        practice_dir = REPO_ROOT / "best-practice" / "agent-assisted-development"
        readme = practice_dir / "README.md"
        checklist = practice_dir / "workflow-checklist.md"
        index = (REPO_ROOT / "best-practice" / "README.md").read_text(encoding="utf-8")

        self.assertFalse((REPO_ROOT / "best-practice" / "vibe-coding").exists())
        docs = sorted(path.name for path in practice_dir.glob("*.md"))
        self.assertEqual(docs, ["README.md", "workflow-checklist.md"])
        for path in (readme, checklist):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing {path.name}")
                tracked = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", str(path.relative_to(REPO_ROOT))],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(tracked.returncode, 0, f"untracked doc: {path}")
        self.assertIn(
            "[受控的 Agent 辅助开发](agent-assisted-development/README.md)", index
        )

        text = "\n".join(
            (readme.read_text(encoding="utf-8"), checklist.read_text(encoding="utf-8"))
        )
        self.assertNotIn("我做过一个代码助手方向的实践", text)
        self.assertRegex(
            text,
            re.compile(r"历史.*公共.*vibe coding.*受控.*Agent 辅助开发", re.DOTALL),
        )
        self.assertIn("https://x.com/karpathy/status/1886192184808149383", text)
        self.assertIn("访问日期：2026-07-19。", text)
        for evidence in (
            "https://github.com/ZophiaWong/forge-harness/blob/"
            "9c1b1dbb0566e9053457db50e64cd374848de856/test/tools/toolRuntime.test.ts",
            "https://github.com/ZophiaWong/forge-harness/blob/"
            "9c1b1dbb0566e9053457db50e64cd374848de856/test/extensions/childSessions.test.ts",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, text)
        minimal_loop = (
            "https://github.com/ZophiaWong/forge-harness/blob/"
            "9c1b1dbb0566e9053457db50e64cd374848de856/"
            "test/core/minimalLoop.test.ts#L1632-L1770"
        )
        self.assertRegex(
            text,
            re.compile(rf"最终回答.{{0,100}}一次恢复.{{0,240}}{re.escape(minimal_loop)}", re.DOTALL),
        )
        self.assertRegex(
            text,
            re.compile(
                r"已提议：外部工具以及 MCP 或插件路由.*?c15b.*?"
                r"c15b-async-child-sessions-parallel-handoff\.md",
                re.DOTALL,
            ),
        )
        self.assertNotRegex(text, re.compile(r"已计划：.{0,120}(?:MCP|插件路由)", re.DOTALL))
        self.assertRegex(
            text,
            re.compile(r"只有实际完成.*?才可以说.*?按这个流程练习过", re.DOTALL),
        )
        self.assertRegex(
            text,
            re.compile(r"没有保留.*?可检查.*?证据没有保留", re.DOTALL),
        )
        self.assertRegex(text, re.compile(r"没有实践.*?只描述.*?计划", re.DOTALL))
        candidate_metrics = re.search(
            r"(?m)^(把下面内容当作测量候选指标.*?)(?:\n[ \t]*\n|\Z)",
            readme.read_text(encoding="utf-8"),
            re.DOTALL,
        )
        self.assertIsNotNone(candidate_metrics, "missing candidate metrics paragraph")
        self.assertRegex(candidate_metrics.group(1), re.compile(r"方法.*?记录", re.DOTALL))
        self.assertNotRegex(candidate_metrics.group(1), re.compile(r"\d+(?:\.\d+)?\s*(?:%|百分之|倍|分钟|小时)"))
        result_verbs = r"(?:减少|增加|提高|提升|下降|降低|节省)"
        count_or_point_units = r"(?:次|项|百分点|个(?:点)?|点)"
        self.assertNotRegex(
            candidate_metrics.group(1),
            re.compile(
                rf"(?:{result_verbs}.{{0,12}}\d+\s*{count_or_point_units}|"
                rf"\d+\s*{count_or_point_units}.{{0,12}}{result_verbs})"
            ),
        )
        self.assertIn("范围 → 上下文 → 计划 → 最小 patch → 验证 → review → bad case 回流", text)

    def test_llm_failure_boundaries_require_classification_and_bounded_remedy(self):
        cold_zone, reference_zone = self.assert_interview_module_contract(
            LLM_FAILURE_BOUNDARIES, ("C02.01",)
        )
        self.assertRegex(cold_zone, re.compile(r"分类.{0,80}故障模式", re.DOTALL))
        self.assertRegex(cold_zone, re.compile(r"选择.{0,80}处理|补救", re.DOTALL))
        self.assertRegex(
            reference_zone,
            re.compile(
                r"temperature.{0,240}(?:不确定|非确定)|"
                r"(?:不确定|非确定).{0,240}temperature",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertRegex(
            reference_zone,
            re.compile(
                r"token.{0,40}概率分布.{0,60}更尖锐.{0,80}通常.{0,40}降低.{0,24}采样随机性",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertRegex(
            reference_zone,
            re.compile(r"不.{0,12}直接.{0,24}缩小.{0,30}候选\s*token.{0,20}取值范围", re.IGNORECASE),
        )
        self.assertNotIn("收窄采样范围", reference_zone)
        for boundary in ("结构化", "schema", "确定性后处理", "拒答", "不确定", "升级", "弃答"):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, reference_zone)
        self.assertRegex(reference_zone, re.compile(r"不代表.*项目.*已实现", re.DOTALL))

    def test_python_debugging_module_demands_executed_diagnostic_evidence(self):
        cold_zone, reference_zone = self.assert_interview_module_contract(
            PYTHON_DEBUGGING, ("C01.02",)
        )
        for step in ("复现", "traceback", "日志", "假设", "最小修复", "回归测试"):
            with self.subTest(step=step):
                self.assertIn(step, cold_zone + reference_zone)
        python_examples = python_fences(reference_zone)
        self.assertTrue(python_examples, "missing standard-library debugging fixture")
        self.assertTrue(
            any("unittest" in example and "assert" in example for example in python_examples),
            "debugging fixture must include a runnable regression test",
        )
        runnable_example = next(
            example for example in python_examples if "class AverageLatencyTest" in example
        )
        namespace = {"__name__": "embedded_debugging_evidence"}
        exec(compile(runnable_example, str(PYTHON_DEBUGGING), "exec"), namespace)
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(
            namespace["AverageLatencyTest"]
        )
        result = unittest.TestResult()
        suite.run(result)
        self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
        self.assertRegex(reference_zone, re.compile(r"0–1.{0,100}未复现就猜", re.DOTALL))
        self.assertRegex(reference_zone, re.compile(r"0–1.{0,140}重写整个函数", re.DOTALL))

    def test_sql_postgresql_module_covers_query_and_plan_reasoning_without_execution_claims(self):
        cold_zone, reference_zone = self.assert_interview_module_contract(
            SQL_POSTGRESQL, ("C07.03", "C12.01")
        )
        combined = cold_zone + reference_zone
        for construct in (
            "JOIN", "GROUP BY", "HAVING", "OVER (", "TRANSACTION", "CREATE INDEX", "EXPLAIN"
        ):
            with self.subTest(construct=construct):
                self.assertIn(construct, combined.upper())
        self.assertRegex(cold_zone, re.compile(r"预期行|预期结果"))
        self.assertRegex(cold_zone, re.compile(r"计划.{0,40}属性|计划.{0,40}节点", re.DOTALL))
        self.assertRegex(
            combined,
            re.compile(r"PostgreSQL.{0,120}(?:假设|假定)", re.IGNORECASE | re.DOTALL),
        )
        self.assertRegex(
            combined,
            re.compile(
                r"没有.{0,20}(?:PostgreSQL|psql).{0,100}(?:不要|不得).{0,40}已执行",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertNotRegex(combined, re.compile(r"已在\s*PostgreSQL.{0,20}(?:运行|执行|验证)", re.IGNORECASE))

        transaction_example = next(
            block
            for block in re.findall(r"```sql\n(.*?)```", reference_zone, re.DOTALL)
            if "UPDATE payments" in block
        )
        self.assertIn("WHERE account_id = 1 AND status = 'paid'", transaction_example)
        self.assertRegex(transaction_example, re.compile(r"RETURNING\s+payment_id", re.IGNORECASE))
        self.assertNotIn("FOR UPDATE", transaction_example)
        self.assertRegex(
            reference_zone,
            re.compile(
                r"READ COMMITTED.{0,200}等待.{0,200}重新检查.{0,80}WHERE.{0,120}(?:0 行|零行)",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertRegex(
            reference_zone,
            re.compile(
                r"FOR UPDATE.{0,220}(?:先读|先读取).{0,160}(?:跨行|业务不变量)",
                re.IGNORECASE | re.DOTALL,
            ),
        )

    def test_new_competency_gap_modules_are_linked_from_topic_indexes(self):
        ai_index = (AI_INTERVIEW_DIR / "README.md").read_text(encoding="utf-8")
        backend_index = (BACKEND_INTERVIEW_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("[LLM 失败边界](llm-failure-boundaries.md)", ai_index)
        self.assertIn("[Python 调试](python-debugging.md)", backend_index)
        self.assertIn("[SQL 与 PostgreSQL](sql-postgresql.md)", backend_index)

    def test_mcp_chapter_uses_stable_lifecycle_and_security_boundaries(self):
        text = MCP_CHAPTER.read_text(encoding="utf-8")
        marker = "<!-- MCP 参考分隔线：完成冷答后再继续 -->"

        self.assertIn("主要能力：C04.03", text)
        self.assertIn(marker, text)
        cold_zone, reference_zone = text.split(marker, maxsplit=1)
        self.assertIn("mcp-boundary-design.md", cold_zone)
        self.assertRegex(cold_zone, re.compile(r"冷启动|冷答"))
        self.assertRegex(cold_zone, re.compile(r"改变约束|迁移题"))
        self.assertIn("延迟复测", cold_zone)
        self.assertRegex(
            cold_zone,
            re.compile(r"(?:阅读|复制).{0,50}不(?:算|是).{0,30}(?:独立)?证据", re.DOTALL),
        )

        roles = reference_zone.split("### MCP 的分层", maxsplit=1)[0]
        for role in ("Host", "Client", "Server"):
            self.assertIn(role, roles)
        self.assertRegex(
            roles,
            re.compile(r"每个.*MCP Server.{0,80}(?:一个|对应).*MCP Client", re.DOTALL),
        )

        layers, lifecycle_and_after = reference_zone.split("### MCP 生命周期", maxsplit=1)
        self.assertIn("JSON-RPC 2.0", layers)
        self.assertRegex(layers, re.compile(r"数据层.{0,120}传输层", re.DOTALL))
        lifecycle = lifecycle_and_after.split("### 标准传输", maxsplit=1)[0]
        for token in (
            "initialize",
            "protocolVersion",
            "capabilities",
            "notifications/initialized",
            "协商成功的能力",
            "关闭传输",
        ):
            with self.subTest(lifecycle_token=token):
                self.assertIn(token, lifecycle)

        transports = lifecycle_and_after.split("### 标准传输", maxsplit=1)[1].split(
            "### Server primitives", maxsplit=1
        )[0]
        self.assertIn("stdio", transports)
        self.assertIn("Streamable HTTP", transports)
        self.assertRegex(transports, re.compile(r"HTTP\+SSE.{0,100}(?:旧|取代|替代)", re.DOTALL))
        self.assertNotRegex(transports, re.compile(r"当前.{0,24}标准.{0,24}HTTP\+SSE"))

        primitives = lifecycle_and_after.split("### Server primitives", maxsplit=1)[1].split(
            "### 信任与授权", maxsplit=1
        )[0]
        self.assertRegex(primitives, re.compile(r"Tools.{0,100}模型控制", re.DOTALL))
        self.assertRegex(primitives, re.compile(r"Resources.{0,100}应用控制", re.DOTALL))
        self.assertRegex(primitives, re.compile(r"Prompts.{0,100}用户控制", re.DOTALL))

        security = lifecycle_and_after.split("### 信任与授权", maxsplit=1)[1]
        for boundary in ("不可信输入", "最小权限", "URI", "输入校验", "用户同意"):
            with self.subTest(security_boundary=boundary):
                self.assertIn(boundary, security)
        self.assertRegex(security, re.compile(r"HTTP.{0,120}授权", re.DOTALL))
        self.assertRegex(security, re.compile(r"stdio.{0,120}环境", re.IGNORECASE | re.DOTALL))
        self.assertRegex(security, re.compile(r"不得.{0,32}token passthrough", re.IGNORECASE))
        self.assertRegex(reference_zone, re.compile(r"设计示例.{0,100}未.*仓库.*执行", re.DOTALL))

    def langgraph_practice_zones(self):
        cases = (
            (
                LANGGRAPH_CHAPTER,
                "<!-- LangGraph 参考分隔线：完成冷答后再继续 -->",
                "C03.03",
                "langgraph-hitl-cold.md",
            ),
            (
                END_TO_END_LAB,
                "<!-- Lab 参考分隔线：完成冷答后再继续 -->",
                "C08.02",
                "agent-lab-cold-design.md",
            ),
        )
        zones = []
        for path, marker, competency, artifact in cases:
            text = path.read_text(encoding="utf-8")
            self.assertIn(marker, text)
            cold_zone, reference_zone = text.split(marker, maxsplit=1)
            zones.append((path, cold_zone, reference_zone))
            with self.subTest(path=path.name):
                self.assertIn(f"主要能力：{competency}", cold_zone)
                self.assertRegex(cold_zone, re.compile(r"冷启动|冷答"))
                self.assertIn(artifact, cold_zone)
                self.assertRegex(cold_zone, re.compile(r"改变约束|迁移题"))
                self.assertIn("延迟复测", cold_zone)
                self.assertNotIn("compile(checkpointer=", cold_zone)
                self.assertIn("compile(checkpointer=", reference_zone)
        return zones

    def test_langgraph_practice_puts_cold_evidence_before_reference(self):
        self.langgraph_practice_zones()

    def test_langgraph_approval_nodes_fail_closed_on_unknown_decisions(self):
        for path, _, reference_zone in self.langgraph_practice_zones():
            with self.subTest(path=path.name):
                approval = next(
                    block
                    for block in python_fences(reference_zone)
                    if "def approval_node" in block
                )
                compile(approval, f"{path.name}:approval_node", "exec")
                self.assertIn("if not isinstance(review, dict):", approval)
                self.assertIn('decision = review.get("decision")', approval)
                self.assertIn('if decision == "reject":', approval)
                self.assertIn('if decision not in {"approve", "edit"}:', approval)
                self.assertRegex(
                    approval,
                    re.compile(
                        r"if decision not in \{\"approve\", \"edit\"\}:.*?"
                        r'"decision": "pending".*?"validation_error"',
                        re.DOTALL,
                    ),
                )
                self.assertLess(
                    approval.index('if decision not in {"approve", "edit"}:'),
                    approval.index("validate_action("),
                )
                self.assertLess(
                    approval.index("validate_action("),
                    approval.rindex('"decision": "approved"'),
                )
                self.assertRegex(
                    approval,
                    re.compile(
                        r'"decision": "rejected".*?"validation_error": None',
                        re.DOTALL,
                    ),
                )
                self.assertRegex(
                    approval,
                    re.compile(
                        r'"decision": "approved".*?"validation_error": None',
                        re.DOTALL,
                    ),
                )
                self.assertNotIn('review.get("action", state["proposed"])', approval)

    def test_langgraph_partial_state_updates_clear_stale_validation_errors(self):
        for path, _, reference_zone in self.langgraph_practice_zones():
            with self.subTest(path=path.name):
                state_schema = next(
                    block
                    for block in python_fences(reference_zone)
                    if "class AgentState" in block
                )
                self.assertRegex(state_schema, re.compile(r"validation_error:\s*str\s*\|\s*None"))
                self.assertRegex(state_schema, re.compile(r"tool_result:\s*dict\s*\|\s*None"))

                approval = next(
                    block
                    for block in python_fences(reference_zone)
                    if "def approval_node" in block
                ).replace("from langgraph.types import interrupt\n", "")
                review = {"decision": "approev", "action": {"malicious": True}}

                def interrupt(_payload):
                    return review

                def validate_action(candidate, **_kwargs):
                    return SimpleNamespace(ok=True, value=candidate, error=None)

                namespace = {
                    "AgentState": dict,
                    "Action": dict,
                    "ACTION_ALLOWLIST": {"send_notification", "create_ticket"},
                    "interrupt": interrupt,
                    "validate_action": validate_action,
                }
                exec(compile(approval, f"{path.name}:approval-transition", "exec"), namespace)

                state = {"proposed": {"kind": "send_notification"}}
                state.update(namespace["approval_node"](state))
                self.assertEqual(state["decision"], "pending")
                self.assertIsInstance(state["validation_error"], str)
                self.assertEqual(namespace["route_after_approval"](state), "approval")

                review.clear()
                review.update(
                    {
                        "decision": "edit",
                        "action": {"kind": "send_notification", "body": "checked"},
                    }
                )
                state.update(namespace["approval_node"](state))
                self.assertEqual(state["decision"], "approved")
                self.assertIsNone(state["validation_error"])
                self.assertEqual(namespace["route_after_approval"](state), "execute")

    def test_langgraph_async_resume_and_outcome_states_are_coherent(self):
        for path, _, reference_zone in self.langgraph_practice_zones():
            with self.subTest(path=path.name):
                invocation = next(
                    block
                    for block in python_fences(reference_zone)
                    if "Command(resume=" in block
                )
                compile(invocation, f"{path.name}:resume", "exec")
                self.assertIn("async def run_approval_roundtrip", invocation)
                self.assertEqual(invocation.count("await graph.ainvoke("), 2)
                self.assertNotIn("graph.invoke(", invocation)

                execution = next(
                    block
                    for block in python_fences(reference_zone)
                    if "async def execute" in block
                )
                compile(execution, f"{path.name}:execute", "exec")
                self.assertIn('if outcome == "success":', execution)
                self.assertIn('if outcome == "failure":', execution)
                self.assertIn("lookup", execution)
                self.assertIn(
                    '"executed": None, "execution_status": "unknown"', execution
                )
                timeout_body = execution.split(
                    "except (TimeoutError, ConnectionError):", maxsplit=1
                )[1].split("\n\n    outcome =", maxsplit=1)[0]
                self.assertNotIn('"executed": False', timeout_body)
                self.assertNotIn('"execution_status": "failed"', timeout_body)
                self.assertRegex(
                    execution,
                    re.compile(
                        r'if outcome == "failure":.*?'
                        r'"executed": False.*?"execution_status": "failed"',
                        re.DOTALL,
                    ),
                )
                unknown_lookup = execution.split(
                    'if outcome == "unknown":', maxsplit=1
                )[1].split('\n\n    if outcome == "success":', maxsplit=1)[0]
                self.assertIn("lookup", unknown_lookup)
                self.assertIn("except (TimeoutError, ConnectionError):", unknown_lookup)
                self.assertIn("cached = None", unknown_lookup)
                self.assertNotIn('"executed": False', unknown_lookup)
                self.assertNotIn('"execution_status": "failed"', unknown_lookup)
                self.assertLess(
                    execution.index('if outcome == "failure":'),
                    execution.rindex(
                        '"executed": None, "execution_status": "unknown"'
                    ),
                )

    def test_langgraph_lookup_transport_uncertainty_returns_unknown(self):
        class UncertainTool:
            async def send(self, *_args, **_kwargs):
                raise TimeoutError("initial result unknown")

            async def execute(self, *_args, **_kwargs):
                raise TimeoutError("initial result unknown")

            async def lookup(self, **_kwargs):
                raise ConnectionError("lookup also uncertain")

            @staticmethod
            def classify_outcome(_action, result):
                return "unknown" if result is None else "success"

        for path, _, reference_zone in self.langgraph_practice_zones():
            with self.subTest(path=path.name):
                execution = next(
                    block
                    for block in python_fences(reference_zone)
                    if "async def execute" in block
                )
                tool = UncertainTool()

                def validate_action(action, **_kwargs):
                    return SimpleNamespace(ok=True, value=action, error=None)

                namespace = {
                    "Action": dict,
                    "AgentState": dict,
                    "validate_action": validate_action,
                    "ACTION_ALLOWLIST": {"send_notification", "create_ticket"},
                    "notification_tool": tool,
                    "tool_gateway": tool,
                    "classify_tool_outcome": (
                        lambda result, _action: "unknown" if result is None else "success"
                    ),
                }
                exec(compile(execution, f"{path.name}:uncertain-lookup", "exec"), namespace)
                if path == LANGGRAPH_CHAPTER:
                    action = {
                        "tenant_id": "tenant-7",
                        "business_action_id": "send-42",
                        "recipient_id": "user-9",
                        "body": "notice",
                    }
                    function_name = "execute_node"
                else:
                    action = {
                        "tenant_id": "tenant-7",
                        "kind": "send_notification",
                        "business_action_id": "send-42",
                        "business_object_id": "user-9",
                        "arguments": {"body": "notice"},
                    }
                    function_name = "execute_action_node"
                result = asyncio.run(
                    namespace[function_name](
                        {"decision": "approved", "approved": action}
                    )
                )
                self.assertEqual(
                    result,
                    {"executed": None, "execution_status": "unknown", "tool_result": None},
                )

    def test_langgraph_idempotency_uses_stable_business_action_identity(self):
        for path, _, reference_zone in self.langgraph_practice_zones():
            with self.subTest(path=path.name):
                key_block = next(
                    block
                    for block in python_fences(reference_zone)
                    if "def action_" in block and "sha256" in block
                )
                compile(key_block, f"{path.name}:idempotency", "exec")
                self.assertRegex(key_block, re.compile(r"business_(?:object|action)_id"))
                self.assertRegex(key_block, re.compile(r"normalized(?:_arguments)?\s*="))
                self.assertRegex(
                    reference_zone,
                    re.compile(r"业务标识.{0,100}规范化.{0,100}(?:参数|动作)", re.DOTALL),
                )
                self.assertRegex(
                    reference_zone,
                    re.compile(r"业务.*ID.{0,100}不(?:是|等于).*随机.*(?:调用|请求).*ID", re.DOTALL),
                )
                self.assertRegex(
                    reference_zone,
                    re.compile(r"task_id:tool_name.{0,100}(?:不足|冲突)", re.DOTALL),
                )

        chapter = LANGGRAPH_CHAPTER.read_text(encoding="utf-8")
        lab = END_TO_END_LAB.read_text(encoding="utf-8")
        self.assertRegex(chapter, re.compile(r"InMemorySaver.{0,100}(?:演示|demo)", re.IGNORECASE | re.DOTALL))
        self.assertRegex(chapter, re.compile(r"生产.{0,100}持久化|持久化.{0,100}生产", re.DOTALL))
        self.assertRegex(
            lab,
            re.compile(r"设计草图.{0,100}(?:没有|未).{0,80}(?:仓库源码|集成测试)", re.DOTALL),
        )
        self.assertNotRegex(lab, re.compile(r"(?:本项目|本仓库).{0,80}(?:已经|已)(?:实现|验证)"))
        self.assertRegex(lab, re.compile(r"审批.{0,36}不等于.{0,36}执行", re.DOTALL))

    def test_mcp_and_langgraph_sources_record_stable_primary_docs(self):
        text = REFERENCE_SOURCES.read_text(encoding="utf-8")
        urls = (
            "https://docs.langchain.com/oss/python/langgraph/interrupts",
            "https://docs.langchain.com/oss/python/langgraph/persistence",
            "https://docs.langchain.com/oss/python/langgraph/graph-api",
            "https://modelcontextprotocol.io/docs/learn/architecture",
            "https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle",
            "https://modelcontextprotocol.io/specification/2025-11-25/basic/transports",
            "https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization",
            "https://modelcontextprotocol.io/specification/2025-11-25/server/tools",
            "https://modelcontextprotocol.io/specification/2025-11-25/server/resources",
            "https://modelcontextprotocol.io/specification/2025-11-25/server/prompts",
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertIn(url, text)
        self.assertGreaterEqual(text.count("访问日期：2026-07-19"), 2)
        self.assertRegex(text, re.compile(r"MCP.*2025-11-25.*稳定", re.DOTALL))
        self.assertRegex(text, re.compile(r"实验.{0,80}明确标注", re.DOTALL))


if __name__ == "__main__":
    unittest.main()
