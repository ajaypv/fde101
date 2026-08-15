---
title: Structured output
description: Ask a model or agent for data that matches an explicit schema instead of parsing prose.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, structured output, Pydantic]
lastVerified: 2026-08-15
sidebar:
  order: 4
sources:
  - title: Models - structured output
    url: https://docs.langchain.com/oss/python/langchain/models#structured-output
    publisher: LangChain
    type: official-doc
  - title: Structured output with agents
    url: https://docs.langchain.com/oss/python/langchain/structured-output
    publisher: LangChain
    type: official-doc
---

**Structured output** asks for a response that matches a Pydantic model, `TypedDict`, dataclass, or JSON Schema. Your code receives fields instead of scraping sentences.

## Tiny example

```python
from pydantic import BaseModel, Field

class Triage(BaseModel):
    priority: str = Field(description="low, medium, or high")
    reason: str

triage_model = model.with_structured_output(Triage)
result = triage_model.invoke("Payment failed for every customer.")
print(result.priority)
```

For an agent, pass the schema as `response_format=Triage`; the validated value appears under `result["structured_response"]`.

## Failure note

A valid object can still be wrong. Schema validation proves shape and types, not factual correctness. Provider support also differs; check whether the integration uses native structured output, tool calling, or another method.

## Related

[Chat models](../chat-models/) · [Tools and schemas](../tools-and-schemas/) · [`create_agent`](../create-agent/)
