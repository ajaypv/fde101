---
title: Nodes
description: Small synchronous or asynchronous Python functions that read state and return updates.
contentType: glossary
level: Beginner
minutes: 4
topics: [LangGraph, nodes, state]
lastVerified: 2026-08-15
sidebar:
  order: 5
sources:
  - title: Graph API overview — Nodes
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
  - title: Thinking in LangGraph
    url: https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph
    publisher: LangChain
    type: official-doc
---

**A node is a Python function that owns one unit of work.** It reads state and returns an update. The function may be synchronous or asynchronous.[^graph-api]

## Tiny example

```python
def classify_ticket(state: TicketState) -> dict:
    urgent = "production" in state["message"].lower()
    return {"priority": "high" if urgent else "normal"}

builder.add_node("classify_ticket", classify_ticket)
```

Good node boundaries match failure boundaries:

1. Read one input.
2. Perform one understandable operation.
3. Return a small update.

## Failure note

If the last operation in a large node fails, the node attempt may run again from its beginning. Separate external services into separate nodes, and make writes idempotent.[^thinking]

## Related

- [Edges](../edges/)
- [`RetryPolicy`](../retries-tool-failures/)
- [Async waiting and timeouts](../async-waiting-timeouts/)

[^graph-api]: LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api#nodes).
[^thinking]: LangChain, [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph).
