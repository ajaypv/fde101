---
title: compile()
description: The step that validates a graph definition and creates the runnable graph.
contentType: glossary
level: Beginner
minutes: 3
topics: [LangGraph, compile, checkpointer]
lastVerified: 2026-08-15
sidebar:
  order: 9
sources:
  - title: Graph API overview — Compiling your graph
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**`compile()` turns a `StateGraph` definition into a runnable graph.** Compilation performs structural checks and accepts runtime features such as a checkpointer or static breakpoints.[^compile]

## Tiny example

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
result = graph.invoke(
    {"order_id": "A-104", "status": "new"},
    {"configurable": {"thread_id": "order-A-104"}},
)
```

1. Build nodes and edges.
2. Compile once.
3. Invoke the compiled graph many times with different inputs.

## Failure note

Compilation checks graph structure; it does not call every API or prove every route works. Test success, failure, loop termination, and resume paths separately.

## Related

- [StateGraph](../stategraph/)
- [Checkpoints and threads](../checkpoints-threads/)
- [`invoke()` and `ainvoke()`](../invoke-ainvoke/)

[^compile]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#compiling-your-graph).
