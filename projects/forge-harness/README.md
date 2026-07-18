# Forge Harness Interview Evidence

Source: [ZophiaWong/forge-harness](https://github.com/ZophiaWong/forge-harness)

Verified snapshot: [`9c1b1dbb0566`](https://github.com/ZophiaWong/forge-harness/commit/9c1b1dbb0566e9053457db50e64cd374848de856) on `2026-07-18`.

At this snapshot, Forge Harness is a TypeScript tutorial project with runnable checkpoints through
async child sessions and isolated edit previews. The labels below separate tested mechanisms from
future tutorial scope and from production properties the repository does not establish.

## Snapshot Claims

| Truth category | Claim | Evidence | Competency |
| --- | --- | --- | --- |
| `implemented` | A registry and dispatcher expose built-in tools, reject unknown tools, and enforce the read boundary tested by the runtime suite. | [Tool runtime tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/tools/toolRuntime.test.ts) | C04, C11 |
| `implemented` | Deterministic verification can gate a final answer and drive one recovery attempt. | [Verification tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/runtime/verification.test.ts) | C03, C06 |
| `implemented` | Context projection and compaction have executable tests rather than documentation-only examples. | [Context projection tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/context/contextProjection.test.ts) and [compaction tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/context/compaction.test.ts) | C03, C11 |
| `implemented` | Async child sessions track pending work, return terminal notifications once, and expose isolated edit-preview metadata. | [Child-session tests](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/test/extensions/childSessions.test.ts) | C03, C08, C11 |
| `proposed` | External tool and MCP or plugin routing is identified as a later boundary, not part of the implemented c15b checkpoint. | [c15b next-gap section](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/docs/tutorial/c15b-async-child-sessions-parallel-handoff.md) | C04, C10 |
| `unknown` | This tutorial snapshot does not establish SaaS operations, multi-tenant authorization, benchmark performance, or production reliability. | [Pinned README scope](https://github.com/ZophiaWong/forge-harness/blob/9c1b1dbb0566e9053457db50e64cd374848de856/README.md) | C09, C10 |

Before each project mock, compare the moving repository with this snapshot and record the refreshed
URL, commit SHA, and access date in the session. Reclassify changed claims. Keep target architecture,
future chapters, tutorial demonstrations, and production behavior distinct.
