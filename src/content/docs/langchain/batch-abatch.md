---
title: batch and abatch
description: Run a list of independent inputs while controlling concurrency and per-item failures.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, batch, concurrency]
lastVerified: 2026-08-15
sidebar:
  order: 7
sources:
  - title: Runnable.batch
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/batch
    publisher: LangChain
    type: official-doc
  - title: Models - batch
    url: https://docs.langchain.com/oss/python/langchain/models#batch
    publisher: LangChain
    type: official-doc
---

`batch()` and `abatch()` apply one Runnable to several independent inputs. The base `batch()` uses a thread pool; the base `abatch()` uses `asyncio.gather`. An integration may override them with a provider-native batch operation.

## Tiny example

```python
tickets = ["INC-101", "INC-102", "INC-103"]

results = await model.abatch(
    [f"Classify {ticket}" for ticket in tickets],
    config={"max_concurrency": 3},
    return_exceptions=True,
)

for ticket, result in zip(tickets, results):
    print(ticket, result)
```

## Remember the flow

1. Use independent inputs.
2. Set `max_concurrency` to protect the provider and your own service.
3. Match outputs to inputs by position, or use an “as completed” method and its returned index.
4. Decide whether one error stops the batch or is returned beside other results.

## Failure note

Batching is not automatically a provider's discounted offline batch API. It can simply make concurrent client calls. Unbounded concurrency can trigger `429` responses, exhaust sockets, and amplify retries.

## Related

[`invoke` and `ainvoke`](../invoke-ainvoke/) · [`RunnableConfig`](../runnable-config/) · [Retries and backoff](../retries-backoff/)
