---
title: Chat models
description: Initialize and call a provider-backed chat model through LangChain's common interface.
contentType: lesson
level: Beginner
minutes: 4
topics: [LangChain, chat models, providers]
lastVerified: 2026-08-15
sidebar:
  order: 1
sources:
  - title: Models
    url: https://docs.langchain.com/oss/python/langchain/models
    publisher: LangChain
    type: official-doc
---

A **chat model** accepts messages and returns an `AIMessage`. `init_chat_model()` selects a provider integration from a model identifier; provider packages still handle credentials and provider-specific options.

## Tiny example

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    timeout=20,
    max_retries=2,
)
reply = model.invoke("Summarize ticket INC-104 in one sentence.")
print(reply.text)
```

## Remember the flow

1. Pick a provider and model.
2. Set a timeout and retry limit.
3. Send messages.
4. Read the returned `AIMessage` and usage metadata.

## Failure note

A common interface does not make models interchangeable. Tool calling, structured output, token limits, pricing, and multimodal support differ. Check the selected provider integration and evaluate the exact model version.

## Related

[Messages](../messages/) · [`invoke` and `ainvoke`](../invoke-ainvoke/) · [Structured output](../structured-output/)
