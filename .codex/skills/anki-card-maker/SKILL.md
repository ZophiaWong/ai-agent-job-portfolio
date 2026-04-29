---
name: anki-card-maker
description: Generate, review, improve, and add high-quality Anki cards from notes, articles, job-search material, technical docs, interview prep, or other study sources. Use when the user asks Codex to create flashcards, convert material into Anki notes, critique card quality, apply Wozniak/SuperMemo-style minimum-information principles, or add cards through Anki MCP.
---

# Anki Card Maker

Use this skill to turn source material into durable Anki cards and to add them through Anki MCP when the user explicitly approves creation.

## Source Reference

For detailed card-making principles, read `references/card-making-20rules.md` when:
- the user asks for card quality, learning efficiency, or Wozniak/SuperMemo principles
- source material is dense, list-heavy, ambiguous, or likely to create interference
- generating more than a small handful of cards
- reviewing or improving existing cards

## Workflow

1. Understand the material before card creation.
   - Do not make cards from unclear material.
   - Ask a concise clarification question or mark the ambiguity in the preview if the source is underspecified.
   - Build from basics before details.

2. Select only memorization-worthy knowledge.
   - Prioritize concepts, definitions, distinctions, constraints, workflows, commands, recurring mistakes, and high-value facts.
   - Skip trivia unless the user asks for exhaustive coverage.
   - Prefer fewer strong cards over many weak cards.

3. Make cards atomic.
   - Test one idea per card.
   - Keep answers short.
   - Split long answers into multiple cards.
   - Do not put explanations in the answer unless they are part of the recall target; place optional context in parentheses or an extra field if the model supports it.

4. Choose the right card type.
   - Use Basic cards for direct Q/A, distinctions, definitions, and commands.
   - Use Cloze cards when a sentence supplies useful context and one small missing piece should be recalled.
   - Use multiple clozes instead of hiding several facts at once.
   - Use reverse cards only when both directions are genuinely useful.

5. Avoid sets and enumerations.
   - Avoid prompts like "What are all X?"
   - Break lists into grouped, ordered, contextual, or overlapping cloze cards.
   - If an ordered sequence must be learned, use small adjacent chunks.

6. Reduce interference.
   - Make prompts specific enough to distinguish similar ideas.
   - Add compact context prefixes such as `React:`, `LLM evals:`, `Job search:`, or `bioch:` when they shorten wording and prevent ambiguity.
   - Add contrast cards for commonly confused terms.

7. Use examples when they improve recall.
   - Prefer personal, concrete, or emotionally vivid examples when the user supplies them or the context clearly supports them.
   - Do not invent personal facts about the user.

8. Preserve provenance.
   - Include source, version, date, or collection timestamp when available, especially for unstable facts.
   - Treat source and timestamp as metadata unless the user specifically wants to memorize them.

9. Preview before writing.
   - Show deck, model, tags, and card fields.
   - Explain any discarded or merged source material briefly when useful.
   - Do not call Anki MCP `addNote` or `addNotes` until the user explicitly confirms creation.

## Quality Gate

Revise or reject any card that:
- tests multiple independent facts
- has a long answer
- asks for an unordered list
- depends on context not present in the prompt
- can be answered by recognition without real retrieval
- is likely to be confused with a nearby card
- stores volatile information without source or timestamp
- encodes material the user likely does not understand

## Anki MCP Procedure

When the user approves adding cards:

1. Check decks and note models if the target deck or model is unknown.
2. Use the requested deck. If no deck is provided and no reasonable default exists, ask.
3. Use `Basic` for front/back cards and `Cloze` for cloze deletions unless the user requests another model.
4. Use `addNotes` for batches sharing a deck and model.
5. Use consistent tags:
   - topic or domain
   - source or project
   - date or version when relevant
   - `generated-by-codex` unless the user prefers otherwise
6. Report the created note IDs and any skipped duplicates or validation failures.

## Preview Format

Use this compact preview shape:

```markdown
Deck: <deck>
Model: <Basic|Cloze>
Tags: <tags>

1. Front: ...
   Back: ...

2. Text: ... {{c1::...}} ...
```

For mixed Basic and Cloze cards, separate previews by model because Anki MCP batches require one model per `addNotes` call.
