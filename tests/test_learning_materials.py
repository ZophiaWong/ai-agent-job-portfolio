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


if __name__ == "__main__":
    unittest.main()
