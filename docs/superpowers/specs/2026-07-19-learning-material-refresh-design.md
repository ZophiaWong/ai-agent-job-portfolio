# Learning Material Refresh Design

## Goal

Turn the repository's committed and currently uncommitted study material into a
discoverable, competency-driven, evidence-producing interview-preparation library
for a mainland-China, career-changing, junior-to-mid AI Agent application engineer.

## Approved Scope

This design implements the review approved on 2026-07-19. It covers public material
only. `.local/interview-prep/` remains private and untouched.

The work will:

- remove empty, obsolete, misleading, and duplicate public drafts;
- preserve the useful Agent/RAG/backend reference chapters as reference material;
- make all retained material reachable from a small set of public indexes;
- correct the reviewed DSA, Python, Node.js, Express, packaging, and LangGraph issues;
- replace reading/self-rating completion with cold-answer, execution, transfer, and
  delayed-retest evidence expectations;
- consolidate the old job matrix and competing study routes around stable C01-C13 IDs;
- add focused material for SQL/PostgreSQL, evidence-driven Python debugging, and LLM
  stochastic behavior and failure boundaries;
- distinguish implemented project facts from plans, design exercises, and guesses.

## Information Architecture

`README.md` remains the public root. It links to four canonical areas:

1. the C01-C13 competency model;
2. the system reference handbook, with a clickable chapter table of contents;
3. an `interviews-docs/README.md` practice index for AI, backend/runtime, DSA/SQL,
   and career communication;
4. project evidence and a small `best-practice/README.md` engineering-practice index.

`learning-materials/` will not receive a new index. Its current contents are empty,
obsolete, or duplicated, so they will be removed and useful replacements will live
beside their canonical subject.

## Material Contract

Every retained or newly added practice entry must make its role clear:

- stable competency ID or IDs;
- whether it is reference, practice, or project evidence;
- a cold prompt that does not reveal the answer first;
- an executable or inspectable evidence task where the competency permits one;
- a transfer or changed-constraint prompt;
- a delayed-retest expectation.

Reading a page, checking a box, or repeating the displayed answer is never evidence
of a higher competency level.

## Truth and Version Boundaries

- First-person project claims must link to inspectable MeterDesk or Forge Harness
  evidence. Generic designs are labeled as exercises or proposed designs.
- Framework-sensitive claims use official primary documentation and state relevant
  version boundaries or an access date.
- Code that is not executed in this repository is labeled as a sketch. A document
  must not claim a LangGraph approval flow is runnable unless pause and resume are
  represented with a checkpointer, stable `thread_id`, `interrupt()`, and
  `Command(resume=...)` and are covered by a verification path.

## Testing

Repository tests will cover:

- recursive local Markdown/image link resolution for public material;
- canonical entrypoints and retained-material reachability;
- absence of known placeholders and obsolete redirect pages;
- presence of reviewed version/truth boundaries in Python and Node material;
- the DSA evidence protocol and corrected DP example;
- competency IDs and evidence tasks in new gap-filling modules;
- absence of unsupported first-person claims in generic engineering-practice material;
- corrected LangGraph HITL protocol markers and explicit sketch/runnable status.

Each behavioral change follows a red-green cycle. Documentation-only cleanup is
verified by the repository contract tests, `git diff --check`, and link checks.

## Delivery

Work is performed on `codex/learning-material-refresh` in an external worktree so the
user's dirty `main` checkout and retained stash stay unchanged. Changes are split into
reviewable commits by material family. No push, PR, merge, stash drop, or private-state
write is part of this design.
