---
title: Agent
description: A model-driven loop that observes state, selects actions, and continues toward an objective.
contentType: glossary
level: Intermediate
minutes: 4
topics: [agents, tools, workflows]
lastVerified: 2026-08-15
sidebar:
  order: 18
---

An **agent** is a loop in which a model can choose the next action, inspect the result, and continue toward an objective.

## Tiny example

```text
request → model chooses search → search result
        → model chooses lookup → customer record
        → model drafts answer → stop
```

The surrounding application owns the loop, state, tool execution, permissions, retries, and stopping conditions.

## What it is not

An agent is not automatically autonomous, reliable, or appropriate for every workflow. A fixed sequence is usually easier to test when the required steps are already known.

## FDE note

Bound the number of steps, expose progress, require approval for consequential actions, and make side effects safe to retry.
