import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "interviews-docs" / "README.md",
    REPO_ROOT / "interviews-docs" / "01-AI" / "README.md",
    REPO_ROOT / "interviews-docs" / "02-后端" / "README.md",
    REPO_ROOT / "interviews-docs" / "03-DS_AL" / "README.md",
    REPO_ROOT / "projects" / "README.md",
    REPO_ROOT / "interviews-docs" / "04-career" / "README.md",
    REPO_ROOT / "best-practice" / "README.md",
    REPO_ROOT
    / "AI_Agent_System_Practical_Reference"
    / "00_README_学习路线与资料使用说明.md",
]
PROJECT_EVIDENCE_PAGES = [
    REPO_ROOT / "projects" / "meter-desk" / "README.md",
    REPO_ROOT / "projects" / "forge-harness" / "README.md",
]
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
PUBLIC_MARKDOWN_ROOTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "AI_Agent_System_Practical_Reference",
    REPO_ROOT / "interviews-docs",
    REPO_ROOT / "learning-materials",
    REPO_ROOT / "best-practice",
    REPO_ROOT / "projects",
    REPO_ROOT / ".codex" / "skills" / "anki-card-maker" / "references",
]
TASK_ONE_NAVIGATION_PAGES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "interviews-docs" / "README.md",
    REPO_ROOT / "interviews-docs" / "01-AI" / "README.md",
    REPO_ROOT / "interviews-docs" / "02-后端" / "README.md",
    REPO_ROOT / "interviews-docs" / "04-career" / "README.md",
    REPO_ROOT / "best-practice" / "README.md",
    REPO_ROOT
    / "AI_Agent_System_Practical_Reference"
    / "00_README_学习路线与资料使用说明.md",
]


class RepositoryNavigationTest(unittest.TestCase):
    def test_public_entrypoints_exist(self):
        for entrypoint in ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint.relative_to(REPO_ROOT)):
                self.assertTrue(entrypoint.is_file(), f"missing {entrypoint}")

    def test_public_markdown_local_links_and_images_resolve(self):
        public_pages = []
        for root in PUBLIC_MARKDOWN_ROOTS:
            if root.is_file():
                public_pages.append(root)
            else:
                public_pages.extend(root.rglob("*.md"))

        for page in public_pages:
            text = page.read_text(encoding="utf-8")
            for target in LINK_RE.findall(text):
                target = target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean_target = target.split("#", 1)[0].split(" ", 1)[0]
                if not clean_target:
                    continue
                resolved = (
                    REPO_ROOT / clean_target.lstrip("/")
                    if clean_target.startswith("/")
                    else page.parent / clean_target
                ).resolve()
                with self.subTest(page=page.relative_to(REPO_ROOT), target=target):
                    self.assertTrue(resolved.exists(), f"broken link in {page}: {target}")

    def test_task_one_navigation_local_targets_are_tracked(self):
        indexed_paths = set(
            subprocess.run(
                ["git", "ls-files", "--cached", "-z"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
            )
            .stdout.decode()
            .split("\0")
        )

        for page in TASK_ONE_NAVIGATION_PAGES:
            text = page.read_text(encoding="utf-8")
            for target in LINK_RE.findall(text):
                target = target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean_target = target.split("#", 1)[0].split(" ", 1)[0]
                if not clean_target:
                    continue
                resolved = (
                    REPO_ROOT / clean_target.lstrip("/")
                    if clean_target.startswith("/")
                    else page.parent / clean_target
                ).resolve()
                with self.subTest(page=page.relative_to(REPO_ROOT), target=target):
                    self.assertIn(
                        resolved.relative_to(REPO_ROOT).as_posix(),
                        indexed_paths,
                        f"untracked navigation target in {page}: {target}",
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

    def test_project_evidence_pages_pin_and_classify_snapshot_claims(self):
        snapshot_pattern = re.compile(
            r"Verified snapshot: \[`([0-9a-f]{7,12})`\]"
            r"\(https://github\.com/[^/]+/[^/]+/commit/([0-9a-f]{40})\) "
            r"on `\d{4}-\d{2}-\d{2}`"
        )
        claim_pattern = re.compile(
            r"^\| `(implemented|planned|proposed|unknown)` \| .+ \| .+ \| .+ \|$",
            flags=re.MULTILINE,
        )

        for page in PROJECT_EVIDENCE_PAGES:
            with self.subTest(page=page.relative_to(REPO_ROOT)):
                text = page.read_text(encoding="utf-8")
                snapshot = snapshot_pattern.search(text)
                self.assertIsNotNone(snapshot, "missing immutable verified snapshot")
                short_sha, full_sha = snapshot.groups()
                self.assertTrue(full_sha.startswith(short_sha))
                permalinks = re.findall(r"/blob/([0-9a-f]{40})/", text)
                self.assertGreaterEqual(len(permalinks), 2)
                self.assertEqual(set(permalinks), {full_sha})
                self.assertIn(
                    "| Truth category | Claim | Evidence | Competency |", text
                )
                claims = claim_pattern.findall(text)
                self.assertGreaterEqual(len(claims), 3)
                self.assertIn("implemented", claims)
                self.assertTrue({"planned", "proposed", "unknown"} & set(claims))


if __name__ == "__main__":
    unittest.main()
