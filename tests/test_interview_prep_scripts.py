import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / ".codex" / "skills" / "interview-prep-coach" / "scripts"


class InterviewPrepScriptsTest(unittest.TestCase):
    def run_script(self, name, root, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / name), "--root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_init_creates_private_state_without_overwriting_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".local" / "interview-prep"
            state_dir.mkdir(parents=True)
            existing_goal = state_dir / "goal.md"
            existing_goal.write_text("keep my goal\n", encoding="utf-8")

            result = self.run_script("init-interview-prep", root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(existing_goal.read_text(encoding="utf-8"), "keep my goal\n")
            for relative in [
                "goal.md",
                "plan.md",
                "weaknesses.md",
                "resume.md",
                "projects.md",
                "jd.md",
            ]:
                self.assertTrue((state_dir / relative).exists(), relative)
            for relative in ["sessions/mock", "sessions/learn", "sessions/review"]:
                self.assertTrue((state_dir / relative).is_dir(), relative)
            self.assertIn("created", result.stdout.lower())
            self.assertIn("preserved", result.stdout.lower())

    def test_check_state_reports_missing_required_and_optional_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_script("check-state", root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required", result.stdout.lower())
            self.assertIn("goal.md", result.stdout)

    def test_check_state_accepts_initialized_state_and_mentions_optional_jd(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_result = self.run_script("init-interview-prep", root)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            (root / ".local" / "interview-prep" / "jd.md").unlink()

            result = self.run_script("check-state", root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ready", result.stdout.lower())
            self.assertIn("optional missing", result.stdout.lower())
            self.assertIn("jd.md", result.stdout)

    def test_log_session_creates_dated_session_file_and_appends_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_result = self.run_script("init-interview-prep", root)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            first = self.run_script(
                "log-session",
                root,
                "--type",
                "mock",
                "--title",
                "RAG drill",
                "--content",
                "Question: What failed?",
            )
            second = self.run_script(
                "log-session",
                root,
                "--type",
                "mock",
                "--title",
                "RAG drill",
                "--content",
                "Diagnosis: weak rerank answer",
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            session_path = Path(first.stdout.strip())
            self.assertEqual(session_path, Path(second.stdout.strip()))
            text = session_path.read_text(encoding="utf-8")
            self.assertIn("# RAG drill", text)
            self.assertIn("Question: What failed?", text)
            self.assertIn("Diagnosis: weak rerank answer", text)


if __name__ == "__main__":
    unittest.main()
