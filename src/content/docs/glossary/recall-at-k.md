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
sources:
  - title: Machine Learning Glossary — Recall@k
    url: https://developers.google.com/machine-learning/glossary/metrics
    publisher: Google for Developers
    type: official-doc
  - title: Develop a RAG solution — Information-retrieval phase
    url: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval
    publisher: Microsoft
    type: official-doc
---

**Recall@k** asks: of everything known to be relevant, what fraction appeared in the first `k` results?[^recall]

```text
Recall@k = relevant results in the first k / all known relevant results
```

## Tiny example

Two passages are labeled relevant. The top five results contain one of them.

```text
Recall@5 = 1 relevant result found / 2 known relevant results = 0.50
```

High recall gives the model a better chance of seeing all the necessary evidence. It does not guarantee that the top results are clean or well ordered.

## FDE note

Recall needs a trustworthy set of relevance labels. A single “gold passage” per question can make the denominator misleading. Read it beside [Precision@k](../precision-at-k/), not in isolation.

Questions with no relevant passage have a zero denominator, so evaluate them in an unanswerable-query or abstention suite instead of silently assigning a Recall@k score.

[^recall]: Google for Developers, [Recall@k](https://developers.google.com/machine-learning/glossary/metrics). Microsoft describes the denominator as all possible relevant items in its [RAG information-retrieval guidance](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval).
