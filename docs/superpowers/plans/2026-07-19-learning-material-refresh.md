# Learning Material Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a clean, navigable, technically current, competency-driven public learning library from the repository's committed and currently uncommitted materials.

**Architecture:** Keep the existing content directories, but establish canonical indexes and a shared evidence protocol. Retain deep chapters as reference material, turn interview material into cold practice with inspectable evidence, and enforce navigation/truth/version boundaries with repository tests.

**Tech Stack:** Markdown, Python `unittest`, Git, official primary documentation for version-sensitive technical facts.

## Global Constraints

- Target mainland-China, career-changing, junior-to-mid AI Agent application engineer roles.
- Stable competency IDs are C01-C13 from `.codex/skills/interview-prep-coach/references/competency-model.md`.
- Reading completion, displayed answers, self-rating, and unchecked code are not capability evidence.
- `.local/interview-prep/` is private: do not read, write, copy, or commit it.
- Generic templates must not assert unsupported first-person project experience.
- Changing framework/API facts must use official primary sources and record a version boundary or access date.
- Do not add external APIs, model keys, databases, Web UI, or a full learning scheduler.
- Preserve the user's original dirty `main` worktree and `stash@{0}`.
- Do not push, open a PR, merge, or drop a stash.

---

### Task 1: Public Material Contract, Cleanup, and Navigation

**Files:**
- Modify: `tests/test_repository_navigation.py`
- Create: `tests/test_learning_materials.py`
- Modify: `README.md`
- Create: `interviews-docs/README.md`
- Modify: `interviews-docs/01-AI/README.md`
- Modify: `interviews-docs/02-后端/README.md`
- Create: `interviews-docs/practice-protocol.md`
- Create: `best-practice/README.md`
- Modify: `AI_Agent_System_Practical_Reference/00_README_学习路线与资料使用说明.md`
- Modify: `.codex/skills/anki-card-maker/references/card-making-20rules.md`
- Delete: `learning-materials/LangGraph.md`
- Delete: `learning-materials/PostgreSQL-crash.md`
- Delete: `learning-materials/RAG-basis.md`
- Delete: `learning-materials/python-crash.md`
- Delete: `best-practice/Harness-Engineering/openai-harness-engineering.md`
- Delete: `best-practice/top-players/agents-design-from-lidangzzz.md`
- Delete: `best-practice/top-players/claude-code-leakage.md`
- Delete: `interviews-docs/05-misc/gap-year-explanation.md`
- Delete: `interviews-docs/05-misc/python.md`
- Delete: `interviews-docs/05-misc/nodejs.md`

**Interfaces:**
- Consumes: current root entrypoints and the C01-C13 model.
- Produces: canonical clickable navigation and a shared practice contract used by Tasks 2-7.

- [ ] **Step 1: Add failing repository-contract tests**

  Add tests that recursively resolve local Markdown links and images in public Markdown,
  assert the canonical entrypoints exist, reject `NEED TO PLAN`/`Example:` placeholder
  indexes, reject the two redirect pages, and require the system handbook README to
  contain real links to chapters 01-16. Run:

  ```bash
  python3 -m unittest tests.test_repository_navigation tests.test_learning_materials -v
  ```

  Expected: FAIL on the four broken Anki references, placeholder indexes, absent indexes,
  and non-clickable handbook table of contents.

- [ ] **Step 2: Implement the minimal cleanup and indexes**

  Remove the listed empty/obsolete files. Create the shared practice protocol with the
  exact sequence `冷启动 → 澄清约束 → 独立作答/编码 → 执行或检查 → 解释权衡 → 迁移题 → 延迟复测`.
  Replace placeholder indexes with links to retained material. Make the system handbook
  table of contents and role paths clickable. Remove or convert the four broken Anki
  links without removing their surrounding learning-rule explanation.

- [ ] **Step 3: Verify green**

  Run the focused command from Step 1, then:

  ```bash
  python3 -m unittest discover -s tests -v
  git diff --check
  ```

  Expected: all tests PASS and `git diff --check` exits 0.

- [ ] **Step 4: Commit**

  ```bash
  git add README.md interviews-docs best-practice learning-materials AI_Agent_System_Practical_Reference/00_README_学习路线与资料使用说明.md .codex/skills/anki-card-maker/references/card-making-20rules.md tests
  git commit -m "docs: clean and connect learning material entrypoints"
  ```

### Task 2: DSA Practice Series

**Files:**
- Modify: `interviews-docs/03-DS_AL/README.md`
- Modify: `interviews-docs/03-DS_AL/CheatSheet.md`
- Create/Modify: `interviews-docs/03-DS_AL/01_数组与双指针.md`
- Create/Modify: `interviews-docs/03-DS_AL/02_滑动窗口.md`
- Create/Modify: `interviews-docs/03-DS_AL/03_链表.md`
- Create/Modify: `interviews-docs/03-DS_AL/04_二叉树.md`
- Create/Modify: `interviews-docs/03-DS_AL/05_动态规划.md`
- Create/Modify: `interviews-docs/03-DS_AL/06_回溯与搜索.md`
- Create/Modify: `interviews-docs/03-DS_AL/07_堆栈队列二分.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: `interviews-docs/practice-protocol.md` and C12.02/C12.03.
- Produces: a linked DSA practice lane with executable evidence requirements.

- [ ] **Step 1: Add failing DSA tests**

  Require the README to link the shared protocol and all seven chapters; require C12.02
  and C12.03 mapping; reject `def one_dim_dp`; require the DP chapter to state a real
  state definition and transition; require each chapter to name edge-case/complexity
  evidence. Run the focused test and confirm the expected failure.

- [ ] **Step 2: Correct and align the material**

  Replace the fake generic DP template with House Robber or Kadane and explicitly state
  its problem-specific state. Add preconditions to sliding-window/binary-search templates,
  input-mutation/recursion-depth boundaries where relevant, and a common evidence block
  that points to the shared practice protocol without duplicating it.

- [ ] **Step 3: Verify and commit**

  Run the focused tests, full suite, and `git diff --check`, then commit:

  ```bash
  git add interviews-docs/03-DS_AL tests/test_learning_materials.py
  git commit -m "docs: add evidence-driven DSA practice series"
  ```

### Task 3: Python Interview and Backend Series

**Files:**
- Modify: `interviews-docs/05-misc/python/README.md`
- Modify: `interviews-docs/05-misc/python/01-containers.md`
- Modify: `interviews-docs/05-misc/python/05-typing-dataclass-pydantic.md`
- Modify: `interviews-docs/05-misc/python/07-asyncio-blocking.md`
- Modify: `interviews-docs/05-misc/python/08-thread-process-gil.md`
- Modify: `interviews-docs/05-misc/python/09-pytest-mock-fixture.md`
- Modify: `interviews-docs/05-misc/python/10-fastapi-lifecycle-di.md`
- Modify: `interviews-docs/05-misc/python/11-packaging-venv-lock.md`
- Retain and lightly align: remaining Python chapters
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: shared practice protocol and C01/C07.
- Produces: technically current Python reference/practice material with explicit evidence tasks.

- [ ] **Step 1: Add failing Python boundary tests**

  Reject bytecode-atomicity as a thread-safety guarantee; require shallow-freeze wording
  and an immutable tuple in the frozen dataclass example; require TaskGroup, timeout, and
  cancellation; require default GIL-enabled/free-threaded version boundaries; require
  `pip freeze` to be labeled an environment snapshot rather than a solver-produced lock;
  require pytest/FastAPI execution tasks. Confirm failures.

- [ ] **Step 2: Update from official sources and add evidence tasks**

  Use current official Python, pip, FastAPI, pytest, Pydantic, and packaging documentation.
  Put an access date of `2026-07-19` beside version-sensitive notes. Link the shared
  practice protocol and map the README to C01/C07 without turning every topic into P0.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests and `git diff --check`, then commit the entire Python directory:

  ```bash
  git add interviews-docs/05-misc/python tests/test_learning_materials.py
  git commit -m "docs: add current Python backend interview practice"
  ```

### Task 4: Node.js, TypeScript, and Cross-Runtime Series

**Files:**
- Modify: `interviews-docs/05-misc/nodejs/README.md`
- Modify: `interviews-docs/05-misc/nodejs/01-event-loop.md`
- Modify: `interviews-docs/05-misc/nodejs/03-promise-async-await-errors.md`
- Modify: `interviews-docs/05-misc/nodejs/05-commonjs-esm.md`
- Modify: `interviews-docs/05-misc/nodejs/10-timeout-cancel-retry-idempotency.md`
- Modify: `interviews-docs/05-misc/nodejs/11-testing-mock-integration.md`
- Modify: `interviews-docs/05-misc/nodejs/12-express-fastify-nestjs.md`
- Retain and lightly align: remaining Node.js chapters
- Modify: `interviews-docs/05-misc/python-vs-nodejs.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: shared practice protocol and C11 target level 2.
- Produces: version-bounded Node/TypeScript practice and one canonical cross-runtime comparison.

- [ ] **Step 1: Add failing Node boundary tests**

  Require the Node 20/libuv 1.45 timers boundary; require modern synchronous
  `require(esm)` limits; require Express 5 qualification; reject a retry example that
  sleeps after its final failure or retries unclassified errors; require a test example
  to exercise production code rather than the fake directly; require an AbortSignal task.

- [ ] **Step 2: Correct examples using official sources**

  Use current Node and Express primary documentation with access date `2026-07-19`.
  Implement a bounded retry sketch with explicit retry classification, exponential backoff
  plus jitter, `Retry-After` consideration, cancellation, and no final sleep. Replace the
  fake-only test with a service using an injected fake. Keep C11 supporting priority at 2.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests and `git diff --check`, then commit:

  ```bash
  git add interviews-docs/05-misc/nodejs interviews-docs/05-misc/python-vs-nodejs.md tests/test_learning_materials.py
  git commit -m "docs: add versioned Node and TypeScript interview practice"
  ```

### Task 5: Evidence-Backed Agent-Assisted Development Practice

**Files:**
- Delete/Rename: `best-practice/vibe-coding/`
- Create: `best-practice/agent-assisted-development/README.md`
- Create: `best-practice/agent-assisted-development/workflow-checklist.md`
- Modify: `best-practice/README.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: C04, C06, C08, C10, C13 and public Forge Harness evidence pages.
- Produces: a two-file engineering-practice entry with explicit truth boundaries.

- [ ] **Step 1: Add failing terminology and truth tests**

  Reject a retained `best-practice/vibe-coding` directory, unsupported phrases such as
  `我做过一个代码助手方向的实践`, and hypothetical metrics presented as results.
  Require an explicit distinction between the historical/public “vibe coding” term and
  controlled agent-assisted development, plus links to Forge Harness evidence.

- [ ] **Step 2: Consolidate the useful material**

  Keep the scope/context/plan/minimal-patch/verify/review/bad-case loop and the operational
  checklist. Remove repetitive recommended-answer scripts. Label all metrics as measurement
  candidates unless a public project snapshot proves a value. Cite the public terminology
  source and record access date `2026-07-19`.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests and `git diff --check`, then commit:

  ```bash
  git add best-practice tests/test_learning_materials.py
  git commit -m "docs: document evidence-backed agent-assisted development"
  ```

### Task 6: Consolidate the Canonical Competency Route

**Files:**
- Modify: `AI_Agent_System_Practical_Reference/00_README_学习路线与资料使用说明.md`
- Modify: `AI_Agent_System_Practical_Reference/00_岗位调研与能力画像/01_AI_Agent应用岗位招聘调研报告.md`
- Modify: `AI_Agent_System_Practical_Reference/00_岗位调研与能力画像/02_岗位核心能力矩阵.md`
- Delete: `AI_Agent_System_Practical_Reference/00_岗位调研与能力画像/03_章节重要性映射表.md`
- Delete: `AI_Agent_System_Practical_Reference/00_岗位调研与能力画像/04_学习优先级建议.md`
- Replace directory contents with one index: `AI_Agent_System_Practical_Reference/role_paths/README.md`
- Modify: `AI_Agent_System_Practical_Reference/Part_04_项目与面试表达/11_项目设计模板与架构表达.md`
- Modify: `AI_Agent_System_Practical_Reference/Part_04_项目与面试表达/12_高频面试题与答题闭环.md`
- Modify: `AI_Agent_System_Practical_Reference/Part_04_项目与面试表达/13_总复习Checklist与学习计划.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: canonical C01-C13 model and project evidence indexes.
- Produces: one evidence-driven 2-3 week route and truth-safe system-design practice.

- [ ] **Step 1: Add failing route/truth tests**

  Reject pseudo-precise 96/94/93 capability scores, multiple seven-day reading routes,
  `我设计并实现` claims in generic templates, and answer-first question-bank structure.
  Require the historical survey to say its sample is international/senior-skewed and not
  the current target baseline. Require one C01-C13 route with daily evidence outputs.

- [ ] **Step 2: Consolidate and relabel**

  Make the handbook a reference chosen by competency gap rather than a book read in order.
  Replace the old matrix with a pointer to the canonical model. Collapse role paths to a JD
  overlay index. Turn Chapter 12 into a cold question index with answers/rubrics placed after
  an explicit separator or in collapsible/linked answer sections. Turn Chapter 13 into the
  public 2-3 week evidence route; private daily allocation stays in `.local`.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests and `git diff --check`, then commit all listed handbook files.

### Task 7: Fill C02.01, C01.02, C07.03, and C12.01 Gaps

**Files:**
- Create: `interviews-docs/01-AI/llm-failure-boundaries.md`
- Create: `interviews-docs/02-后端/python-debugging.md`
- Create: `interviews-docs/02-后端/sql-postgresql.md`
- Modify: `interviews-docs/01-AI/README.md`
- Modify: `interviews-docs/02-后端/README.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: shared practice protocol and C02.01/C01.02/C07.03/C12.01.
- Produces: three focused, executable gap-filling practice modules.

- [ ] **Step 1: Add failing coverage tests**

  Require stable competency IDs, cold prompts, executable/inspectable evidence, transfer
  prompts, and delayed retest. Require SQL coverage of JOIN, GROUP BY/HAVING, window
  functions, transactions, indexes, and EXPLAIN; debugging coverage of reproduction,
  traceback/log evidence, hypothesis, minimal fix, regression test; LLM boundary coverage
  of stochastic output, nondeterminism despite temperature controls, schema validation,
  refusal/uncertainty, and failure-mode selection.

- [ ] **Step 2: Write minimal focused modules**

  Keep each module concise and interview-oriented. Include runnable SQL/Python examples or
  deterministic inspection tasks without adding a database dependency. Do not place the
  full answer before the cold task.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests and `git diff --check`, then commit the three modules, indexes, and tests.

### Task 8: Repair LangGraph HITL and Project Truth Boundaries

**Files:**
- Modify: `AI_Agent_System_Practical_Reference/Part_01_Agent核心原理/03_工具调用_FunctionCalling_MCP_与行动能力.md`
- Modify: `AI_Agent_System_Practical_Reference/Part_05_框架专项与实战Lab/14_LangGraph工程实战专项.md`
- Modify: `AI_Agent_System_Practical_Reference/Part_05_框架专项与实战Lab/16_端到端实战Lab与代码骨架.md`
- Modify: `AI_Agent_System_Practical_Reference/references_参考来源.md`
- Modify: `tests/test_learning_materials.py`

**Interfaces:**
- Consumes: C03.03/C04.03/C08.02/C10.03 and current official LangGraph/MCP docs.
- Produces: accurate protocol sketches with explicit executability and truth labels.

- [ ] **Step 1: Add failing HITL/protocol tests**

  Require Chapter 16 to contain checkpointer, stable `thread_id`, `interrupt()`, and
  `Command(resume=...)`; require the approval path to distinguish proposed/approved/executed
  state and use an action-specific idempotency key; reject `task_id:tool_name` as sufficient.
  Require explicit “design sketch, not verified repository source” labeling unless a runnable
  lab and integration test are added. Require MCP lifecycle, capability negotiation,
  host-client-server, transport, resource/prompt, trust, and authorization coverage.

- [ ] **Step 2: Correct from official primary documentation**

  Update with access date `2026-07-19`. Replace the non-pausing approval node and disconnected
  approval endpoint with one coherent pause/resume sketch. Ensure validation precedes success.
  Remove every resume/project claim that implies the sketch was implemented. Mark Chapter 14
  as the framework mapping and Chapter 16 as the end-to-end design sketch unless execution is
  actually added and verified.

- [ ] **Step 3: Verify and commit**

  Run focused/full tests, any skill validator, and `git diff --check`, then commit the corrected
  Agent/LangGraph material and reference list.

### Task 9: Whole-Branch Verification and Review

**Files:**
- Review all branch changes; modify only files required by review findings.

**Interfaces:**
- Consumes: Tasks 1-8.
- Produces: verified branch ready for the user's chosen integration action.

- [ ] **Step 1: Run complete verification**

  ```bash
  python3 -m unittest discover -s tests -v
  python3 /mnt/c/Users/Poter/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/interview-prep-coach
  python3 /mnt/c/Users/Poter/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/anki-card-maker
  git diff --check
  git status --short
  ```

- [ ] **Step 2: Run final whole-branch review**

  Generate a review package from merge base `f451e6d` to HEAD and dispatch the final reviewer.
  Fix all Critical and Important findings, re-run covering tests, and re-review.

- [ ] **Step 3: Present integration choices**

  Use `superpowers:finishing-a-development-branch`. Do not merge, push, open a PR, or remove
  the worktree until the user explicitly chooses an option.
