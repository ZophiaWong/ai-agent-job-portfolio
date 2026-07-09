---
name: interview-prep-coach
description: Use when the user wants mock interview practice, interview-focused learning, weakness tracking, local study planning, or post-interview review for AI Agent, Python backend, RAG, SQL, TypeScript, Python, or DSA interview preparation.
---

# Interview Prep Coach

Run a mock-driven learning loop for technical interview preparation. Keep personal state local, use repo materials for focused study, and update goals, plans, and weaknesses from concrete evidence.

## Quick Start

1. Run `scripts/init-interview-prep --root <repo>` when private state is missing.
2. Run `scripts/check-state --root <repo>` before mock, learn, or review workflows.
3. Read `.local/interview-prep/goal.md`, `plan.md`, `weaknesses.md`, `resume.md`, `projects.md`, and optional `jd.md`.
4. Select the workflow:
   - `mock`: interview the user one question at a time.
   - `learn`: teach and test one focused weak spot.
   - `review`: process real interview notes.
5. Use `scripts/log-session` to record session summaries when the user wants local logging.

## Privacy Boundary

Treat `.local/interview-prep/` as private user state. Do not quote or commit it. Ask before revealing sensitive resume, company, JD, or real-interview details in final answers.

Public skill instructions, templates, and scripts live in this skill folder. Personal state lives under `.local/interview-prep/` and should be ignored by git.

## Workflows

Read only the reference needed for the current request:

- For local file shape, required fields, and update rules, read `references/file-contracts.md`.
- For mock interviews, scoring, and diagnosis, read `references/mock-workflow.md`.
- For focused study, plan updates, post-interview review, and Anki handoff, read `references/learning-workflow.md`.

## Core Rules

- Ask one interview question at a time in mock mode. Do not reveal the model answer before the user answers.
- Diagnose from evidence in the user's answer, not from vibes.
- Update or propose updates to `weaknesses.md` and `plan.md` after mock/review sessions.
- Prefer existing repo material before external sources. Search local files with `rg` first.
- Keep v1 scheduling simple: severity, recency, target role relevance, and user feedback. Do not use FSRS.
- Use the existing `anki-card-maker` skill only when the user asks to turn durable facts into Anki cards or approves the handoff.
