---
title: stream and astream
description: Consume model or Runnable output incrementally when every relevant component supports streaming.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, streaming, async]
lastVerified: 2026-08-15
sidebar:
  order: 8
sources:
  - title: Models - stream
    url: https://docs.langchain.com/oss/python/langchain/models#stream
    publisher: LangChain
    type: official-doc
  - title: Runnable.stream
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/stream
    publisher: LangChain
    type: official-doc
---

`stream()` returns a normal iterator. `astream()` returns an async iterator. A chat model usually yields `AIMessageChunk` objects that can be added together into one message.

## Tiny example

```python
full = None

async for chunk in model.astream("Draft a short incident update"):
    full = chunk if full is None else full + chunk
    await websocket.send_text(chunk.text)

print(full.text)
```

## Streaming is a pipeline property

1. The provider must send chunks.
2. Each middle step must preserve them.
3. The transport must flush them to the client.
4. Your application must still record the final result and failures.

The base Runnable implementation of `stream()` calls `invoke()` and the base `astream()` calls `ainvoke()`. A component must override that behavior to produce real incremental output.

## Failure note

A partial answer may already be visible when a later tool or network call fails. Design a terminal error event, cancellation handling, and UI state for incomplete output.

## Related

[`invoke` and `ainvoke`](../invoke-ainvoke/) · [Messages](../messages/) · [Callbacks and tracing](../callbacks-tracing/)
