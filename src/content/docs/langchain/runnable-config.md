---
title: RunnableConfig
description: Pass tracing labels, callbacks, concurrency limits, and runtime configuration alongside an input.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, RunnableConfig, tracing]
lastVerified: 2026-08-15
sidebar:
  order: 9
sources:
  - title: RunnableConfig
    url: https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig
    publisher: LangChain
    type: official-doc
  - title: Trace LangChain applications
    url: https://docs.langchain.com/langsmith/trace-with-langchain
    publisher: LangChain
    type: official-doc
---

`RunnableConfig` is the optional configuration dictionary passed beside a Runnable's business input. Common keys include `tags`, `metadata`, `callbacks`, `run_name`, `max_concurrency`, `recursion_limit`, and `configurable`.

## Tiny example

```python
config = {
    "run_name": "classify_support_ticket",
    "tags": ["support", "production"],
    "metadata": {"release": "2026.08.15"},
    "max_concurrency": 4,
}

result = chain.invoke({"ticket": "INC-104"}, config=config)
```

Keep the two channels distinct:

| Channel | Example | Meaning |
| --- | --- | --- |
| Input | `{"ticket": "INC-104"}` | Data the Runnable processes |
| Config | `{"tags": ["support"]}` | How this run executes or is observed |

## Failure note

Tags and metadata can be inherited by child Runnables and sent to tracing systems. Do not place API keys, raw personal data, or authorization decisions in tracing metadata. The `configurable` field only affects attributes explicitly exposed as configurable.

## Related

[Runnables and LCEL](../runnables-lcel/) · [`batch` and `abatch`](../batch-abatch/) · [Callbacks and tracing](../callbacks-tracing/)
