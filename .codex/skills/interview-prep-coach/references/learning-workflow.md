# Learning Workflow

## Focus Selection

Choose one study focus from `weaknesses.md` and `plan.md`. Prefer:
1. `P0` open weaknesses.
2. Weaknesses tied to current JD or target role.
3. Recent mock failures.
4. User-requested topics.

Search repo materials with `rg` before using external sources. Useful local areas include:
- `AI_Agent_System_Practical_Reference/`
- `interviews-docs/`
- `learning-materials/`
- `best-practice/`

## Study Session Shape

1. Name the weak spot and why it matters for interviews.
2. Teach the minimum concept needed to fix it.
3. Ask a short retrieval question or mini mock question.
4. Evaluate the user's answer.
5. Update the weakness status or next action.
6. Update the plan with the next mock or study step.

Keep sessions narrow. One weak spot per session is usually enough.

## Post-Interview Review

When the user provides real interview notes:
1. Extract company, role, round, date, questions, answer quality, and surprises if present.
2. Identify recurring weak spots and new gaps.
3. Merge them into `weaknesses.md` with evidence.
4. Update `plan.md` with immediate repair tasks and the next mock.
5. Log to `sessions/review/` if the user wants local records.

## Anki Handoff

Use Anki only for durable recall items: definitions, distinctions, commands, decision rules, and common pitfalls. Do not make Anki cards for broad skills like storytelling or system-design judgment unless they can be made atomic.

When useful, suggest invoking `anki-card-maker` with source material and card candidates. Do not add cards without explicit user approval.
