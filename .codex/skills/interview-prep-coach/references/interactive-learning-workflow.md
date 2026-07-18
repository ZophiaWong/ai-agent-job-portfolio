# Interactive Learning Workflow

Use this workflow for `learn`, delayed retest, and a focused diagnostic. The goal is
observable capability change, not content completion.

## Session State Machine

1. `SETUP`: Map the request to one primary competency and a target behavior; state the selected
   competency ID briefly before the first question.
2. `DIAGNOSE`: Ask one cold question before teaching. Do not reveal the answer.
3. `TEACH`: Explain only the smallest missing concept exposed by the answer.
4. `RETRIEVE`: Ask the user to restate, distinguish, or reconstruct it without notes.
5. `APPLY`: Use code, architecture, diagnosis, or a project scenario.
6. `TRANSFER`: Change the scenario or constraints and test the same capability again.
7. `ASSESS`: Apply `assessment-rubric.md`; account for hints.
8. `PROPOSE_UPDATE`: Show the session summary and exact proposed state changes.
9. `COMMIT_OR_DISCARD`: Write only after explicit confirmation.

Ask exactly one question per conversational turn. Do not pre-generate the whole lesson.

## Topic Mapping

- Select one `primary_competency` from `competency-model.md`.
- Record actually taught or tested knowledge as `covered_topics`.
- Record mentioned but untested knowledge as `related_topics`; it produces no level evidence.
- For a broad request such as `RAG`, inspect C05.01-C05.04 and C06.01-C06.03, then use
  the weakest relevant observable behavior as the primary target.
- When a tangent requires a different primary competency, add a future task instead of
  expanding the current session.

## Hint Ladder

| Level | Assistance |
| ---: | --- |
| 0 | No hint; independent answer. |
| 1 | Name the missing direction only. |
| 2 | Supply a relevant concept or constraint. |
| 3 | Supply the answer structure. |
| 4 | Show a reference answer, then require a fresh explanation. |

Record the highest hint used. A correct answer at levels 1-4 is assisted evidence and cannot
by itself establish independent mastery.

## Evidence States

- `introduced`: material was presented; no performance claim.
- `assisted`: completed with a hint.
- `independent`: completed without hints.
- `transfer-passed`: applied independently under changed constraints.
- `retained`: passed a later independent retest.

Do not apply automatic time decay. Time triggers a retest; observed performance changes a level.

## Similar and Repeated Topics

Create one unique session per learning task. A `RAG` session and a later `RAG evaluation`
session remain separate evidence. Update only the sub-competencies actually tested. Never raise
the whole RAG parent because one evaluation sub-topic improved.

Keep conflicting evidence. Prefer independent, transfer, delayed, project, and real-interview
evidence over assisted recall. Mark the competency `unstable` and schedule a targeted retest
instead of averaging conflicting scores.

## Interrupt and Resume

- Log an unfinished session as `in-progress`; resume it by session ID.
- Mark a deliberately stopped session `abandoned`.
- Treat `completed` and `abandoned` records as immutable; link a new session for later work.
- Only a `completed` session can propose matrix or weakness changes.
- An abandoned session may inform planning but is not level evidence.

## Source Selection

Search the repository before browsing. Use stable local material for principles. Verify current
framework, API, model, regulation, or product behavior against primary official sources and
record the source date/version. Surface source conflicts instead of silently choosing one.

## End-of-Session Contract

Show, in order:

1. Target competency and evidence state.
2. What the user demonstrated, with answer excerpts.
3. Errors, omissions, and communication issues separately.
4. Hint usage, transfer result, confidence, and next validation.
5. Proposed session log, matrix change, weakness change, and plan change.
6. One confirmation request covering all writes.

On rejection, write nothing. On partial approval, apply only the explicitly approved changes.
