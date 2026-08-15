---
title: State schema
description: The typed contract for values that nodes read and update during a graph run.
contentType: glossary
level: Beginner
minutes: 4
topics: [LangGraph, state, TypedDict]
lastVerified: 2026-08-15
sidebar:
  order: 3
sources:
  - title: Graph API overview — State
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**A state schema names the data that moves through the graph.** Every node reads the current state and normally returns only the keys it changed.[^graph-api]

## Tiny example

```python
from typing_extensions import TypedDict

class RefundState(TypedDict):
    order_id: str
    eligible: bool
    reason: str

def check_policy(state: RefundState) -> dict:
    return {"eligible": True, "reason": "Returned within 30 days"}
```

`check_policy` does not need to return `order_id`; LangGraph applies its partial update to the existing state.

| Schema choice | Use it when |
| --- | --- |
| `TypedDict` | You want a light, typed dictionary |
| `dataclass` | You need defaults and a Python object |
| Pydantic model | You need recursive input validation and accept extra overhead |

## Failure note

`TypedDict` helps type checkers; it is not runtime validation. Keep secrets and large service clients out of state. State may be serialized into checkpoints.

## Related

- [Reducers](../reducers/)
- [Checkpoints and threads](../checkpoints-threads/)
- [Nodes](../nodes/)

[^graph-api]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#state).
