# Mock Workflow

## Setup

Before asking questions:
1. Run or mentally apply `check-state`.
2. Read `goal.md`, `plan.md`, `weaknesses.md`, `resume.md`, `projects.md`, and optional `jd.md`.
3. Pick one interview lane: concept, project deep dive, system design, coding/SQL, or behavioral/project communication.
4. State the lane and ask the first question only.

## Interview Loop

For each question:
1. Ask a realistic interviewer question.
2. Wait for the user's answer.
3. Ask one follow-up if the answer is vague, incomplete, or misses a production tradeoff.
4. Score after the follow-up, not before.
5. Give concise feedback: strengths, gaps, better answer structure, and next action.

Do not reveal a model answer before the user answers.

## Scoring Rubric

Use 1-5:
- `1`: cannot answer or gives incorrect core concept.
- `2`: knows terms but lacks mechanism, tradeoff, or example.
- `3`: acceptable baseline answer with missing depth or structure.
- `4`: strong answer with concrete engineering detail.
- `5`: interview-ready answer with tradeoffs, production risks, and project relevance.

Evaluate dimensions:
- correctness
- structure
- depth
- production realism
- project/JD relevance
- communication clarity

## Diagnosis Output

At session end, produce:
- session summary
- score by question
- weaknesses to add or update
- plan updates
- next mock topic
- optional Anki candidates for durable facts

If writing files, update `weaknesses.md` and `plan.md` conservatively and log a session summary with `scripts/log-session`.
