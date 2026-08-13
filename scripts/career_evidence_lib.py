#!/usr/bin/env python3
"""Shared, dependency-free helpers for career evidence validation and matching."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Iterable


EVIDENCE_DIR = Path("reference") / "career-evidence"
TABLES = {
    "capabilities": "capabilities.csv",
    "claims": "claims.csv",
    "evidence": "evidence.csv",
    "bullets": "bullets.csv",
}
EVIDENCE_LEVELS = ("verified_direct", "direct_implementation", "adjacent", "gap")
LEVEL_RANK = {level: len(EVIDENCE_LEVELS) - index for index, level in enumerate(EVIDENCE_LEVELS)}
IMPORTANCE = ("must", "nice")
ROLE_TRACKS = ("applied-agent", "runtime", "ai-backend", "ai-fullstack")
PROJECT_COMMITS = {"meterdesk": "f9dee13", "forge-harness": "a0146b2"}
PROJECT_ORDER = {
    "applied-agent": ("meterdesk", "forge-harness"),
    "runtime": ("forge-harness", "meterdesk"),
    "ai-backend": ("meterdesk", "forge-harness"),
    "ai-fullstack": ("meterdesk", "forge-harness"),
}
REQUIRED_COLUMNS = {
    "capabilities": ("capability_id", "name_zh", "name_en", "category", "definition", "scope", "aliases"),
    "claims": ("claim_id", "project", "capability_id", "evidence_level", "fact_zh", "fact_en", "limitations", "forbidden", "commit_sha", "last_verified_at"),
    "evidence": ("evidence_id", "claim_id", "evidence_type", "repository", "commit_sha", "path", "locator", "verification_command", "expected_observation", "public_url"),
    "bullets": ("bullet_id", "project", "role_track", "language", "claim_ids", "min_evidence_level", "display_order", "text", "review_required", "demo_evidence_ids"),
}


class EvidenceError(Exception):
    """Raised for a user-correctable evidence data or input error."""


def read_table(root: Path, table_name: str) -> list[dict[str, str]]:
    path = root / EVIDENCE_DIR / TABLES[table_name]
    if not path.is_file():
        raise EvidenceError(f"missing table: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        actual = tuple(reader.fieldnames or ())
        expected = REQUIRED_COLUMNS[table_name]
        if actual != expected:
            raise EvidenceError(f"invalid {table_name}.csv header: expected {expected}, got {actual}")
        return list(reader)


def unique_ids(rows: Iterable[dict[str, str]], column: str, label: str, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    for row in rows:
        value = row.get(column, "").strip()
        if not value:
            errors.append(f"{label} has empty {column}")
        elif value in ids:
            errors.append(f"duplicate {label} {column}: {value}")
        ids.add(value)
    return ids


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def git_has_path(project_root: Path, commit: str, path: str) -> bool:
    if not path:
        return False
    result = subprocess.run(
        ["git", "-C", str(project_root), "cat-file", "-e", f"{commit}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def git_has_commit(project_root: Path, commit: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(project_root), "cat-file", "-e", f"{commit}^{{commit}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def validate_tables(
    root: Path,
    project_roots: dict[str, Path],
    *,
    check_external_paths: bool = True,
) -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    tables = {name: read_table(root, name) for name in TABLES}
    errors: list[str] = []
    capability_ids = unique_ids(tables["capabilities"], "capability_id", "capability", errors)
    claim_ids = unique_ids(tables["claims"], "claim_id", "claim", errors)
    evidence_ids = unique_ids(tables["evidence"], "evidence_id", "evidence", errors)
    unique_ids(tables["bullets"], "bullet_id", "bullet", errors)

    for claim in tables["claims"]:
        project = claim["project"].strip()
        level = claim["evidence_level"].strip()
        if project not in PROJECT_COMMITS:
            errors.append(f"claim {claim['claim_id']} has invalid project: {project}")
        if claim["capability_id"] not in capability_ids:
            errors.append(f"claim {claim['claim_id']} references missing capability {claim['capability_id']}")
        if level not in EVIDENCE_LEVELS:
            errors.append(f"claim {claim['claim_id']} has invalid evidence level: {level}")
        expected_commit = PROJECT_COMMITS.get(project)
        if expected_commit and claim["commit_sha"] != expected_commit:
            errors.append(f"claim {claim['claim_id']} must use fixed commit {expected_commit}")

    evidence_by_claim: dict[str, list[dict[str, str]]] = {}
    for evidence in tables["evidence"]:
        evidence_by_claim.setdefault(evidence["claim_id"], []).append(evidence)
        if evidence["claim_id"] not in claim_ids:
            errors.append(f"evidence {evidence['evidence_id']} references missing claim {evidence['claim_id']}")
        project = evidence["repository"].strip()
        if project not in PROJECT_COMMITS:
            errors.append(f"evidence {evidence['evidence_id']} has invalid repository: {project}")
        expected_commit = PROJECT_COMMITS.get(project)
        if expected_commit and evidence["commit_sha"] != expected_commit:
            errors.append(f"evidence {evidence['evidence_id']} must use fixed commit {expected_commit}")
        if check_external_paths:
            project_root = project_roots.get(project)
            if project_root is None:
                errors.append(f"missing project root for {project} (evidence {evidence['evidence_id']})")
            elif not project_root.is_dir():
                errors.append(f"missing project root: {project_root}")
            elif expected_commit and not git_has_commit(project_root, expected_commit):
                errors.append(f"missing commit {expected_commit} in {project_root}")
            elif expected_commit and not git_has_path(project_root, expected_commit, evidence["path"]):
                errors.append(f"missing evidence path {project}:{expected_commit}:{evidence['path']}")

    for claim in tables["claims"]:
        evidence = evidence_by_claim.get(claim["claim_id"], [])
        kinds = {item["evidence_type"] for item in evidence}
        if claim["evidence_level"] == "verified_direct":
            has_build = bool(kinds & {"implementation", "spec"})
            has_verification = bool(kinds & {"test", "smoke", "report"})
            if not has_build or not has_verification:
                errors.append(f"verified_direct claim {claim['claim_id']} needs implementation/spec and test/smoke/report evidence")
        if claim["evidence_level"] == "gap" and "boundary" not in kinds:
            errors.append(f"gap claim {claim['claim_id']} needs boundary evidence")

    for bullet in tables["bullets"]:
        if bullet["project"] not in PROJECT_COMMITS:
            errors.append(f"bullet {bullet['bullet_id']} has invalid project {bullet['project']}")
        if bullet["role_track"] not in ROLE_TRACKS:
            errors.append(f"bullet {bullet['bullet_id']} has invalid role track {bullet['role_track']}")
        if bullet["language"] not in {"zh", "en"}:
            errors.append(f"bullet {bullet['bullet_id']} has invalid language {bullet['language']}")
        if bullet["min_evidence_level"] not in EVIDENCE_LEVELS:
            errors.append(f"bullet {bullet['bullet_id']} has invalid minimum evidence level {bullet['min_evidence_level']}")
        for claim_id in split_values(bullet["claim_ids"]):
            if claim_id not in claim_ids:
                errors.append(f"bullet {bullet['bullet_id']} references missing claim {claim_id}")
        for evidence_id in split_values(bullet["demo_evidence_ids"]):
            if evidence_id not in evidence_ids:
                errors.append(f"bullet {bullet['bullet_id']} references missing demo evidence {evidence_id}")
        if bullet["review_required"] not in {"true", "false"}:
            errors.append(f"bullet {bullet['bullet_id']} has invalid review_required value")

    return tables, errors


def table_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for name in TABLES.values():
        digest.update(name.encode("utf-8"))
        digest.update((root / EVIDENCE_DIR / name).read_bytes())
    return digest.hexdigest()


def best_claim(claims: list[dict[str, str]], project: str, capability_id: str) -> dict[str, str] | None:
    candidates = [claim for claim in claims if claim["project"] == project and claim["capability_id"] == capability_id]
    if not candidates:
        return None
    return sorted(candidates, key=lambda claim: (-LEVEL_RANK.get(claim["evidence_level"], 0), claim["claim_id"]))[0]


def bullet_is_usable(bullet: dict[str, str], claims_by_id: dict[str, dict[str, str]]) -> bool:
    required = LEVEL_RANK.get(bullet["min_evidence_level"], 0)
    return all(
        claim_id in claims_by_id and LEVEL_RANK.get(claims_by_id[claim_id]["evidence_level"], 0) >= required
        for claim_id in split_values(bullet["claim_ids"])
    )


def json_dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
