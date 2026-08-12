# Core Competency Model

Use this public model to select and assess preparation work for a career-changing,
junior-to-mid AI Agent application engineer targeting mainland China. Keep personal
levels and evidence in `.local/interview-prep/competency-matrix.md`.

## Level Scale

| Level | Observable standard |
| ---: | --- |
| 0 | Unassessed; no usable evidence. |
| 1 | Recognizes terms but cannot explain the mechanism independently. |
| 2 | Explains the mechanism and a basic example. |
| 3 | Applies the capability independently in code, design, diagnosis, or a project. |
| 4 | Defends tradeoffs, failure modes, alternatives, and changing constraints. |

Reading or completing a lesson is not evidence of a higher level. Prefer independent,
transfer, delayed-retest, project, and real-interview evidence in that order.

## Core Competencies

| ID | Capability statement | Priority | Default target | Evidence anchor |
| --- | --- | --- | ---: | --- |
| C01 | Write, test, debug, and explain Python solutions. | core | 3 | Executed Python or debugging task |
| C02 | Build reliable LLM application boundaries. | core | 3 | Prompt/schema/error-handling exercise |
| C03 | Design stateful Agent workflows. | core | 3 | Workflow/state-machine design |
| C04 | Govern Tool Calling, Function Calling, and MCP actions. | core | 3 | Tool contract and failure scenario |
| C05 | Design and diagnose an end-to-end RAG system. | core | 3 | RAG design and retrieval diagnosis |
| C06 | Evaluate and improve Agent/RAG behavior. | core | 3 | Eval plan, trace analysis, regression task |
| C07 | Ship AI applications through Python backend and data systems. | core | 3 | FastAPI/asyncio/PostgreSQL task |
| C08 | Apply security, permission, HITL, and audit controls. | core | 3 | Governed-action scenario |
| C09 | Produce system designs and defend technical tradeoffs. | core | 3 | Timed architecture exercise |
| C10 | Present truthful, defensible project evidence. | differentiator | 4 | MeterDesk and Forge Harness deep dives |
| C11 | Explain TypeScript, Node.js, and Agent harness runtime design. | supporting | 2 | Forge Harness code/runtime follow-up |
| C12 | Solve common SQL and DSA interview problems in Python. | supporting | 2 | Executed SQL/algorithm task |
| C13 | Communicate fit through resume, introduction, and behavior stories. | supporting | 3 | Timed introduction or behavioral mock |

Fine-tuning, model training, and inference optimization are extension topics with a
default target of 1-2 unless a future JD explicitly raises their priority.
Raise C11 or C12 from 2 to 3 when a target JD or interview lane emphasizes that capability.

## Observable Sub-Competencies

### C01 Python Coding and Problem Solving

- `C01.01`: Use core Python data structures, functions, exceptions, typing, and tests.
- `C01.02`: Debug incorrect behavior from evidence rather than guessing.
- `C01.03`: Explain time/space complexity and cover boundary cases.

### C02 LLM Application Fundamentals

- `C02.01`: Explain model limitations, stochastic behavior, and failure boundaries.
- `C02.02`: Design prompts and structured outputs with server-side validation.
- `C02.03`: Choose Prompt, RAG, tools, workflow constraints, or fine-tuning for a failure.

### C03 Agent Workflow and State

- `C03.01`: Distinguish deterministic workflows from autonomous Agent decisions.
- `C03.02`: Design state, nodes, routing, loops, termination, retry, and recovery.
- `C03.03`: Explain checkpoint, interrupt, memory, and multi-Agent boundaries.

### C04 Tool Calling and MCP

- `C04.01`: Design tool schemas and validate model-proposed arguments server-side.
- `C04.02`: Classify retryable errors, protect side effects with idempotency, and audit calls.
- `C04.03`: Explain MCP discovery, transport, trust, permission, and host/server boundaries.

### C05 RAG Engineering

- `C05.01`: Design parsing, cleaning, chunking, metadata, indexing, and version updates.
- `C05.02`: Choose vector, BM25, hybrid retrieval, filtering, rewrite, and reranking.
- `C05.03`: Design context construction, citations, grounding, and permission filtering.
- `C05.04`: Diagnose ingestion, retrieval, context, and generation failures separately.

### C06 Evaluation and Improvement

- `C06.01`: Build representative datasets, labels, slices, and reproducible baselines.
- `C06.02`: Separate retrieval, generation, outcome, trace, latency, cost, and safety metrics.
- `C06.03`: Compare prompt/model/policy versions and route Bad Cases back into tests.
- `C06.04`: Design and calibrate LLM-as-judge rubrics, evidence, confidence, and review gates.

### C07 Backend and Data Engineering

- `C07.01`: Design FastAPI contracts, lifecycle, validation, dependency injection, and errors.
- `C07.02`: Handle asyncio blocking, cancellation, timeout, concurrency, and background work.
- `C07.03`: Use PostgreSQL, transactions, indexes, Redis/cache, and task queues appropriately.
- `C07.04`: Explain deployment, logs, metrics, traces, health, limits, and graceful degradation.

### C08 Safety, HITL, and Audit

- `C08.01`: Separate authentication, authorization, policy, and data-scope checks.
- `C08.02`: Model proposal, approval, execution, rejection, expiry, and replay-safe transitions.
- `C08.03`: Apply sandboxing, secret handling, output filtering, and immutable audit evidence.

### C09 System Design and Tradeoffs

- `C09.01`: Clarify users, goals, constraints, risks, scale, and success measures first.
- `C09.02`: Draw boundaries and trace data/control flow through the system.
- `C09.03`: Defend reliability, latency, cost, consistency, build/buy, and framework choices.

### C10 Project Evidence

- `C10.01`: Explain MeterDesk's goal, governed run, approval gate, trace, and Eval Lab.
- `C10.02`: Explain Forge Harness's loop, permissions, context, recovery, and child sessions.
- `C10.03`: Separate implemented behavior, documented plans, proposed improvements, and guesses.
- `C10.04`: Present personal decisions, hard problems, tradeoffs, evidence, and lessons concisely.

### C11 TypeScript, Node.js, and Harness

- `C11.01`: Explain event loop, promises, cancellation, streams, and process boundaries.
- `C11.02`: Use TypeScript types, modules, errors, and tests in runtime code.
- `C11.03`: Explain harness state, tool runtime, permissions, compaction, and isolation.

### C12 SQL and DSA

- `C12.01`: Write joins, grouping, window functions, transactions, and index-aware SQL.
- `C12.02`: Solve common array, hash, window, tree, graph, heap, and DP problems in Python.
- `C12.03`: Clarify constraints, test edge cases, and state complexity.

### C13 Career Communication

- `C13.01`: Write resume claims backed by inspectable project evidence.
- `C13.02`: Deliver a role-specific 60-second and 2-minute introduction.
- `C13.03`: Answer behavioral questions with specific actions, results, and reflection.

## Relationship Rules

- Use one stable competency ID for each observed ability. Never create a second ID for a synonym.
- Treat the model as a graph: `parent` decomposes capability, `prerequisite` orders learning,
  `related` adds context without changing levels, and `used_by` connects a shared technique.
- Map `RAG evaluation`, `RAG eval`, and `检索评测` to C06 sub-competencies; relate them to C05
  without automatically raising the full C05 level.
- Keep `LLM-as-judge` canonical at `C06.04`; mark C05, C10, and C13 assessments as `used_by`.
- If no existing ID fits, record an unmapped note and ask for confirmation before extending this model.
- Never reuse or silently rename an ID that already appears in session evidence.

## Future JD Overlay

A JD overlay may raise or lower target levels and priorities, but it must reference these IDs.
It never changes personal evidence, duplicates a competency, or rewrites historical sessions.
