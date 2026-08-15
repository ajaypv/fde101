---
title: Retries, backoff, await, and sleep
description: Retry transient model or tool failures after a bounded delay without repeating unsafe work.
contentType: lesson
level: Intermediate
minutes: 8
topics: [LangChain, retries, backoff, Python async]
lastVerified: 2026-08-15
sidebar:
  order: 14
sources:
  - title: Runnable.with_retry
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_retry
    publisher: LangChain
    type: official-doc
  - title: Prebuilt middleware - tool retry
    url: https://docs.langchain.com/oss/python/langchain/middleware/built-in#tool-retry
    publisher: LangChain
    type: official-doc
---

A **retry** runs a failed operation again. **Backoff** increases the wait between attempts. **Jitter** adds randomness so many workers do not retry at the same instant.

## First choose the boundary

```text
model/tool call fails
        ↓
is the error transient? ── no ──→ fail or correct the input
        │ yes
        ↓
wait with backoff + jitter → try the same small operation again
        ↓
attempt limit reached? ── yes ──→ controlled error or fallback
```

## Runnable retry

```python
safe_lookup = lookup_runnable.with_retry(
    retry_if_exception_type=(TimeoutError, ConnectionError),
    stop_after_attempt=3,       # total attempts, not retries after the first
    wait_exponential_jitter=True,
)
result = await safe_lookup.ainvoke("order-A-19")
```

Scope `with_retry()` to the network call likely to fail. Its defaults retry broad `Exception` types, so narrow them for production code.

## Agent tool retry

```python
from langchain.agents.middleware import ToolRetryMiddleware

retry_tools = ToolRetryMiddleware(
    tools=["search_orders"],
    retry_on=(TimeoutError, ConnectionError),
    max_retries=2,              # retries after the initial call
    initial_delay=1.0,
    backoff_factor=2.0,
    max_delay=8.0,
    jitter=True,
    on_failure="continue",
)
```

`ToolRetryMiddleware` waits for you. You do not add `sleep()` around it.

## Where await and sleep fit

```python
import asyncio

async def manual_retry():
    for attempt in range(3):
        try:
            return await call_external_api()  # wait for this attempt
        except TimeoutError:
            if attempt == 2:
                raise
            await asyncio.sleep(2 ** attempt)  # wait before next attempt
```

`await` and `asyncio.sleep()` are Python features, not LangChain retry keywords. `asyncio.sleep()` yields control to the event loop; `time.sleep()` blocks its current thread.

## Failure note

Do not retry invalid arguments, denied access, or a non-idempotent side effect without an idempotency key and result check. A timed-out “send payment” may have succeeded even though its response was lost.

## Related

[`invoke` and `ainvoke`](../invoke-ainvoke/) · [Middleware](../middleware/) · [Tool calling](../tool-calling/)
