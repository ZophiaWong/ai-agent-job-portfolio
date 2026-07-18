# Assessment Rubric

Use Codex-native evaluation in v1. Do not call an external judge API. Treat the result as
auditable evidence, not an objective truth.

## Scale

Score each applicable dimension from 0 to 4:

- `0`: absent, unusable, or fundamentally wrong.
- `1`: fragments or terminology without a correct mechanism.
- `2`: basically correct but missing important parts or application.
- `3`: independently usable in a normal interview or engineering task.
- `4`: deep, evidence-backed, and able to defend tradeoffs under follow-up.

## Dimensions

1. `correctness`: technical claims and causal reasoning.
2. `completeness`: required parts of the question.
3. `depth`: mechanisms, boundaries, and failure modes.
4. `application`: code, design, diagnosis, or concrete scenario use.
5. `tradeoffs`: alternatives, costs, and decision criteria.
6. `project_truth`: consistency with actual MeterDesk or Forge Harness evidence.
7. `communication`: conclusion-first structure and precise language.
8. `follow_up_resilience`: consistency when constraints change.
9. `epistemic_safety`: calibrated claims grounded in available evidence, without hallucination,
   evasion, buzzword substitution, or unjustified certainty. Higher is better.

Use `not-applicable` rather than inventing a score for an irrelevant dimension.

## Deterministic Evidence First

For Python, SQL, DSA, commands, or other executable work, prioritize test output, runtime
behavior, complexity, and boundary cases. Never claim code is correct when it was not executed.
Use the LLM rubric only for explanation, design judgment, and communication around the result.

## Evaluator Output

Produce:

- competency and question type;
- dimension scores with one-line reasons;
- verbatim answer excerpts supporting strengths and problems;
- errors, omissions, and communication issues as separate lists;
- highest hint level and evidence state;
- follow-up or transfer result;
- confidence: `low`, `medium`, or `high`;
- recommended next validation;
- proposed matrix, weakness, and plan changes.

Do not punish a valid alternative merely because it differs from a reference answer.

## Candidate-Level Decision Rules

Do not convert an average dimension score directly into a competency level. Apply these gates in
order and choose the highest fully satisfied level:

1. Level 1: the response contains at least one correct relevant claim (`correctness >= 1`) and
   `epistemic_safety >= 1`.
2. Level 2: an unassisted explanation or example has `correctness >= 2` and
   `completeness >= 2`, with `epistemic_safety >= 2`.
3. Level 3: an independently executed or worked application has `correctness >= 3` and
   `application >= 3`, passes applicable deterministic checks, and has `epistemic_safety >= 3`.
4. Level 4: transfer or retained evidence additionally has `depth >= 3`, `tradeoffs >= 3`, and
   `follow_up_resilience >= 3`; at least one of those is 4, `epistemic_safety >= 3`, and
   `project_truth >= 3` when relevant.

Apply these caps after the gates:

- `introduced` evidence cannot raise a candidate level. Assisted evidence may identify a gap or
  create a `watch`, but cannot confirm a higher level.
- Unexecuted code, SQL, or DSA cannot establish above level 2.
- Low confidence, Critic conflict, or `epistemic_safety <= 1` produces a
  follow-up, not a level change.
- Leave a parent `unassessed` while any listed child is unassessed. Once every child has a
  confirmed level, set the parent to the minimum child level; one strong leaf changes only itself.

Assign confidence consistently:

- `low`: any material conflict remains, the answer was assisted, an applicable deterministic
  check is missing, or project truth cannot be sourced.
- `medium`: at least one unassisted observation supports the gate and no material conflict remains,
  but independent transfer or retained evidence is absent.
- `high`: at least two independent observations include transfer or retained evidence, applicable
  deterministic checks pass, sources are recorded, and the Critic finds no material conflict.

Report the satisfied gate and every applied cap. Confirmation still governs any state write.

## Critic Pass

Before proposing a state change, check:

1. Does every score cite observable answer evidence?
2. Did the evaluator confuse an omission with an incorrect claim?
3. Did it confuse communication quality with technical knowledge?
4. Is another technically valid approach being rejected?
5. Did hints inflate the proposed level?
6. Does project assessment distinguish implemented, planned, proposed, and unknown behavior?
7. Is confidence justified by enough evidence?

If the Critic finds a material conflict or confidence is low, do not change the confirmed level.
Ask one discriminating follow-up or schedule a retest.

## State-Change Gates

- Never update state from reading completion or self-rating alone.
- A completed session may propose, but not apply, a change before user confirmation.
- One strong answer may create a candidate level or `watch`; a later independent/transfer check
  confirms mastery.
- One weak answer does not automatically lower a stable level. Repeated or strong contrary
  evidence marks it `unstable` and triggers a retest.
- Close a weakness only after later independent evidence demonstrates improvement.
- Record `rubric_version: interview-prep-v1`, judge mode/model when available, assessment time,
  and confidence. A future rubric version does not rewrite old evidence.
