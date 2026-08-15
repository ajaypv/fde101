---
title: Recall@k
description: The share of all known relevant results found among the top retrieved results.
contentType: glossary
level: Beginner
minutes: 3
topics: [recall, retrieval, evaluation]
lastVerified: 2026-08-15
sidebar:
  order: 5
---

**Recall@k** asks: of everything known to be relevant, how much appeared in the first `k` results?

## Tiny example

Two passages are labeled relevant. The top five results contain one of them.

```text
Recall@5 = 1 relevant result found / 2 known relevant results = 0.50
```

High recall gives the model a better chance of seeing all the necessary evidence. It does not guarantee that the top results are clean or well ordered.

## FDE note

Recall needs a trustworthy set of relevance labels. A single “gold passage” per question can make the denominator misleading. Read it beside [Precision@k](../precision-at-k/), not in isolation.
