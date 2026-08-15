---
title: invoke() and ainvoke()
description: Synchronous and asynchronous ways to run a compiled graph to its final result.
contentType: glossary
level: Beginner
minutes: 4
topics: [LangGraph, invoke, ainvoke, async]
lastVerified: 2026-08-15
sidebar:
  order: 10
sources:
  - title: Use the graph API — Async
    url: https://docs.langchain.com/oss/python/langgraph/use-graph-api
    publisher: LangChain
    type: official-doc
---

**`invoke()` runs a graph synchronously; `ainvoke()` runs it through Python's async interface.** Both normally return the final state after the graph stops.[^async]

## Tiny example

```python
# Synchronous application
result = graph.invoke({"question": "Where is order A-104?"})

# Inside an async application such as FastAPI
result = await graph.ainvoke({"question": "Where is order A-104?"})
```

| Application | Normal choice |
| --- | --- |
| Simple script or sync worker | `invoke()` |
| FastAPI async route | `await graph.ainvoke(...)` |
| Need progress while running | `stream()` or `astream()` |

`await` belongs to Python. LangGraph supplies the awaitable `ainvoke()` method.

## Failure note

Use async nodes for async I/O and call the graph with `ainvoke()` or `astream()`. Do not hide blocking I/O or `time.sleep()` inside an async node; it blocks the event loop.

## Related

- [`stream()` and `astream()`](../stream-astream/)
- [Async waiting and timeouts](../async-waiting-timeouts/)
- [Nodes](../nodes/)

[^async]: LangChain, [Use the graph API — Async](https://docs.langchain.com/oss/python/langgraph/use-graph-api#async).
