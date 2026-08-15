---
title: Send and parallel fan-out
description: Dynamic dispatch that runs one node several times with separate inputs.
contentType: glossary
level: Intermediate
minutes: 5
topics: [LangGraph, Send, parallel, map-reduce]
lastVerified: 2026-08-15
sidebar:
  order: 13
sources:
  - title: Use the graph API — Map-reduce and the Send API
    url: https://docs.langchain.com/oss/python/langgraph/use-graph-api
    publisher: LangChain
    type: official-doc
---

**`Send` creates a dynamic call to a node with its own input.** Return several `Send` objects to fan work out in parallel, then merge results through a reducer.[^send]

## Tiny example

```python
import operator
from typing import Annotated
from langgraph.types import Send

class ResearchState(TypedDict):
    urls: list[str]
    summaries: Annotated[list[str], operator.add]

def fan_out(state: ResearchState):
    return [Send("summarize", {"url": url}) for url in state["urls"]]

def summarize(state: dict) -> dict:
    return {"summaries": [fetch_summary(state["url"])]}
```

1. Router sees three URLs.
2. It returns three `Send("summarize", ...)` values.
3. Three node calls run concurrently.
4. The reducer combines their summaries.

## Failure note

Cap fan-out and invocation concurrency. Parallel calls can overload an API, and results should not rely on completion order. Side-effecting workers need idempotency keys.

## Related

- [Reducers](../reducers/)
- [Edges](../edges/)
- [Async waiting and timeouts](../async-waiting-timeouts/)

[^send]: LangChain, [Use the graph API — Map-reduce and the Send API](https://docs.langchain.com/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api).
