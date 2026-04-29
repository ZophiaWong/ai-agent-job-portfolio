# AI Agent Job Portfolio

针对求职 AI Agent 应用的工作。

综合了学习资料、Best-Practice、Top-player 等部分。

## How to Use

### 配合 Anki 使用

本仓库提供了一个 Codex skill：[`skills/anki-card-maker`](skills/anki-card-maker/SKILL.md)，用于把学习材料、求职笔记、技术文档、面试题等内容转换成高质量 Anki 卡片。

这个 skill 会参考 [`refs/card-making-20rules.md`](refs/card-making-20rules.md) 中的制卡原则，重点保证：

- 先理解材料，再制卡
- 一张卡只考一个知识点
- 避免「列出所有……」这类集合题
- 优先使用简洁问答或 Cloze
- 给易混淆内容补充上下文
- 对不稳定信息保留来源和时间戳
- 通过 Anki-MCP 写入前先预览，确认后再添加

使用方式是在 Codex 对话中显式调用 skill：

```text
Use $anki-card-maker to generate Anki cards from this material.
Target deck: Agent Jobs
Preview the cards first, and wait for my approval before adding them through Anki MCP.
```

也可以粘贴具体材料：

```text
Use $anki-card-maker.

Source:
<粘贴文章、笔记、JD、面试复盘或技术文档>

Target deck: Agent Jobs
Goal: make concise Basic and Cloze cards.
Preview first.
```

推荐流程：

1. 启动 Anki，并安装/启用 AnkiConnect 插件。
2. 用本仓库的启动脚本打开 Codex：

   ```shell
   ./scripts/codex-anki
   ```

   这个脚本会在当前仓库目录启动 Codex，并临时注入 Anki-MCP 配置：
   - MCP server 名称：`anki-mcp`
   - 启动命令：`npx -y @ankimcp/anki-mcp-server --stdio`
   - AnkiConnect 地址：`http://localhost:8765`
   - `NO_PROXY/no_proxy`：`localhost,127.0.0.1,::1`

   也可以把参数继续传给 Codex，例如：

   ```shell
   ./scripts/codex-anki "Use $anki-card-maker to make cards from refs/card-making-20rules.md. Preview first."
   ```

3. 在 Codex 中使用 `$anki-card-maker` 生成卡片预览。
4. 检查 deck、model、tags、Front/Back 或 Cloze 内容。
5. 明确回复确认添加，例如：`确认，添加到 Agent Jobs`。
6. Codex 再通过 Anki-MCP 批量写入卡片。

## Acknowledge

- [agent_java_offer](https://github.com/guoguo-tju/agent_java_offer)
-

## Recommended Sources
