---
title: Fine-tuning
description: Updating a model's weights with examples or feedback to improve a defined, repeated behavior.
contentType: glossary
level: Intermediate
minutes: 4
topics: [fine-tuning, model optimization, evaluation]
lastVerified: 2026-08-15
sidebar:
  order: 30
sources:
  - title: Model optimization
    url: https://developers.openai.com/api/docs/guides/model-optimization
    publisher: OpenAI
    type: official-doc
---

**Fine-tuning** updates model weights using examples or feedback so the model performs a defined task or behavior more consistently.

## Tiny example

A support classifier repeatedly confuses two company-specific categories. You have thousands of reviewed examples, a stable label definition, and an eval set. Fine-tuning may improve that repeated decision.

## Retrieval or fine-tuning?

| Need | Better starting point |
| --- | --- |
| Current product policy | Retrieval from the governed policy source |
| Consistent JSON or house style | Schema and prompting, then fine-tuning if measured failures remain |
| New private fact for one customer | Context or retrieval |
| Stable specialized classification | Fine-tuning may fit |

OpenAI's model-optimization workflow starts with evals, improves prompts, and uses fine-tuning where the measured task benefits.[^optimization]

## FDE note

“Fine-tune last” is a useful default, not a law. Fine-tune when the behavior is stable, the data is good, and the expected quality, cost, or latency gain justifies training and maintenance.

[^optimization]: OpenAI, [model optimization](https://developers.openai.com/api/docs/guides/model-optimization).
