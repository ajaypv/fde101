---
title: Context engineering
description: Curating the instructions, tools, history, state, and evidence available to a model for each call.
contentType: glossary
level: Beginner
minutes: 4
topics: [context engineering, prompts, agents]
lastVerified: 2026-08-15
sidebar:
  order: 29
sources:
  - title: Effective context engineering for AI agents
    url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    publisher: Anthropic
    type: official-doc
---

**Context engineering** chooses and organizes the tokens available to a model for one inference: instructions, tool definitions, examples, retrieved evidence, message history, state, and runtime results.[^context]

## Prompting versus context engineering

| Prompt engineering | Context engineering |
| --- | --- |
| Writes and organizes instructions | Curates the model's complete working set |
| Often changes a prompt template | May retrieve, filter, compact, or remove information on every turn |
| Asks “How should I say the task?” | Asks “What should the model know right now?” |

## Tiny example

For a refund question, the useful context may be the system rule, the signed-in user's region, the current regional policy passage, one order lookup result, and enough message history to resolve “that order.” The entire policy library and complete chat history would add noise.

For a Python authentication change, useful context may be the current route, service interface, user model, token utility, dependency versions, and relevant tests. “Write production-ready authentication code” is an instruction, not a substitute for those repository facts.

## FDE note

Treat context as a limited budget. Keep the smallest high-signal set that supports the next decision, and keep authorization outside the model.

Read the full [prompt-versus-context lesson](../../foundations/context-engineering/) for a runnable context-selection example.

[^context]: Anthropic, [“Effective context engineering for AI agents”](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
