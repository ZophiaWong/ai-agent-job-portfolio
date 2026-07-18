# File Contracts

## Private State Root

Default path: `.local/interview-prep/`.

Required files:
- `goal.md`: target role, timeline, target companies or JD focus, in-scope topics, current focus.
- `plan.md`: current priorities, next mock topics, learning tasks, recently completed tasks.
- `weaknesses.md`: evidence-backed weakness ledger.
- `resume.md`: private resume/profile notes used to personalize mock questions.
- `projects.md`: private project inventory used for project and system-design follow-ups.
- `competency-matrix.md`: current and target levels with confidence and session evidence.
- `daily.md`: today's time blocks, evidence targets, and completion state.
- `introduction.md`: private 60-second and 2-minute self-introductions.
- `stories.md`: private behavioral story bank.

Optional file:
- `jd.md`: pasted JD or company-specific requirements.

Required directories:
- `sessions/diagnostic/`
- `sessions/mock/`
- `sessions/learn/`
- `sessions/review/`

## Competency Matrix

Use these columns:

`Competency ID | Current | Target | Status | Confidence | Evidence | Next Validation`

- IDs must exist in `competency-model.md`; do not invent a synonym ID.
- Current levels use 0-4. Target levels come from the generic model or an explicit JD overlay.
- Status values: `unassessed`, `learning`, `needs-practice`, `watch`, `stable`, `unstable`.
- Confidence values: `low`, `medium`, `high`.
- Every confirmed level change links to a completed session ID.
- Keep conflicting evidence and use `unstable`; do not average scores.

## Session Records

Use one unique file per task. Required metadata:

- Session ID, type, status, start time, and primary competency.
- `covered_topics` for taught/tested topics and `related_topics` for untested context.
- Questions, answers or concise excerpts, highest hint level, and evidence state.
- Evaluator output, Critic result, confidence, and next validation.
- For project claims, a source snapshot: local path or URL plus commit SHA when available,
  otherwise an access date; classify each claim as implemented, planned, proposed, or unknown.
- Proposed state changes and the user's approval decision.

Status values: `in-progress`, `completed`, `abandoned`. Only `completed` may propose matrix or
weakness changes. An abandoned session is not level evidence. Resume an in-progress record with
`scripts/log-session --session-id <id> --status <status>`. Completed and abandoned records are
immutable; later work starts a new session and may link the earlier session ID.

## Weakness Ledger

Use a Markdown table with these columns:

`ID | Area | Severity | Evidence | Next Action | Status | Last Updated`

Severity values:
- `P0`: blocks credible interview performance.
- `P1`: likely to cost signal in a target interview.
- `P2`: improvement item or polish.

Status values:
- `open`
- `in-progress`
- `watch`
- `closed`

Update rules:
- Add or update a weakness only when there is concrete evidence from mock, learn, review, or user feedback.
- Keep evidence short and specific.
- Make next action executable in one study session.
- Do not close a weakness unless the user demonstrates improvement in a later mock or study check.
- Reuse an existing weakness when new evidence shows the same concrete gap.

## Plan File

Keep `plan.md` short and active. It should answer:
- What is the current focus?
- What weak spots drive the plan?
- What should the next mock test?
- What should the next study session cover?

Prioritize by severity first, then target role relevance, then recency, then explicit user feedback.

## Write Safety and Context Loading

- Show a single proposed update covering session, matrix, weakness, and plan changes.
- Apply only explicitly approved changes. On rejection, write nothing.
- Always read goal, active plan, open weaknesses, and the matrix summary.
- Read only the current topic's latest 3-5 evidence records and relevant project/JD files.
- Do not load all historical sessions by default.

## Privacy

Do not commit `.local/`. Do not copy personal details into public templates or skill docs.
