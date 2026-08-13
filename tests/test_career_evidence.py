import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE = REPO_ROOT / "scripts" / "validate-career-evidence"
MATCH = REPO_ROOT / "scripts" / "match-job"
METERDESK_ROOT = Path("/home/poter/resume-pj/meter-desk")
FORGE_ROOT = Path("/home/poter/resume-pj/forge-harness")


def run_script(script, *args):
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class CareerEvidenceScriptsTest(unittest.TestCase):
    def test_validate_career_evidence_accepts_fixed_project_commits(self):
        result = run_script(
            VALIDATE,
            "--root",
            str(REPO_ROOT),
            "--project-root",
            f"meterdesk={METERDESK_ROOT}",
            "--project-root",
            f"forge-harness={FORGE_ROOT}",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("career evidence valid", result.stdout.lower())

    def test_validate_reports_broken_foreign_evidence_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "reference" / "career-evidence").mkdir(parents=True)
            for name, content in {
                "capabilities.csv": "capability_id,name_zh,name_en,category,definition,scope,aliases\nCAP-X,X,X,agent,definition,scope,x\n",
                "claims.csv": "claim_id,project,capability_id,evidence_level,fact_zh,fact_en,limitations,forbidden,commit_sha,last_verified_at\nCL-X,meterdesk,CAP-X,verified_direct,事实,fact,限制,禁止,deadbeef,2026-08-13\n",
                "evidence.csv": "evidence_id,claim_id,evidence_type,repository,commit_sha,path,locator,verification_command,expected_observation,public_url\nEV-X,CL-X,implementation,meterdesk,deadbeef,missing.py,,true,works,\n",
                "bullets.csv": "bullet_id,project,role_track,language,claim_ids,min_evidence_level,display_order,text,review_required,demo_evidence_ids\nB-X,meterdesk,applied-agent,zh,CL-X,verified_direct,1,事实,false,EV-X\n",
            }.items():
                (root / "reference" / "career-evidence" / name).write_text(content, encoding="utf-8")
            result = run_script(VALIDATE, "--root", str(root), "--project-root", f"meterdesk={METERDESK_ROOT}")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing", (result.stdout + result.stderr).lower())

    def test_match_rejects_unconfirmed_requirements(self):
        input_payload = {
            "schema_version": 1,
            "job_id": "job-1",
            "role_track": "applied-agent",
            "requirements_confirmed": False,
            "requirements": [],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "job.json"
            output_path = Path(temp_dir) / "result.json"
            input_path.write_text(json.dumps(input_payload), encoding="utf-8")
            result = run_script(MATCH, "--root", str(REPO_ROOT), "--input", str(input_path), "--output", str(output_path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confirmed", (result.stdout + result.stderr).lower())

    def test_match_marks_rag_must_as_hard_gap_and_keeps_output_deterministic(self):
        input_payload = {
            "schema_version": 1,
            "job_id": "job-rag",
            "role_track": "applied-agent",
            "requirements_confirmed": True,
            "requirements": [
                {
                    "requirement_id": "REQ-RAG",
                    "capability_id": "CAP-RAG",
                    "importance": "must",
                    "source_quote": "负责 RAG 检索链路",
                    "unmapped_label": None,
                },
                {
                    "requirement_id": "REQ-TOOL",
                    "capability_id": "CAP-TOOL-GOVERNANCE",
                    "importance": "nice",
                    "source_quote": "熟悉工具权限治理",
                    "unmapped_label": None,
                },
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "job.json"
            output_a = Path(temp_dir) / "result-a.json"
            output_b = Path(temp_dir) / "result-b.json"
            input_path.write_text(json.dumps(input_payload, ensure_ascii=False), encoding="utf-8")
            args = ["--root", str(REPO_ROOT), "--input", str(input_path)]
            first = run_script(MATCH, *args, "--output", str(output_a))
            second = run_script(MATCH, *args, "--output", str(output_b))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            result_a = json.loads(output_a.read_text(encoding="utf-8"))
            result_b = json.loads(output_b.read_text(encoding="utf-8"))
            self.assertEqual(result_a, result_b)
            self.assertIn("REQ-RAG", result_a["hard_gaps"])
            self.assertNotIn("REQ-TOOL", result_a["hard_gaps"])
            self.assertIn("evidence", result_a)
            self.assertIn("bullets", result_a)

    def test_match_rejects_unmapped_requirement_as_formal_match_input(self):
        input_payload = {
            "schema_version": 1,
            "job_id": "job-new",
            "role_track": "runtime",
            "requirements_confirmed": True,
            "requirements": [
                {
                    "requirement_id": "REQ-NEW",
                    "capability_id": None,
                    "importance": "must",
                    "source_quote": "需要量子记忆图谱",
                    "unmapped_label": "量子记忆图谱",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "job.json"
            output_path = Path(temp_dir) / "result.json"
            input_path.write_text(json.dumps(input_payload, ensure_ascii=False), encoding="utf-8")
            result = run_script(MATCH, "--root", str(REPO_ROOT), "--input", str(input_path), "--output", str(output_path))
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertIn("REQ-NEW", output["unmapped"])
            self.assertEqual(output["hard_gaps"], [])

    def test_validator_rejects_duplicate_ids_and_invalid_enum(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            evidence_root = root / "reference" / "career-evidence"
            evidence_root.mkdir(parents=True)
            (evidence_root / "capabilities.csv").write_text(
                "capability_id,name_zh,name_en,category,definition,scope,aliases\n"
                "CAP-X,X,X,agent,definition,scope,x\n"
                "CAP-X,X2,X2,agent,definition,scope,x2\n",
                encoding="utf-8",
            )
            (evidence_root / "claims.csv").write_text(
                "claim_id,project,capability_id,evidence_level,fact_zh,fact_en,limitations,forbidden,commit_sha,last_verified_at\n"
                "CL-X,meterdesk,CAP-X,not-a-level,事实,fact,限制,禁止,f9dee13,2026-08-13\n",
                encoding="utf-8",
            )
            (evidence_root / "evidence.csv").write_text(
                "evidence_id,claim_id,evidence_type,repository,commit_sha,path,locator,verification_command,expected_observation,public_url\n",
                encoding="utf-8",
            )
            (evidence_root / "bullets.csv").write_text(
                "bullet_id,project,role_track,language,claim_ids,min_evidence_level,display_order,text,review_required,demo_evidence_ids\n",
                encoding="utf-8",
            )
            result = run_script(VALIDATE, "--root", str(root))
            self.assertNotEqual(result.returncode, 0)
            output = (result.stdout + result.stderr).lower()
            self.assertIn("duplicate", output)
            self.assertIn("invalid evidence level", output)

    def test_validator_rejects_false_verified_direct_and_broken_bullet_dependency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            evidence_root = root / "reference" / "career-evidence"
            evidence_root.mkdir(parents=True)
            (evidence_root / "capabilities.csv").write_text(
                "capability_id,name_zh,name_en,category,definition,scope,aliases\nCAP-X,X,X,agent,definition,scope,x\n",
                encoding="utf-8",
            )
            (evidence_root / "claims.csv").write_text(
                "claim_id,project,capability_id,evidence_level,fact_zh,fact_en,limitations,forbidden,commit_sha,last_verified_at\n"
                "CL-X,meterdesk,CAP-X,verified_direct,事实,fact,限制,禁止,f9dee13,2026-08-13\n",
                encoding="utf-8",
            )
            (evidence_root / "evidence.csv").write_text(
                "evidence_id,claim_id,evidence_type,repository,commit_sha,path,locator,verification_command,expected_observation,public_url\n"
                "EV-X,CL-X,implementation,meterdesk,f9dee13,README.md,,git show,works,\n",
                encoding="utf-8",
            )
            (evidence_root / "bullets.csv").write_text(
                "bullet_id,project,role_track,language,claim_ids,min_evidence_level,display_order,text,review_required,demo_evidence_ids\n"
                "B-X,meterdesk,applied-agent,zh,CL-MISSING,verified_direct,1,事实,false,EV-MISSING\n",
                encoding="utf-8",
            )
            result = run_script(VALIDATE, "--root", str(root), "--project-root", f"meterdesk={METERDESK_ROOT}")
            self.assertNotEqual(result.returncode, 0)
            output = (result.stdout + result.stderr).lower()
            self.assertIn("verified_direct claim", output)
            self.assertIn("missing claim", output)
            self.assertIn("missing demo evidence", output)


if __name__ == "__main__":
    unittest.main()
