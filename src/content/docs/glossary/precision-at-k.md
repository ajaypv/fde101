---
title: Precision@k
description: The share of the top retrieved results that are relevant to the question.
contentType: glossary
level: Beginner
minutes: 3
topics: [precision, retrieval, evaluation]
lastVerified: 2026-08-15
sidebar:
  order: 4
sources:
  - title: Machine Learning Glossary — Precision@k
    url: https://developers.google.com/machine-learning/glossary/metrics
    publisher: Google for Developers
    type: official-doc
  - title: Develop a RAG solution — Information-retrieval phase
    url: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval
    publisher: Microsoft
    type: official-doc
---

**Precision@k** asks: what fraction of the first `k` results were relevant? The denominator is the requested value of `k`, not a smaller number of results that happened to be returned.[^precision]

```text
Precision@k = relevant results in the first k / k
```

## Tiny example

A search returns three passages. One answers the question and two do not.

```text
Precision@3 = 1 relevant result / 3 results = 0.33
```

High precision keeps distracting evidence out of the model's context. It does not tell you whether the retriever missed other relevant passages.

## The at-least-k convention

This book calculates Precision@k only when the retriever returned at least `k` results. If a query returns fewer results, either use a valid smaller `k` and label it clearly or record the run as incomplete. Dividing by the shorter returned list while still calling the metric Precision@k changes the denominator and makes runs harder to compare.

## FDE note

Always state `k`, the relevance-labeling method, and how ties or duplicate passages are handled. Compare precision with [Recall@k](../recall-at-k/); optimizing only one can hide a weak retrieval system.

[^precision]: Google for Developers, [Precision@k](https://developers.google.com/machine-learning/glossary/metrics). Microsoft gives the same retrieval-oriented definition in its [RAG information-retrieval guidance](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval).
