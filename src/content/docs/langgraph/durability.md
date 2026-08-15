---
title: Durability modes
description: Controls for when graph checkpoint writes complete relative to the next step.
contentType: glossary
level: Advanced
minutes: 5
topics: [LangGraph, durability, checkpoints]
lastVerified: 2026-08-15
sidebar:
  order: 16
sources:
  - title: Durability API reference
    url: https://reference.langchain.com/python/langgraph/types/Durability
    publisher: LangChain
    type: official-doc
  - title: Pregel invoke API reference
    url: https://reference.langchain.com/python/langgraph/pregel/main/Pregel/invoke
    publisher: LangChain
    type: official-doc
---

**Durability controls when checkpoint writes finish relative to graph execution.** It matters only when the graph has a checkpointer.[^durability]

## Three choices

| Mode | When persistence happens | Trade-off |
| --- | --- | --- |
| `"sync"` | Finish the write before the next step starts | Strongest boundary, more latency |
| `"async"` | Write while the next step runs | Default; lower latency, small crash window |
| `"exit"` | Persist only when the graph exits | Fastest intermediate steps, no intermediate recovery point |

## Tiny example

```python
result = graph.invoke(
    {"case_id": "104"},
    config={"configurable": {"thread_id": "case-104"}},
    durability="sync",
)
```

Use `sync` when the next step must never start before the previous checkpoint is stored. Use `exit` only when replaying the whole run is acceptable.

## Failure note

Durability does not make external effects transactional. A checkpoint and a payment API are two separate systems; use an idempotency key and verify the remote result on retry.

## Related

- [Checkpoints and threads](../checkpoints-threads/)
- [`RetryPolicy` and tool failures](../retries-tool-failures/)
- [Interrupt and resume](../interrupts-resume/)

[^durability]: LangChain, [`Durability` reference](https://reference.langchain.com/python/langgraph/types/Durability) and [`invoke` reference](https://reference.langchain.com/python/langgraph/pregel/main/Pregel/invoke).
