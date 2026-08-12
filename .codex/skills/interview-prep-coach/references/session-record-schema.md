# Completed Evidence Session Schema

`diagnostic`, `learn`, and `mock` sessions start as `in-progress`. To change one to
`completed`, append a record with every section and field below. `scripts/log-session` validates
this structure before it appends the entry or changes the status.

Use `not-applicable` only where the rubric permits it. Record one `Claim` block for every material
project statement so its source and truth category stay attached. A project-free answer records
one `not-applicable` block, making the absence of a project claim explicit. A completed record is
assessment evidence, but it never bypasses the user-confirmation gate for matrix, weakness, or
plan writes.

```markdown
## Questions and answers

- Question: <the tested question>
- Answer: <answer or concise faithful summary>

## Evidence excerpts

- "<verbatim answer excerpt supporting a score>"

## Evaluator

- Question type: <conceptual|coding|design|project|behavioral|other precise type>
- correctness: <0-4|not-applicable> - <reason grounded in evidence>
- completeness: <0-4|not-applicable> - <reason grounded in evidence>
- depth: <0-4|not-applicable> - <reason grounded in evidence>
- application: <0-4|not-applicable> - <reason grounded in evidence>
- tradeoffs: <0-4|not-applicable> - <reason grounded in evidence>
- project_truth: <0-4|not-applicable> - <reason grounded in evidence>
- communication: <0-4|not-applicable> - <reason grounded in evidence>
- follow_up_resilience: <0-4|not-applicable> - <reason grounded in evidence>
- epistemic_safety: <0-4|not-applicable> - <reason grounded in evidence>
- Highest hint level: <0-4>
- Evidence state: <introduced|assisted|independent|transfer-passed|retained>
- Follow-up / transfer result: <result or not-run>
- Satisfied gate: <highest fully satisfied level gate or none>
- Applied caps: <all applied caps or none>
- Rubric version: interview-prep-v1
- Judge mode: <codex-native and model, when available>
- Assessment time: <ISO 8601 timestamp>
- Confidence: <low|medium|high>
- Next validation: <one concrete follow-up or retest>
- Errors: <specific errors or none>
- Omissions: <specific omissions or none>
- Communication issues: <specific issues or none>

## Critic

- Critic result: <pass|follow-up-required>

## Project evidence

- Claim: <material project claim or not-applicable>
  - Source snapshot: <local path or URL plus commit SHA, access date, or not-applicable>
  - Truth category: <implemented|planned|proposed|unknown|not-applicable>

## Proposed state changes

- Matrix: <exact proposed change or no change>
- Weaknesses: <exact proposed change or no change>
- Plan: <exact proposed change or no change>

## Approval

- Approval decision: <approved|rejected|partial>
```

If confidence is low or the Critic requires a follow-up, complete the session with no level
change by writing exactly `Matrix: no change`, and put the discriminating follow-up in
`Next validation`. The same rule applies when `epistemic_safety` is 0 or 1. For code, SQL, DSA,
or commands, include deterministic execution evidence in the answer or evidence excerpts;
unexecuted work must not be described as correct.

`review` sessions are synthesis records rather than direct capability evidence and do not require
this schema. They still default to `in-progress` and become immutable when explicitly marked
`completed` or `abandoned`.
