---
title: Edges
description: Static routes that schedule which node runs after another node.
contentType: glossary
level: Beginner
minutes: 3
topics: [LangGraph, edges, routing]
lastVerified: 2026-08-15
sidebar:
  order: 6
sources:
  - title: Graph API overview — Edges
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**An edge says what runs next.** Use a normal edge when the route never changes.[^edges]

## Tiny example

```python
builder.add_edge("read_invoice", "validate_total")
builder.add_edge("validate_total", "save_result")
```

The mental model is a railway track: once `read_invoice` finishes, the track leads to `validate_total`.

| Shape | Runtime behavior |
| --- | --- |
| One outgoing edge | Run one next node |
| Several outgoing edges | Run destination nodes in parallel in the next superstep |
| Edge to `END` | Stop that path |

## Failure note

Do not add a static outgoing edge and also return a dynamic `Command(goto=...)` from the same node unless both paths should run. LangGraph can schedule both.

## Related

- [Conditional edges](../conditional-edges/)
- [`START` and `END`](../start-end/)
- [`Command`](../command/)

[^edges]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#edges).
