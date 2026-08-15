---
title: Async waiting and timeouts
description: How Python await differs from LangGraph retries, durable pauses, and per-attempt timeouts.
contentType: glossary
level: Advanced
minutes: 8
topics: [LangGraph, async, await, asyncio, TimeoutPolicy]
lastVerified: 2026-08-15
sidebar:
  order: 20
sources:
  - title: Use the graph API — Async
    url: https://docs.langchain.com/oss/python/langgraph/use-graph-api
    publisher: LangChain
    type: official-doc
  - title: Fault tolerance — Timeouts
    url: https://docs.langchain.com/oss/python/langgraph/fault-tolerance
    publisher: LangChain
    type: official-doc
  - title: Interrupts
    url: https://docs.langchain.com/oss/python/langgraph/interrupts
    publisher: LangChain
    type: official-doc
---

**`async def`, `await`, and `asyncio.sleep()` are Python features, not LangGraph keywords.** They keep an async process responsive, but they do not create a persisted LangGraph pause.[^async]

## Pick the waiting mechanism by intent

| Need | Use | Why |
| --- | --- | --- |
| Wait for HTTP/model I/O | `await client_call()` | Releases the Python event loop while I/O is pending |
| Retry a short transient failure | `RetryPolicy` | Bounded attempts, backoff, jitter, and exception filtering |
| Stop a slow node attempt | `TimeoutPolicy` or `timeout=` | Raises `NodeTimeoutError`; retry policy then decides |
| Wait hours for a person or external signal | `interrupt()` + checkpointer | The pause is saved and can resume after a restart |
| Demonstrate latency in a test | `await asyncio.sleep(...)` | In-memory test delay only |

## Tiny example

```python
from langgraph.types import RetryPolicy, TimeoutPolicy

async def fetch_inventory(state: OrderState) -> dict:
    response = await inventory_client.get(state["sku"])
    response.raise_for_status()
    return {"stock": response.json()["stock"]}

builder.add_node(
    "fetch_inventory",
    fetch_inventory,
    timeout=TimeoutPolicy(run_timeout=5, idle_timeout=2),
    retry_policy=RetryPolicy(max_attempts=3),
)

result = await graph.ainvoke({"sku": "SKU-104"})
```

`run_timeout` caps the whole async attempt. `idle_timeout` resets when the node produces recognized progress. Current node timeouts require LangGraph 1.2 or later and apply only to async nodes.[^timeouts]

## Why manual sleep is the wrong retry

```python
# Avoid this retry pattern inside a node.
try:
    return await call_tool()
except Exception:
    await asyncio.sleep(30)
    return await call_tool()
```

It catches defects and permission errors, hides the retry from graph policy, and keeps the wait only in process memory. If the process dies, the node can restart from its boundary. Prefer an explicit retryable exception and node `RetryPolicy`.

Also avoid `time.sleep()` in an async node. It blocks the event loop, and cooperative async timeouts cannot fire until blocking work releases control. Wrap unavoidable blocking I/O with `await asyncio.to_thread(...)`.[^timeouts]

## Failure note

A timeout cancels one node attempt, clears writes from that failed attempt, and raises `NodeTimeoutError`. The retry policy can start a fresh attempt. A timeout does not prove the remote service stopped processing; writes still need idempotency keys.

## Related

- [`RetryPolicy` and tool failures](../retries-tool-failures/)
- [Interrupt and resume](../interrupts-resume/)
- [`invoke()` and `ainvoke()`](../invoke-ainvoke/)
- [Durability modes](../durability/)

[^async]: LangChain, [Use the graph API — Async](https://docs.langchain.com/oss/python/langgraph/use-graph-api#async).
[^timeouts]: LangChain, [Fault tolerance — Timeouts](https://docs.langchain.com/oss/python/langgraph/fault-tolerance#timeouts).
