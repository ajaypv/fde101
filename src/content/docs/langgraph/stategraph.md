---
title: StateGraph
description: The builder used to define a LangGraph workflow around a shared state schema.
contentType: glossary
level: Beginner
minutes: 3
topics: [LangGraph, StateGraph, graph]
lastVerified: 2026-08-15
sidebar:
  order: 2
sources:
  - title: Graph API overview
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**`StateGraph` is the builder that holds a state schema, named nodes, and edges.** It describes the workflow; `compile()` turns that description into something you can run.[^graph-api]

## Tiny example

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

class OrderState(TypedDict):
    order_id: str
    status: str

builder = StateGraph(OrderState)
```

Think of `builder` as a whiteboard. You still need to add work and routes.

| Object | Job |
| --- | --- |
| `StateGraph(OrderState)` | Starts the definition |
| `builder.add_node(...)` | Registers work |
| `builder.add_edge(...)` | Registers routing |
| `builder.compile()` | Produces the runnable graph |

## Failure note

Creating `StateGraph` does not call a model, save state, or run anything. Do not confuse the builder with the compiled graph.

## Related

- [State schema](../state-schema/)
- [Nodes](../nodes/)
- [`compile()`](../compile/)

[^graph-api]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api).
