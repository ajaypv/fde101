---
title: Messages
description: Represent system instructions, user turns, model output, and tool results without flattening them into one string.
contentType: lesson
level: Beginner
minutes: 4
topics: [LangChain, messages, context]
lastVerified: 2026-08-15
sidebar:
  order: 2
sources:
  - title: Messages
    url: https://docs.langchain.com/oss/python/langchain/messages
    publisher: LangChain
    type: official-doc
---

A **message** carries a role, content, and optional metadata. The main types are `SystemMessage`, `HumanMessage`, `AIMessage`, and `ToolMessage`.

## Tiny example

```python
from langchain.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("Answer from the supplied refund policy only."),
    HumanMessage("Can order A-19 be returned after 45 days?"),
]
reply = model.invoke(messages)
```

Think of the list as the envelope sent on this call. A model is not remembering an earlier Python request unless your application sends or retrieves that history again.

## What belongs where?

| Message | Job |
| --- | --- |
| System | Stable role, rules, and boundaries |
| Human | The user's current request |
| AI | A model response, including requested tool calls |
| Tool | One tool result tied to one tool-call ID |

## Failure note

Do not treat message history as durable memory. Long histories can exceed the context window, retain stale facts, or cross tenant boundaries if keyed incorrectly. Store, filter, and trim history deliberately.

## Related

[Prompt templates](../prompt-templates/) · [Tool calling](../tool-calling/) · [`create_agent`](../create-agent/)
