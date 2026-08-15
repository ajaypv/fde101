---
title: Conditional edges
description: Routing functions that choose one or more next nodes from current state.
contentType: glossary
level: Beginner
minutes: 4
topics: [LangGraph, conditional edges, routing]
lastVerified: 2026-08-15
sidebar:
  order: 7
sources:
  - title: Graph API overview — Conditional edges
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**A conditional edge calls a routing function after a node finishes.** The function reads the updated state and returns the next node name, `END`, or a list of destinations.[^conditional]

## Tiny example

```python
from typing import Literal
from langgraph.graph import END

def route_refund(state: RefundState) -> Literal["approve", "review", END]:
    if state["policy_violation"]:
        return "review"
    if state["eligible"]:
        return "approve"
    return END

builder.add_conditional_edges("check_policy", route_refund)
```

Remember the order:

1. Node returns an update.
2. LangGraph applies the update.
3. Router reads the new state.
4. Router returns the destination.

## Failure note

Every loop needs a tested stop condition. Otherwise the graph eventually reaches its recursion limit instead of completing normally.

## Related

- [Edges](../edges/)
- [`Command`](../command/)
- [`ToolNode` and `tools_condition`](../toolnode-tools-condition/)

[^conditional]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#conditional-edges).
