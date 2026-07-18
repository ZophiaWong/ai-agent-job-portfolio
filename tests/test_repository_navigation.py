import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "projects" / "README.md",
    REPO_ROOT / "interviews-docs" / "04-career" / "README.md",
]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class RepositoryNavigationTest(unittest.TestCase):
    def test_public_entrypoints_exist_and_local_links_resolve(self):
        for entrypoint in ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint.relative_to(REPO_ROOT)):
                self.assertTrue(entrypoint.is_file(), f"missing {entrypoint}")
                text = entrypoint.read_text(encoding="utf-8")
                for target in LINK_RE.findall(text):
                    if target.startswith(("http://", "https://", "#")):
                        continue
                    clean_target = target.split("#", 1)[0]
                    if not clean_target:
                        continue
                    resolved = (entrypoint.parent / clean_target).resolve()
                    self.assertTrue(
                        resolved.exists(),
                        f"broken link in {entrypoint}: {target}",
                    )

    def test_competency_matrix_covers_every_public_competency_id(self):
        skill_root = REPO_ROOT / ".codex" / "skills" / "interview-prep-coach"
        model = (skill_root / "references" / "competency-model.md").read_text(
            encoding="utf-8"
        )
        matrix = (skill_root / "assets" / "templates" / "competency-matrix.md").read_text(
            encoding="utf-8"
        )
        competency_pattern = re.compile(r"\bC(?:0[1-9]|1[0-3])(?:\.\d{2})?\b")

        self.assertEqual(
            set(competency_pattern.findall(matrix)),
            set(competency_pattern.findall(model)),
        )

    def test_assessment_rubric_defines_all_nine_positive_dimensions(self):
        rubric = (
            REPO_ROOT
            / ".codex"
            / "skills"
            / "interview-prep-coach"
            / "references"
            / "assessment-rubric.md"
        ).read_text(encoding="utf-8")
        dimensions = {
            "correctness",
            "completeness",
            "depth",
            "application",
            "tradeoffs",
            "project_truth",
            "communication",
            "follow_up_resilience",
            "epistemic_safety",
        }

        for dimension in dimensions:
            self.assertIn(f"`{dimension}`", rubric)
        self.assertNotIn("`risk_signals`", rubric)


if __name__ == "__main__":
    unittest.main()
