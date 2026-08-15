---
title: ReAct
description: A pattern that interleaves model decisions, external actions, and observations.
contentType: glossary
level: Intermediate
minutes: 4
topics: [ReAct, agents, tools]
lastVerified: 2026-08-15
sidebar:
  order: 27
sources:
  - title: ReAct — Synergizing reasoning and acting in language models
    url: https://arxiv.org/abs/2210.03629
    publisher: arXiv
    type: paper
---

**ReAct** is an agent pattern that interleaves reasoning with actions and observations. New tool results can change what the model does next.[^react]

## Tiny example

```text
decide: current weather is needed
act:    call the weather tool
observe: rain begins at 4 PM
decide: search for a morning train
act:    call the train tool
observe: an 8 AM seat is available
answer: recommend the morning option
```

This differs from two fixed tool calls because the second action depends on the first observation.

## FDE note

Use an allowlist, argument validation, a step limit, timeouts, and an escalation path. “Think, act, repeat forever” is not a production control loop.

[^react]: Yao et al., [“ReAct: Synergizing Reasoning and Acting in Language Models”](https://arxiv.org/abs/2210.03629), ICLR 2023.
