# File Contracts

## Private State Root

Default path: `.local/interview-prep/`.

Required files:
- `goal.md`: target role, timeline, target companies or JD focus, in-scope topics, current focus.
- `plan.md`: current priorities, next mock topics, learning tasks, recently completed tasks.
- `weaknesses.md`: evidence-backed weakness ledger.
- `resume.md`: private resume/profile notes used to personalize mock questions.
- `projects.md`: private project inventory used for project and system-design follow-ups.

Optional file:
- `jd.md`: pasted JD or company-specific requirements.

Required directories:
- `sessions/mock/`
- `sessions/learn/`
- `sessions/review/`

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

## Plan File

Keep `plan.md` short and active. It should answer:
- What is the current focus?
- What weak spots drive the plan?
- What should the next mock test?
- What should the next study session cover?

Prioritize by severity first, then target role relevance, then recency, then explicit user feedback.

## Privacy

Do not commit `.local/`. Do not copy personal details into public templates or skill docs.
