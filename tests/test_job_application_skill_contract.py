import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / ".codex" / "skills" / "job-application-tracker" / "SKILL.md"


class JobApplicationSkillContractTest(unittest.TestCase):
    def test_skill_exists_and_requires_confirmation_before_matching(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("requirements_confirmed", text)
        self.assertIn("不跳过 must / nice 确认", text)
        self.assertIn("match-job", text)
        self.assertIn("JD 原文", text)
        self.assertIn("重新 fetch", text)

    def test_skill_preserves_boundaries_and_regressed_eval(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("不把 RAG", text)
        self.assertIn("REGRESSED", text)
        self.assertIn("interview-prep-coach", text)
        self.assertIn("pending", text)


if __name__ == "__main__":
    unittest.main()
