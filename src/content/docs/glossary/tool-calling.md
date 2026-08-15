---
title: Tool calling
description: A structured request from a model for application code to invoke a defined capability.
contentType: glossary
level: Intermediate
minutes: 4
topics: [tool calling, agents, security]
lastVerified: 2026-08-15
sidebar:
  order: 19
---

**Tool calling** lets a model propose a named operation and structured arguments. The application decides whether and how to execute it, then returns the result to the model.

## Tiny example

```json
{
  "name": "lookup_order",
  "arguments": { "order_id": "A-1042" }
}
```

The model has requested a lookup; it has not performed one.

## FDE note

Validate arguments against a schema, authenticate the user, authorize the specific operation and resource, set timeouts, and log the result. Never rely on the model to enforce permissions or confirm that a side effect succeeded.
