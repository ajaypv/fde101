---
title: ToolNode and tools_condition
description: Prebuilt tool execution and routing for a custom LangGraph tool loop.
contentType: glossary
level: Intermediate
minutes: 6
topics: [LangGraph, ToolNode, tools_condition, tools]
lastVerified: 2026-08-15
sidebar:
  order: 14
sources:
  - title: LangChain tools — ToolNode
    url: https://docs.langchain.com/oss/python/langchain/tools
    publisher: LangChain
    type: official-doc
  - title: ToolNode API reference
    url: https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode
    publisher: LangChain
    type: official-doc
---

**`ToolNode` executes tool calls from the last AI message. `tools_condition` routes to that node when tool calls exist, or to `END` when they do not.**[^tools]

## Tiny example

```python
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode([lookup_order]))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")
```

The loop is: model proposes a call → tools execute → model reads the result → model calls again or answers.

## The default error boundary

| Event inside `ToolNode` | Default behavior |
| --- | --- |
| Model supplies invalid tool arguments | Return an error `ToolMessage` so the model can correct the call |
| Tool function raises during execution | Re-raise the exception so the graph can fail or retry |
| `handle_tool_errors=True` | Catch all tool exceptions and return error `ToolMessage` values |

## Failure note

If `handle_tool_errors=True` catches a transient execution error, the node's `RetryPolicy` never sees that exception. Choose deliberately: error message for model correction, or escaped exception for system retry. `ToolNode` can execute multiple tool calls in parallel, so every write tool must tolerate a repeated node attempt.

## Related

- [`RetryPolicy` and tool failures](../retries-tool-failures/)
- [Conditional edges](../conditional-edges/)
- [`Command`](../command/)

[^tools]: LangChain, [Tools — ToolNode](https://docs.langchain.com/oss/python/langchain/tools#toolnode) and [`ToolNode` API reference](https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode).
