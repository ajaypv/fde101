---
title: State
description: The data a workflow needs to carry from one step to the next.
contentType: glossary
level: Intermediate
minutes: 3
topics: [state, agents, LangGraph]
lastVerified: 2026-08-15
sidebar:
  order: 21
---

**State** is the current data available to a workflow: messages, retrieved evidence, decisions, tool results, counters, or other fields needed by later steps.

## Tiny example

```json
{
  "question": "Why did deployment fail?",
  "evidence": ["log-18", "runbook-4"],
  "attempts": 1
}
```

Each node reads relevant fields and returns a controlled update rather than relying on hidden global variables.

## FDE note

Keep the schema explicit and minimal. Define merge behavior for concurrent updates, avoid storing secrets unnecessarily, and isolate state by user and tenant.
