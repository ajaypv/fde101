---
title: Prompt templates
description: Turn named application data into a repeatable sequence of model messages.
contentType: lesson
level: Beginner
minutes: 4
topics: [LangChain, prompts, context]
lastVerified: 2026-08-15
sidebar:
  order: 3
sources:
  - title: ChatPromptTemplate
    url: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate
    publisher: LangChain
    type: official-doc
---

A **prompt template** formats named inputs into a prompt value. `ChatPromptTemplate` preserves message roles instead of building one large string by hand.

## Tiny example

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer only from this policy:\n{policy}"),
    ("human", "Order {order_id}: {question}"),
])

messages = prompt.invoke({
    "policy": "Returns are accepted for 30 days.",
    "order_id": "A-19",
    "question": "Can I return it after 45 days?",
})
```

## Remember the flow

1. Write stable instructions once.
2. Name each changing value.
3. Format with a dictionary.
4. Pass the result to a model or compose it with `|`.

## Failure note

Templates format text; they do not make untrusted text safe. Retrieved pages and user input can contain instructions. Keep authorization outside the prompt, mark data clearly, and test prompt-injection cases.

## Related

[Messages](../messages/) · [Runnables and LCEL](../runnables-lcel/) · [Structured output](../structured-output/)
