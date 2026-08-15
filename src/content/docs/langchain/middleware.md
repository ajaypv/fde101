---
title: Middleware
description: Add controls around an agent's model calls, tool calls, and lifecycle without rewriting its loop.
contentType: lesson
level: Intermediate
minutes: 6
topics: [LangChain, middleware, agents]
lastVerified: 2026-08-15
sidebar:
  order: 13
sources:
  - title: Middleware overview
    url: https://docs.langchain.com/oss/python/langchain/middleware/overview
    publisher: LangChain
    type: official-doc
  - title: Custom middleware
    url: https://docs.langchain.com/oss/python/langchain/middleware/custom
    publisher: LangChain
    type: official-doc
---

**Middleware** hooks into an agent before, after, or around model and tool calls. Use it for cross-cutting behavior such as logging, limits, redaction, retries, fallbacks, and human approval.

## Tiny example

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[search_orders],
    middleware=[
        ToolCallLimitMiddleware(tool_name="search_orders", run_limit=3),
    ],
)
```

## Hook mental model

| Hook style | Use it for |
| --- | --- |
| `before_*` | Validate or add state before a step |
| `after_*` | Inspect a result or record state |
| `wrap_*` | Control whether the wrapped call runs zero, one, or several times |

Middleware hooks run inside the compiled LangGraph returned by `create_agent()`; middleware is not a second runtime.

## Failure note

Order matters when middleware wraps other middleware. Retrying outside a handler that performs a side effect can repeat that side effect. Test the actual order and keep authorization in the tool or service that owns the data.

## Related

[`create_agent`](../create-agent/) · [Retries and backoff](../retries-backoff/) · [Callbacks and tracing](../callbacks-tracing/)
