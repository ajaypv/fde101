---
title: START and END
description: Virtual graph markers that identify entry and terminal routes.
contentType: glossary
level: Beginner
minutes: 3
topics: [LangGraph, START, END]
lastVerified: 2026-08-15
sidebar:
  order: 8
sources:
  - title: Graph API overview — START and END
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**`START` and `END` are virtual markers, not business functions.** `START` routes graph input to the first node. `END` marks a completed path.[^start-end]

## Tiny example

```python
from langgraph.graph import START, END

builder.add_edge(START, "load_order")
builder.add_edge("send_reply", END)
```

| Marker | Read it as |
| --- | --- |
| `START` | “When input arrives…” |
| `END` | “…this path is finished.” |

You can also add a conditional edge from `START` when different inputs need different entry nodes.

## Failure note

Reaching `END` stops routing; it does not prove that an external side effect succeeded. Record and verify the outcome inside the node that owns the side effect.

## Related

- [Edges](../edges/)
- [Conditional edges](../conditional-edges/)
- [`compile()`](../compile/)

[^start-end]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#start-node).
