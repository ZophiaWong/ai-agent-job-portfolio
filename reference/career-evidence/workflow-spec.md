# Career Evidence Workflow

这套材料把岗位要求、项目事实、证据定位和简历表达拆成四层。Notion 负责真实岗位和投递进展；Git 负责可审计的项目事实源。

## 固定版本

- MeterDesk：`f9dee13`
- Forge Harness：`a0146b2`
- 任何提交变化都需要重新验证受影响 claim；匹配器不会自动升级或降级证据。

## 文件接口

- `capabilities.csv`：能力 ID、定义、边界和仅用于语义提示的别名。
- `claims.csv`：项目可声称的事实与明确缺口。一个 claim 只表达一个可面试主张。
- `evidence.csv`：实现、规格、测试、smoke、截图、报告或边界证据。一个 claim 可以有多条证据。
- `bullets.csv`：按岗位路线和语言复用的候选 bullet。bullet 依赖 claim，不直接依赖 JD 词语。

多值字段只使用分号：`claim_ids`、`demo_evidence_ids`、`aliases`。CSV 中的自然语言字段使用标准 CSV quoting。

## 证据等级

| 等级 | 含义 |
| --- | --- |
| `verified_direct` | 当前提交有直接实现，并有至少一条实现/规格证据和一条测试、smoke 或报告验证证据。 |
| `direct_implementation` | 当前提交有直接实现，但独立验证仍不足。 |
| `adjacent` | 有可迁移的相邻机制，但不是 JD 要求的同一能力。 |
| `gap` | 规格明确排除、roadmap 未实现或固定提交核查确认缺失。 |

没有 claim 记录时，匹配结果使用 `unassessed`；不自动把没有登记等同于 `gap`。JD 词表外要求使用 `unmapped`，需用户批准扩展能力表并重新核查项目。

## 匹配规则

1. Codex 从 JD 原句提出 `capability_id`、`must/nice` 和引用原句；用户确认后才可运行匹配器。
2. 匹配器按能力 ID 精确关联 claim，不在项目源码中做关键词搜索，也不调用模型。
3. 等级优先级为 `verified_direct > direct_implementation > adjacent > gap`。
4. `must` 在两个项目均为明确 `gap` 才形成硬缺口；`nice` 缺失不会形成硬缺口。
5. `must` 只有 `adjacent` 时形成相邻证据风险，不能生成已实现式 bullet。
6. 项目顺序首先服从岗位路线：Applied Agent 与后端/全栈以 MeterDesk 为主，Runtime 以 Forge Harness 为主；同一路线内再按直接覆盖数稳定排序。
7. bullet 的全部依赖 claim 必须达到其 `min_evidence_level`，否则不输出为可用草稿。
8. 不计算百分制，不替用户决定是否投递。

## Notion 边界

每条岗位页面固定四段：

```text
## JD 原文
## 需求标注
## 技术匹配结果
## 投递与面试记录
```

`JD 原文`和`投递与面试记录`默认只读；`需求标注`必须经用户确认；`技术匹配结果`是唯一可自动整体替换的章节。写回前必须 fetch 最新页面并使用精确章节替换；章节重复或页面结构不符合预期时停止，不整页覆盖。

Notion 连接配置只放在 `.local/job-application-tracker/config.json`，真实 JD 和投递记录不提交 Git。Notion 失败时结果进入 `.local/job-application-tracker/pending/`，不丢失分析。

## 命令

```bash
python scripts/validate-career-evidence \
  --root . \
  --project-root meterdesk=/home/poter/resume-pj/meter-desk \
  --project-root forge-harness=/home/poter/resume-pj/forge-harness

python scripts/match-job --root . --input confirmed-job.json --output match-result.json
```

匹配输入要求 `requirements_confirmed: true`，且 `role_track` 必须是 `applied-agent`、`runtime`、`ai-backend` 或 `ai-fullstack`。输出包含数据指纹、项目提交、逐项项目匹配、硬缺口、风险、项目顺序、候选中英 bullet、禁用表述和演示证据。
