---
title: stream() and astream()
description: Interfaces for observing graph updates, values, messages, or custom events as work runs.
contentType: glossary
level: Intermediate
minutes: 4
topics: [LangGraph, stream, astream]
lastVerified: 2026-08-15
sidebar:
  order: 11
sources:
  - title: Streaming
    url: https://docs.langchain.com/oss/python/langgraph/streaming
    publisher: LangChain
    type: official-doc
---

**`stream()` and `astream()` expose progress before the final result is ready.** Pick a stream mode based on what the client needs.[^streaming]

## Tiny example

```python
for part in graph.stream(
    {"question": "Check order A-104"},
    stream_mode="updates",
    version="v2",
):
    if part["type"] == "updates":
        print(part["data"])
```

| Mode | What it exposes |
| --- | --- |
| `updates` | Node name and its state update |
| `values` | Full state after a step |
| `messages` | LLM message/token chunks with metadata |
| `custom` | Application-defined progress events |

Use `async for part in graph.astream(...)` in an async application.

## Failure note

Streaming is an observation interface, not a checkpoint. A client seeing an update does not by itself mean the update is durably stored. Configure a checkpointer and durability mode separately.

## Related

- [`invoke()` and `ainvoke()`](../invoke-ainvoke/)
- [Durability modes](../durability/)
- [Subgraphs](../subgraphs/)

[^streaming]: LangChain, [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming).
