---
title: Callbacks and tracing
description: Record the nested model, tool, retriever, and chain work behind one user request.
contentType: lesson
level: Intermediate
minutes: 6
topics: [LangChain, callbacks, LangSmith, tracing]
lastVerified: 2026-08-15
sidebar:
  order: 19
sources:
  - title: Trace LangChain applications
    url: https://docs.langchain.com/langsmith/trace-with-langchain
    publisher: LangChain
    type: official-doc
  - title: Observability concepts
    url: https://docs.langchain.com/langsmith/observability-concepts
    publisher: LangChain
    type: official-doc
---

A **callback** receives lifecycle events from LangChain runs. A **trace** groups the nested runs for one operation so you can inspect inputs, outputs, timing, errors, and metadata. LangSmith is LangChain's tracing service.

## Tiny example

```python
# Set LANGSMITH_TRACING=true and LANGSMITH_API_KEY in the environment.
result = chain.invoke(
    {"ticket": "INC-104"},
    config={
        "run_name": "support_summary",
        "tags": ["production"],
        "metadata": {"release": "2026.08.15"},
    },
)
```

## Read a trace in this order

1. Find the failed or slow user request.
2. Open its nested model, retriever, and tool runs.
3. Compare the actual input with the expected input.
4. Check latency, token usage, retrieved document IDs, and errors.
5. Turn a repeated failure into an evaluation case or alert.

## Failure note

Tracing can capture prompts, tool arguments, retrieved text, and model output. Redact secrets and personal data, configure retention and access, and avoid putting sensitive values in tags or metadata. A trace explains what happened; it does not prove the answer was correct.

## Related

[`RunnableConfig`](../runnable-config/) · [Middleware](../middleware/) · [LLMOps](../../llmops/)
