---
title: invoke and ainvoke
description: Choose the synchronous or asynchronous interface for one Runnable input.
contentType: lesson
level: Beginner
minutes: 4
topics: [LangChain, Python, async]
lastVerified: 2026-08-15
sidebar:
  order: 6
sources:
  - title: Runnable
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable
    publisher: LangChain
    type: official-doc
  - title: Runnable.ainvoke
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/ainvoke
    publisher: LangChain
    type: official-doc
---

`invoke(input)` blocks the current Python thread until one result is ready. `await ainvoke(input)` lets an async application yield control while it waits.

## Tiny example

```python
# A command-line script
reply = model.invoke("Summarize incident INC-104")

# An async FastAPI route or worker
async def summarize(ticket: str):
    reply = await model.ainvoke(f"Summarize {ticket}")
    return {"summary": reply.text}
```

`await` is Python syntax. It does not mean “retry,” “sleep,” or “run in parallel.” The base `Runnable` async implementation may call synchronous code in a thread pool; a subclass can provide native async behavior.

## Failure note

Calling `invoke()` inside an async web handler can block its event-loop thread. Calling `ainvoke()` does not remove provider rate limits, connection limits, or the need for a timeout.

## Related

[Chat models](../chat-models/) · [`batch` and `abatch`](../batch-abatch/) · [Retries and backoff](../retries-backoff/)
