---
title: Command
description: A LangGraph value for updating state and choosing a route together, or resuming an interrupt.
contentType: glossary
level: Intermediate
minutes: 4
topics: [LangGraph, Command, routing, resume]
lastVerified: 2026-08-15
sidebar:
  order: 12
sources:
  - title: Graph API overview — Command
    url: https://docs.langchain.com/oss/python/langgraph/graph-api
    publisher: LangChain
    type: official-doc
---

**A node returns `Command` when it must update state and choose the next node in one decision.** `Command(resume=...)` is also the input used to resume an interrupt.[^command]

## Tiny example

```python
from typing import Literal
from langgraph.types import Command

def decide(state: RefundState) -> Command[Literal["approve", "review"]]:
    next_node = "approve" if state["eligible"] else "review"
    return Command(
        update={"decision_recorded": True},
        goto=next_node,
    )
```

| Field | Meaning |
| --- | --- |
| `update` | State changes from this node |
| `goto` | Next node or nodes |
| `resume` | Value returned by a paused `interrupt()` |
| `graph=Command.PARENT` | Route from a subgraph to its parent |

## Failure note

Do not combine `goto` with a normal outgoing edge unless both destinations should execute. `Command(resume=...)` is input for a paused graph; normal new input should remain a plain state dictionary.

## Related

- [Conditional edges](../conditional-edges/)
- [Interrupt and resume](../interrupts-resume/)
- [Subgraphs](../subgraphs/)

[^command]: LangChain, [Graph API overview — Command](https://docs.langchain.com/oss/python/langgraph/graph-api#command).
