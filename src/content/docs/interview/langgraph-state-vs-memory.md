---
title: LangGraph state vs memory
description: A concise interview answer distinguishing graph state, checkpoints, threads, and cross-thread memory.
contentType: interview
level: Intermediate
minutes: 4
topics: [LangGraph, state, memory, interview]
lastVerified: 2026-08-15
sidebar:
  order: 2
sources:
  - title: LangGraph persistence
    url: https://docs.langchain.com/oss/python/langgraph/persistence
    publisher: LangChain
    type: official-doc
---

## Short answer

**State** is the data a graph run reads and updates. A **checkpoint** is a saved state snapshot. A **thread** groups the checkpoints for one ongoing conversation or job. A **store** can hold information that needs to be shared across threads.[^persistence]

## Tiny example

For a support conversation:

```text
state      = current messages, selected account, proposed action
checkpoint = state after the user confirms the account
thread     = support conversation 9f21
store      = the user's saved communication preference
```

Calling all four “memory” hides important lifecycle and security decisions.

## Strong follow-up

Explain that persistence requires product choices: retention, encryption, tenant isolation, deletion, and what may be used in future threads. Checkpointing execution does not grant permission to retain everything indefinitely.

[^persistence]: [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), official documentation.
