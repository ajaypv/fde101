---
title: Subgraphs
description: Compiled graphs used as nodes inside a larger parent workflow.
contentType: glossary
level: Advanced
minutes: 5
topics: [LangGraph, subgraphs, state]
lastVerified: 2026-08-15
sidebar:
  order: 18
sources:
  - title: Subgraphs
    url: https://docs.langchain.com/oss/python/langgraph/use-subgraphs
    publisher: LangChain
    type: official-doc
---

**A subgraph packages several nodes behind one parent-graph step.** Add the compiled subgraph directly when parent and child share state keys; use a wrapper node when their schemas differ.[^subgraphs]

## Tiny example

```python
child = (
    StateGraph(CaseState)
    .add_node("check_policy", check_policy)
    .add_edge(START, "check_policy")
    .compile()
)

parent = StateGraph(CaseState)
parent.add_node("policy_review", child)
parent.add_edge(START, "policy_review")
```

| Parent and child state | Integration |
| --- | --- |
| Share keys | Add compiled subgraph as a node |
| Different schemas | Wrapper maps parent input to child input and output back |

By default, a child compiled without a checkpointer setting inherits the parent's checkpointer for per-invocation persistence.

## Failure note

Choose subgraph persistence deliberately. Per-thread child memory can conflict when the same stateful subgraph is called more than once in one parent node. A stateless child cannot resume an interrupt.

## Related

- [State schema](../state-schema/)
- [Checkpoints and threads](../checkpoints-threads/)
- [`Command`](../command/)

[^subgraphs]: LangChain, [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs).
