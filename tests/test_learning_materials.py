import re
import unittest
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


if __name__ == "__main__":
    unittest.main()
