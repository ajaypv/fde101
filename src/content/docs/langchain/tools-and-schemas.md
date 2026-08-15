---
title: Tools and schemas
description: Expose a narrow Python function with a name, description, and typed arguments a model can request.
contentType: lesson
level: Beginner
minutes: 5
topics: [LangChain, tools, schemas]
lastVerified: 2026-08-15
sidebar:
  order: 10
sources:
  - title: Tools
    url: https://docs.langchain.com/oss/python/langchain/tools
    publisher: LangChain
    type: official-doc
---

A LangChain **tool** pairs executable code with a schema. The model sees the tool's name, description, and arguments; your application executes the function.

## Tiny example

```python
from langchain.tools import tool

@tool
def get_order_status(order_id: str) -> str:
    """Return the shipping status for one order the caller may access."""
    return order_service.lookup(order_id)
```

Type hints define the input schema. The docstring helps the model decide when the tool applies.

## A useful tool contract

1. **Narrow name:** `get_order_status`, not `do_everything`.
2. **Clear description:** say when to use it and what it returns.
3. **Typed arguments:** reject missing or malformed input early.
4. **Application checks:** authenticate the caller and authorize the specific record.
5. **Small output:** return what the next step needs, not an entire database row.

## Failure note

Schema validation is not authorization. The model can request `order_id="someone-elses-order"`; the tool must enforce tenant and object permissions. Do not expose broad filesystem, SQL, or shell access because the description asks the model to be careful.

## Related

[Tool calling](../tool-calling/) · [`create_agent`](../create-agent/) · [Middleware](../middleware/)
