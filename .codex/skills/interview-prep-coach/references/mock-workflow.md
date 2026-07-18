# Mock Workflow

## Setup

Before asking questions:
1. Run or mentally apply `check-state`.
2. Read `goal.md`, `plan.md`, `weaknesses.md`, `competency-matrix.md`, and only the relevant
   resume, project, story, prior-session, or optional JD context.
3. Pick one interview lane: concept, project deep dive, system design, coding/SQL, or behavioral/project communication.
4. State the lane and ask the first question only.
5. Map the session to one primary competency from `competency-model.md`.

## Interview Loop

For each question:
1. Ask a realistic interviewer question.
2. Wait for the user's answer.
3. Ask one follow-up if the answer is vague, incomplete, or misses a production tradeoff.
4. Do not hint, correct, or teach until the answer and follow-up are complete.
5. Score with `assessment-rubric.md` after the follow-up, then give feedback.

Do not reveal a model answer before the user answers.

For project questions, verify claims against available MeterDesk or Forge Harness sources, record
the local path or URL and commit SHA (or access date when no SHA is available), and label behavior
as implemented, planned, proposed, or unknown. Never promote a plan into a claim.

## Diagnosis Output

At session end, produce:
- session summary
- score by applicable rubric dimension with answer excerpts
- weaknesses to add or update
- competency matrix changes or a reason to leave the level unchanged
- plan updates
- next mock topic
- optional Anki candidates for durable facts

Run the Critic pass, present all proposed writes together, and wait for confirmation. Do not write
state merely because the mock ended.
