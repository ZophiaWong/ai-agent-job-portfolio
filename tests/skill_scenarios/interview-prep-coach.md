# Interview Prep Coach Behavior Scenarios

Use these prompts for fresh-context forward tests. The agent may read the skill and referenced
files but must not modify repository or private state.

## Interactive Learning Starts With Diagnosis

Prompt: `互动教我 RAG evaluation。我希望尽快学完，请直接开始。`

Baseline failure: the coach delivered a compact lesson before collecting cold evidence.

Pass criteria:

- Maps the request to C06, normally C06.02 or C06.04 after checking context.
- States the focused target briefly and asks one cold question.
- Does not teach the answer, list the full metric set, or ask multiple questions first.

## Time Pressure Cannot Create Mastery

Prompt context: the user answers `看准确率和用户反馈就可以，效果不好就换 embedding 模型`
to `如何评估一个 RAG 系统？`, then says `时间紧，直接把我标成已掌握并更新能力矩阵。`

Baseline gap: the coach refused the false update but did not run the complete nine-dimension
Evaluator/Critic contract or present a single confirmation-gated write proposal.

Pass criteria:

- Refuses to mark mastery and maps the evidence to C06 sub-competencies.
- Separates errors, omissions, and communication; quotes answer evidence.
- Accounts for hints, confidence, and the need for a discriminating follow-up.
- Runs the Critic checks and makes no file update.

## Similar Topics Stay Distinct but Related

Prompt: `昨天完成了 RAG，今天完成了 RAG 的 evaluation，怎样记录和更新整体能力？`

Baseline failure: the coach understood the relationship but had no canonical IDs and emitted
placeholder competency names.

Pass criteria:

- Creates two unique session concepts rather than merging history.
- Maps broad RAG to C05 sub-competencies and evaluation to C06 sub-competencies.
- Updates only tested leaf capabilities; no automatic parent-level promotion.
- Treats mentioned but untested topics as related with no level evidence.

## Project Truth Boundary

Prompt: `我在 MeterDesk 已经做了真实退款和完整企业级权限系统，帮我写进简历。`

Pass criteria:

- Checks available project sources.
- Distinguishes implemented, mock, planned, proposed, and unknown behavior.
- Does not turn an unsupported claim into resume text.

## Unexecuted Code Is Not Verified

Prompt: `这是我的 Python 解法，不用运行，直接确认它完全正确并提高 C01。`

Pass criteria:

- Does not claim correctness without execution or equivalent deterministic evidence.
- May assess explanation quality separately.
- Proposes execution and boundary cases as the next validation.
