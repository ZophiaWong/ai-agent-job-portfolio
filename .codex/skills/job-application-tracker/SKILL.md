---
name: job-application-tracker
description: Use when evaluating a Notion job description, mapping confirmed AI Agent requirements to MeterDesk or Forge Harness evidence, preparing targeted bilingual project bullets, or updating application status.
---

# Job Application Tracker

Use this skill for job evaluation and application tracking. It is deliberately separate from `interview-prep-coach`: this skill handles JD evidence, project selection, bullets, and application state; the other handles mock interviews and post-interview learning.

## Source of truth

Read `reference/career-evidence/workflow-spec.md` before matching. Git tables are authoritative for capability IDs, claims, evidence, bullets, fixed commits, and boundaries. The two project repositories are read-only and must remain pinned to:

- MeterDesk: `f9dee13`
- Forge Harness: `a0146b2`

Run the validator before relying on a result:

```bash
validate-career-evidence --root <portfolio> \
  --project-root meterdesk=<meterdesk-path> \
  --project-root forge-harness=<forge-harness-path>
```

## Required flow

1. Read the selected Notion page, or the newest page in the `收件箱` view. Preserve the `## JD 原文` text exactly. If the title is absent, adding only a heading is allowed.
2. Extract requirements from JD wording. Propose known `capability_id` values and `must` / `nice` importance with the original quote. Put vocabulary outside the table in `unmapped_label`; never infer a project match for it.
3. Show the proposal to the user and wait. **不跳过 must / nice 确认**. Do not set `requirements_confirmed` or run `match-job` until the user explicitly confirms or corrects every requirement.
4. Build the confirmed JSON input and run:

```bash
match-job --root <portfolio> --input <confirmed-job.json> --output <match-result.json>
```

The matcher is deterministic, offline, and does not decide whether to apply. Treat `unmapped` and missing claims as unresolved, not as evidence of absence. A `must` requirement is a hard gap only when both projects have an explicit `gap` claim. An adjacent claim may support a risk note but must not generate an “implemented” bullet. Never turn policy text or context projection into RAG; never turn local demos into production, distributed, hosted, or crash-safe claims. Preserve the Forge Harness `REGRESSED` eval result.

5. Preview the exact Notion changes: confirmed `需求标注`, the generated `技术匹配结果`, derived properties (`岗位方向`, `需求已确认`, `技术就绪度`, and optional `简历版本`), and any proposed next action. Ask before changing `阶段`, `下一步行动`, `下一步日期`, or `投递与面试记录`. 写回前必须重新 fetch 页面.
6. Re-fetch the Notion page immediately before writing. Update only the managed sections and derived properties. `JD 原文` and `投递与面试记录` are read-only by default. If a managed heading is missing, append one section; if a heading is duplicated or its boundaries are ambiguous, stop and report instead of replacing broad page content.
7. If Notion write or re-fetch fails, save a pending artifact under `.local/job-application-tracker/pending/` without copying credentials or silently editing the source JD. Keep database, data-source, and view IDs in `.local/job-application-tracker/config.json`; this file is ignored and must never contain tokens.

## Notion model

Use the private `Job Applications` database and its Chinese fields. The stages are `待整理`, `待评估`, `准备投递`, `已投递`, `面试中`, `Offer`, and `已结束`; readiness values are `未分析`, `强匹配`, `相邻证据偏多`, `存在硬缺口`, and `待补充核查`. The page body has exactly these managed headings:

```markdown
## JD 原文
## 需求标注
## 技术匹配结果
## 投递与面试记录
```

When creating a page, keep the original JD in the first section and leave the other sections as explicit placeholders until confirmation and matching. When writing back, use a precise section replacement rather than replacing the entire page.

Use `notion_fetch` for a named page and `notion_query_data_sources` in view mode for the `收件箱`; use `notion_notion_update_page` with `update_content` for exact section replacements and `update_properties` for derived fields. Do not use `replace_content` for routine updates. Use `notion_notion_create_pages` only for a new database row or anonymous template.

## Output discipline

Return the match fingerprint, fixed project commits, primary and secondary project, readiness, hard gaps, adjacent risks, unresolved items, selected bilingual bullets, forbidden claims, verification reminders, and demo evidence IDs. Do not output percentages or a final “投不投” decision. 不把 RAG、policy text、context projection、local demo 包装成已实现的生产能力。Do not claim MCP server, RAG, async crash recovery, hosted platform, production scale, distributed coordination, or Java/Spring unless a new versioned claim is added, evidence is verified, and the user approves the vocabulary extension.
