---
title: Reducers and Annotated
description: Rules that tell LangGraph how to combine updates to the same state key.
contentType: glossary
level: Intermediate
minutes: 4
topics: [LangGraph, reducers, Annotated, state]
lastVerified: 2026-08-15
sidebar:
  order: 4
sources:
  - title: Use the graph API — Process state updates with reducers
    url: https://docs.langchain.com/oss/python/langgraph/use-graph-api
    publisher: LangChain
    type: official-doc
---

**A reducer decides how an old state value and a new update become one value.** Without a reducer, a new update replaces the old value.[^reducers]

## Tiny example

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict

class ResearchState(TypedDict):
    question: str
    findings: Annotated[list[str], operator.add]

def search_policy(state: ResearchState) -> dict:
    return {"findings": ["Refund window is 30 days"]}
```

`Annotated[list[str], operator.add]` means “append this update to the existing list.”

| Update | No reducer | `operator.add` reducer |
| --- | --- | --- |
| old `['A']`, new `['B']` | `['B']` | `['A', 'B']` |

## Failure note

Parallel nodes that update the same key need a merge rule. Choose a deterministic reducer and do not assume parallel results arrive in a business-significant order.

## Related

- [State schema](../state-schema/)
- [`Send` and fan-out](../send-parallel-fanout/)
- [Edges](../edges/)

[^reducers]: LangChain, [Use the graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api#process-state-updates-with-reducers).
