---
title: Checkpoints and thread_id
description: Persisted state snapshots grouped under one conversation or job identifier.
contentType: glossary
level: Intermediate
minutes: 5
topics: [LangGraph, checkpoints, thread_id, persistence]
lastVerified: 2026-08-15
sidebar:
  order: 15
sources:
  - title: Persistence
    url: https://docs.langchain.com/oss/python/langgraph/persistence
    publisher: LangChain
    type: official-doc
---

**A checkpointer saves graph state at step boundaries. `thread_id` tells it which sequence of checkpoints belongs to this conversation or job.**[^persistence]

## Tiny example

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "tenant-7:case-104"}}

graph.invoke({"messages": [{"role": "user", "content": "Check case 104"}]}, config)
snapshot = graph.get_state(config)
```

| Term | Scope | Example |
| --- | --- | --- |
| State | Current data | messages and case status |
| Checkpoint | One saved snapshot | state after policy lookup |
| Thread | Ordered checkpoint history | all work for case 104 |
| Store | Data shared outside one thread | a user's saved preference |

## Failure note

`InMemorySaver` loses data when the process stops; use a persistent checkpointer in production. Never let two tenants share a `thread_id`, and apply retention rules because checkpoint histories grow.

## Related

- [Durability modes](../durability/)
- [Interrupt and resume](../interrupts-resume/)
- [State schema](../state-schema/)

[^persistence]: LangChain, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
