import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / ".codex" / "skills" / "interview-prep-coach" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from state_utils import write_exclusive_with_suffix


class InterviewPrepScriptsTest(unittest.TestCase):
    def run_script(self, name, root, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / name), "--root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def run_executable(self, name, root, *args):
        return subprocess.run(
            [str(SCRIPTS_DIR / name), "--root", str(root), *args],
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
                "competency-matrix.md",
                "daily.md",
                "introduction.md",
                "stories.md",
            ]:
                self.assertTrue((state_dir / relative).exists(), relative)
            for relative in [
                "sessions/diagnostic",
                "sessions/mock",
                "sessions/learn",
                "sessions/review",
            ]:
                self.assertTrue((state_dir / relative).is_dir(), relative)
            self.assertIn("created", result.stdout.lower())
            self.assertIn("preserved", result.stdout.lower())

    def test_check_state_reports_missing_required_and_optional_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_script("check-state", root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required", result.stdout.lower())
            reported = {
                line.removeprefix("- ")
                for line in result.stdout.splitlines()
                if line.startswith("- ")
            }
            expected = {
                ".local/interview-prep/goal.md",
                ".local/interview-prep/plan.md",
                ".local/interview-prep/weaknesses.md",
                ".local/interview-prep/resume.md",
                ".local/interview-prep/projects.md",
                ".local/interview-prep/competency-matrix.md",
                ".local/interview-prep/daily.md",
                ".local/interview-prep/introduction.md",
                ".local/interview-prep/stories.md",
                ".local/interview-prep/sessions/diagnostic/",
                ".local/interview-prep/sessions/mock/",
                ".local/interview-prep/sessions/learn/",
                ".local/interview-prep/sessions/review/",
            }
            self.assertEqual(reported, expected)

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

    def test_log_session_creates_unique_structured_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_result = self.run_script("init-interview-prep", root)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            first = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG drill",
                "--status",
                "in-progress",
                "--primary-competency",
                "C05",
                "--covered-topic",
                "hybrid retrieval",
                "--related-topic",
                "RAG evaluation",
                "--content",
                "Question: What failed?",
            )
            second = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG drill",
                "--primary-competency",
                "C05",
                "--content",
                "Diagnosis: weak rerank answer",
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            session_path = Path(first.stdout.strip())
            second_path = Path(second.stdout.strip())
            self.assertNotEqual(session_path, second_path)
            text = session_path.read_text(encoding="utf-8")
            self.assertIn("# RAG drill", text)
            self.assertIn("- Type: learn", text)
            self.assertIn("- Status: in-progress", text)
            self.assertIn("- Primary competency: C05", text)
            self.assertIn('- Covered topics: ["hybrid retrieval"]', text)
            self.assertIn('- Related topics: ["RAG evaluation"]', text)
            self.assertIn("Question: What failed?", text)
            self.assertNotIn("Diagnosis: weak rerank answer", text)

    def test_log_session_resumes_existing_session_and_updates_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)

            first = self.run_script(
                "log-session",
                root,
                "--type",
                "diagnostic",
                "--title",
                "Agent baseline",
                "--status",
                "in-progress",
                "--primary-competency",
                "C03",
                "--content",
                "First answer",
            )
            session_path = Path(first.stdout.strip())
            resumed = self.run_script(
                "log-session",
                root,
                "--type",
                "diagnostic",
                "--session-id",
                session_path.stem,
                "--status",
                "completed",
                "--content",
                "Final assessment",
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            self.assertEqual(Path(resumed.stdout.strip()), session_path)
            text = session_path.read_text(encoding="utf-8")
            self.assertIn("- Status: completed", text)
            self.assertIn("First answer", text)
            self.assertIn("Final assessment", text)

    def test_log_session_resume_preserves_status_when_status_is_omitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            first = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG evaluation",
                "--status",
                "in-progress",
                "--primary-competency",
                "C06.02",
                "--content",
                "Cold answer",
            )
            session_path = Path(first.stdout.strip())

            resumed = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--session-id",
                session_path.stem,
                "--content",
                "More evidence",
            )

            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            text = session_path.read_text(encoding="utf-8")
            self.assertIn("- Status: in-progress", text)
            self.assertNotIn("- Status: completed", text)

    def test_log_session_resume_merges_and_deduplicates_topics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            first = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG evaluation",
                "--status",
                "in-progress",
                "--primary-competency",
                "C06.02",
                "--covered-topic",
                "retrieval metrics",
                "--content",
                "Cold answer",
            )
            session_path = Path(first.stdout.strip())

            resumed = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--session-id",
                session_path.stem,
                "--covered-topic",
                "retrieval metrics",
                "--covered-topic",
                "generation metrics",
                "--related-topic",
                "RAG failure diagnosis",
                "--related-topic",
                r"C:\path",
                "--content",
                "Applied answer",
            )

            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            text = session_path.read_text(encoding="utf-8")
            self.assertIn(
                '- Covered topics: ["retrieval metrics", "generation metrics"]', text
            )
            self.assertIn(
                '- Related topics: ["RAG failure diagnosis", "C:\\\\path"]', text
            )

    def test_log_session_keeps_terminal_sessions_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            completed = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG evaluation",
                "--primary-competency",
                "C06.02",
                "--content",
                "Final evidence",
            )
            session_path = Path(completed.stdout.strip())
            before = session_path.read_text(encoding="utf-8")

            reopened = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--session-id",
                session_path.stem,
                "--status",
                "in-progress",
                "--content",
                "Late mutation",
            )

            self.assertNotEqual(reopened.returncode, 0)
            self.assertIn("terminal", reopened.stderr.lower())
            self.assertEqual(session_path.read_text(encoding="utf-8"), before)

    def test_log_session_records_abandoned_interruption_as_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            started = self.run_script(
                "log-session",
                root,
                "--type",
                "diagnostic",
                "--title",
                "Agent state",
                "--status",
                "in-progress",
                "--primary-competency",
                "C03.02",
                "--content",
                "Cold answer",
            )
            session_path = Path(started.stdout.strip())

            abandoned = self.run_script(
                "log-session",
                root,
                "--type",
                "diagnostic",
                "--session-id",
                session_path.stem,
                "--status",
                "abandoned",
                "--content",
                "Stopped by user",
            )
            retried = self.run_script(
                "log-session",
                root,
                "--type",
                "diagnostic",
                "--session-id",
                session_path.stem,
                "--content",
                "Must not append",
            )

            self.assertEqual(abandoned.returncode, 0, abandoned.stderr)
            text = session_path.read_text(encoding="utf-8")
            self.assertIn("- Status: abandoned", text)
            self.assertIn("Stopped by user", text)
            self.assertNotEqual(retried.returncode, 0)
            self.assertNotIn("Must not append", session_path.read_text(encoding="utf-8"))

    def test_log_session_rejects_invalid_competency_and_metadata_newlines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)

            invalid_competency = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG",
                "--primary-competency",
                "C99",
                "--content",
                "Evidence",
            )
            injected_title = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG\n- Status: completed",
                "--content",
                "Evidence",
            )

            self.assertNotEqual(invalid_competency.returncode, 0)
            self.assertIn("competency", invalid_competency.stderr.lower())
            self.assertNotEqual(injected_title.returncode, 0)
            self.assertIn("newline", injected_title.stderr.lower())

    def test_log_session_requires_primary_competency_for_evidence_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)

            result = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG",
                "--content",
                "Evidence",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("primary-competency", result.stderr)

    def test_exclusive_session_creation_preserves_collision_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_dir = root / "sessions"
            session_dir.mkdir()
            existing = session_dir / "learn-fixed.md"
            existing.write_text("keep me\n", encoding="utf-8")

            path, session_id = write_exclusive_with_suffix(
                session_dir,
                "learn-fixed",
                lambda allocated_id: f"# {allocated_id}\n",
                root,
            )

            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me\n")
            self.assertEqual(session_id, "learn-fixed-2")
            self.assertEqual(path.name, "learn-fixed-2.md")
            self.assertEqual(path.read_text(encoding="utf-8"), "# learn-fixed-2\n")

    def test_state_scripts_reject_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(tmp)
            outside = Path(outside_tmp)
            (root / ".local").symlink_to(outside, target_is_directory=True)

            init_result = self.run_script("init-interview-prep", root)
            check_result = self.run_script("check-state", root)

            self.assertNotEqual(init_result.returncode, 0)
            self.assertIn("outside", init_result.stderr.lower())
            self.assertNotEqual(check_result.returncode, 0)
            self.assertIn("outside", check_result.stderr.lower())
            self.assertEqual(list(outside.iterdir()), [])

    def test_state_scripts_reject_symlink_redirection_inside_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".local").mkdir()
            state_link = root / ".local" / "interview-prep"
            state_link.symlink_to(root, target_is_directory=True)

            init_result = self.run_script("init-interview-prep", root)
            check_result = self.run_script("check-state", root)

            self.assertNotEqual(init_result.returncode, 0)
            self.assertIn("symlink", init_result.stderr.lower())
            self.assertNotEqual(check_result.returncode, 0)
            self.assertIn("symlink", check_result.stderr.lower())
            self.assertFalse((root / "goal.md").exists())

    def test_log_session_rejects_symlinked_session_directory(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(tmp)
            outside = Path(outside_tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            learn_dir = root / ".local" / "interview-prep" / "sessions" / "learn"
            learn_dir.rmdir()
            learn_dir.symlink_to(outside, target_is_directory=True)

            result = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG",
                "--primary-competency",
                "C05",
                "--content",
                "Evidence",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside", result.stderr.lower())
            self.assertEqual(list(outside.iterdir()), [])

    def test_log_session_rejects_cross_mode_symlink_inside_private_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_script("init-interview-prep", root).returncode, 0)
            sessions_dir = root / ".local" / "interview-prep" / "sessions"
            learn_dir = sessions_dir / "learn"
            learn_dir.rmdir()
            learn_dir.symlink_to(sessions_dir / "mock", target_is_directory=True)

            result = self.run_script(
                "log-session",
                root,
                "--type",
                "learn",
                "--title",
                "RAG",
                "--primary-competency",
                "C05",
                "--content",
                "Evidence",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.lower())
            self.assertEqual(list((sessions_dir / "mock").iterdir()), [])

    def test_scripts_are_directly_executable_and_forced_to_lf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calls = [
                ("init-interview-prep", []),
                ("check-state", []),
                (
                    "log-session",
                    ["--type", "review", "--title", "Direct run", "--content", "ok"],
                ),
            ]
            for name, args in calls:
                with self.subTest(script=name):
                    result = self.run_executable(name, root, *args)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    relative = f".codex/skills/interview-prep-coach/scripts/{name}"
                    attr = subprocess.run(
                        ["git", "check-attr", "eol", "--", relative],
                        cwd=REPO_ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    self.assertEqual(attr.returncode, 0, attr.stderr)
                    self.assertTrue(attr.stdout.rstrip().endswith(": lf"), attr.stdout)
                    self.assertNotIn(b"\r", (REPO_ROOT / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
