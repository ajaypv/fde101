---
title: LangChain
description: Understand where LangChain helps, what its core abstractions mean, and when plain application code is enough.
contentType: lesson
level: Beginner
minutes: 10
topics: [LangChain, models, tools, retrieval]
lastVerified: 2026-08-15
sources:
  - title: LangChain overview
    url: https://docs.langchain.com/oss/python/langchain/overview
    publisher: LangChain
    type: official-doc
---

LangChain is an application framework that gives common interfaces to models, tools, messages, retrieval, middleware, and agents.[^overview]

## The useful mental model

Treat it as integration code you can inspect, replace, and test—not as the architecture itself.

| Building block | Plain meaning |
| --- | --- |
| Model | The text or multimodal model being called |
| Message | A structured turn: system, user, assistant, or tool |
| Tool | A function the model may request |
| Retriever | A component that returns documents for a query |
| Middleware | Logic around model or tool calls, such as limits or logging |
| Agent | A loop that lets a model decide which action to take next |

## LangChain or plain code?

Use plain provider SDK calls when the workflow is one or two stable calls and the abstraction would hide more than it helps. LangChain becomes useful when shared interfaces, tools, structured messages, retrieval integrations, or middleware remove repeated glue.

## LangChain or LangGraph?

| Need | Better starting point |
| --- | --- |
| A direct model call or simple tool-using agent | LangChain |
| Explicit workflow state and branches | LangGraph |
| Durable checkpoints and resumable execution | LangGraph |
| A few composable model/retriever integrations | LangChain |

The two are complementary. Current LangChain agents use LangGraph for orchestration, while LangGraph remains available for lower-level workflows.[^overview]

## FDE questions

- Can operators see the actual model input, tool arguments, and retrieved evidence?
- Which framework abstraction is part of your contract, and which is replaceable?
- What timeouts, retries, and access checks wrap each external call?
- Can the core business rule be tested without calling a model?

[^overview]: [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview), official documentation.
