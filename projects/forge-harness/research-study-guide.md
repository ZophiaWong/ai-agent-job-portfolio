# Forge Harness Research Study Guide

This guide uses the fixed source
[`research/agent-runtime-design-studies`](https://github.com/ZophiaWong/forge-harness)
at commit [`8fb8529b104350c36c2e1f2eecd1c40b4bb56d24`](https://github.com/ZophiaWong/forge-harness/commit/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24), accessed `2026-08-02`.
Start with its pinned [design-studies README](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/README.md), [STATUS](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/STATUS.md), [SOURCES](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/SOURCES.md), and [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md).

These reports are a reviewable learning source. They do not replace the existing
[`9c1b1dbb0566`](README.md#snapshot-claims) interview-evidence snapshot and do not claim that
Forge Harness `main` moved, matches the research, or implements a research proposal.

## Vocabulary for auditing claims

- **Session History** is the durable record of a conversation or run; **Runtime State** is the
  live control state that drives the next step; **Model Context** is the selected, bounded input
  sent to the model; **Workspace State** is the external files, tools, and side effects the runtime
  can inspect or change.
- **Mechanism** means the technical means that can make something happen; **Policy** means the
  rule choosing when it may happen; **Product behavior** means the user-visible outcome. Do not
  treat one as proof of either of the others.
- Mark each audited claim `implemented`, `proposed`, or `unknown`. A report can explain a design
  without establishing that the frozen Forge snapshot implements it.

## Learning units

1. **Synthesis and evidence method** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C03, C10, C11. Core question: How do we turn a comparative report into bounded evidence? Essential model: separate claim, source, mechanism, policy, product behavior, and proof status. Audit: (a) the synthesis is a review artifact, not an `implemented` Forge claim; (b) a source citation can support a design explanation while leaving runtime behavior `unknown`. Limitation: report synthesis is secondary evidence and may omit source-code detail. Cold answer: What evidence would let you classify a statement as `implemented`? Transfer: If the source commit changed, which conclusions remain `unknown` until re-audited?

2. **Loop and completion** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C03, C11. Core question: What makes an agent loop stop safely and credibly? Essential model: observe, decide, act, verify, recover, complete. Audit: (a) deterministic verification is a `Mechanism` for gating a final answer; (b) completion criteria are a `Policy`, while a reliable user result is `Product behavior` and may remain `unknown`. Limitation: the report may describe alternative loops rather than executable tests. Cold answer: Where would you place verification and one recovery attempt in a loop? Transfer: If verification becomes asynchronous and fallible, what policy prevents endless recovery?

3. **Tool runtime and action boundary** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C04, C10, C11. Core question: How is a model request converted into a bounded action? Essential model: tool schema, registry, dispatcher, authorization boundary, result. Audit: (a) a registry/dispatcher is a `Mechanism`; (b) rejecting unknown tools and enforcing a read boundary are `implemented` snapshot claims, whereas MCP/plugin routing is `proposed`. Limitation: a design report does not prove deployment authorization or tenant isolation. Cold answer: Why is schema validation insufficient as an action policy? Transfer: If a write tool is added, what policy and evidence must change before calling its product behavior safe?

4. **Context construction and compaction** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C03, C04, C11. Core question: What reaches the model, and what is intentionally left out? Essential model: project history and workspace observations into a bounded model context, then compact with retained invariants. Audit: (a) projection/compaction are `Mechanism` claims with executable snapshot tests; (b) token selection and retention priorities are `Policy`, not proof that model answers improve (`unknown` product behavior). Limitation: compaction quality depends on workload and model behavior not established by a report. Cold answer: Distinguish Session History from Model Context in one sentence. Transfer: If a privacy rule excludes raw tool output, what must the projection policy preserve instead?

5. **Session persistence and branching** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C03, C08, C11. Core question: Which state survives a pause, retry, or branch? Essential model: persist Session History separately from Runtime State and Workspace State, then resume from an explicit checkpoint. Audit: (a) persistence is a `Mechanism`, not automatically a branching `Policy`; (b) isolated edit-preview metadata is `implemented`, but durable multi-user branching behavior is `unknown`. Limitation: report terminology may not map one-to-one to the tutorial’s state objects. Cold answer: Which state must be captured to reproduce a paused run? Transfer: If a branch may apply writes, how should workspace isolation change?

6. **Delegation and coordination** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C03, C08, C10. Core question: How can child work run concurrently without losing accountability? Essential model: parent owns the task, child has scoped state, terminal notification returns once, and coordination policy resolves results. Audit: (a) pending-work tracking and once-only terminal notifications are `implemented` mechanisms; (b) delegation selection and merge/conflict handling are policies, while parallel speedup is `unknown` product behavior. Limitation: report examples do not establish scheduler fairness or production reliability. Cold answer: What event makes a child result safe to consume exactly once? Transfer: If two children edit the same file, what coordination policy decides the next action?

7. **Extensibility governance and trust** — Source report: [agent-runtime synthesis](https://github.com/ZophiaWong/forge-harness/blob/8fb8529b104350c36c2e1f2eecd1c40b4bb56d24/docs/design-studies/07-agent-runtime-design-synthesis.md). Competencies: C04, C10, C11. Core question: How do extensions expand capability without silently expanding trust? Essential model: extension registration, declared capability, policy check, audit trail, revocation boundary. Audit: (a) routing external MCP/plugins is `proposed`, not `implemented`; (b) a capability check is a mechanism, but least-privilege and operator approval are policies, and trustworthy SaaS operation remains `unknown`. Limitation: the report cannot prove third-party extension behavior or supply-chain controls. Cold answer: What is the difference between loading an extension and trusting it? Transfer: If extensions can call nested tools, where must trust be re-checked?

## Fixed study loop

For every unit: (1) cold answer, (2) read the report, (3) inspect at most three code/test anchors,
(4) record **claim / evidence / not-proven**, (5) solve the transfer question, then (6) optionally
begin a structured learn session. Do **not** update the competency matrix merely for reading;
record a change only after assessed evidence supports it.
