---
title: Runnables and LCEL
description: Compose small LangChain units with a shared calling interface and the pipe operator.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, Runnable, LCEL]
lastVerified: 2026-08-15
sidebar:
  order: 5
sources:
  - title: Runnable
    url: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable
    publisher: LangChain
    type: official-doc
---

A **Runnable** is a unit of work with standard methods such as `invoke`, `batch`, and `stream`. LangChain Expression Language (LCEL) composes Runnables with `|`.

## Tiny example

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Summarize ticket: {ticket}")
chain = prompt | model | StrOutputParser()

summary = chain.invoke({"ticket": "Checkout returns HTTP 503."})
```

The output of each step becomes the input of the next. A dictionary inside a sequence creates parallel branches; a `RunnableSequence` runs steps in order.

## Failure note

Composition can hide a wide retry boundary. If `prompt | model | send_email` is retried as one unit, the email step may run twice. Apply timeout, retry, and tracing configuration to the smallest risky component.

## Related

[`invoke` and `ainvoke`](../invoke-ainvoke/) · [`RunnableConfig`](../runnable-config/) · [Retries and backoff](../retries-backoff/)
