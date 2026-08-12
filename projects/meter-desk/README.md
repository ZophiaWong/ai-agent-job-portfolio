# MeterDesk Interview Evidence

Source: [ZophiaWong/meter-desk](https://github.com/ZophiaWong/meter-desk)

Verified snapshot: [`62aa4456b42a`](https://github.com/ZophiaWong/meter-desk/commit/62aa4456b42a8b8851a275950abec9f80fab833f) on `2026-07-18`.

At this snapshot, MeterDesk presents a billing-support workbench whose backend governs tool use,
resolution drafts, financial approvals, trace evidence, and offline evaluation. The labels below
describe only what the pinned source supports; they are not a production-readiness claim.

## Snapshot Claims

| Truth category | Claim | Evidence | Competency |
| --- | --- | --- | --- |
| `implemented` | The governed agent path persists trace categories, verifies a bounded plan, and creates a pending approval instead of directly executing a financial action. | [Agent-loop tests](https://github.com/ZophiaWong/meter-desk/blob/62aa4456b42a8b8851a275950abec9f80fab833f/apps/api/tests/test_m3_agent_loop.py) | C03, C04, C08 |
| `implemented` | Eval Lab runs deterministic outcome, planning, governance, evidence, policy, and approval-routing checks, with blocked gaps represented explicitly. | [Eval Lab tests](https://github.com/ZophiaWong/meter-desk/blob/62aa4456b42a8b8851a275950abec9f80fab833f/apps/api/tests/test_m4_eval_lab.py) | C06 |
| `implemented` | The documented local stack uses Next.js, FastAPI, and Postgres; external payment and support integrations remain mock or out of scope. | [Pinned README](https://github.com/ZophiaWong/meter-desk/blob/62aa4456b42a8b8851a275950abec9f80fab833f/README.md) | C07, C09 |
| `planned` | The Usage Spike governed runner remains a visible coverage gap rather than a completed scenario. | [Pinned README status](https://github.com/ZophiaWong/meter-desk/blob/62aa4456b42a8b8851a275950abec9f80fab833f/README.md) | C06, C10 |
| `unknown` | This source snapshot does not establish production deployment, production traffic, enterprise tenancy, or real payment integration. | [Pinned README exclusions](https://github.com/ZophiaWong/meter-desk/blob/62aa4456b42a8b8851a275950abec9f80fab833f/README.md) | C09, C10 |

Before each project mock, compare the moving repository with this snapshot and record the refreshed
URL, commit SHA, and access date in the session. Reclassify changed claims. Never present a planned
milestone, visible coverage gap, mock integration, or unverified production property as implemented.
