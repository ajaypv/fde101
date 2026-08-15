---
title: Chain or workflow
description: A predefined sequence of model, tool, and application steps controlled by code.
contentType: glossary
level: Beginner
minutes: 3
topics: [workflow, chain, agents]
lastVerified: 2026-08-15
sidebar:
  order: 26
sources:
  - title: Building effective agents
    url: https://www.anthropic.com/engineering/building-effective-agents
    publisher: Anthropic
    type: official-doc
---

A **chain** or **workflow** follows code paths defined before the request runs. A model may perform individual steps, but application code decides their order and branches.

## Tiny example

```text
invoice → extract fields → validate total → request approval → write to ERP
```

The model may extract the fields. Code still chooses the next step and blocks the write when validation or approval fails.

## Compared with an agent

| Workflow | Agent |
| --- | --- |
| Code chooses the path | Model chooses the next action |
| Predictable call count | Variable call count |
| Easier to test | More flexible for open-ended work |
| Best when steps are known | Best when findings determine the next step |

Anthropic uses this same architecture distinction and recommends adding agentic complexity only when the task needs it.[^agents]

## FDE note

A workflow can contain one bounded agentic node. Keep known policy, validation, authorization, and side effects deterministic around it.

[^agents]: Anthropic, [“Building effective agents”](https://www.anthropic.com/engineering/building-effective-agents).
