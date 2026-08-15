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
---

**Precision@k** asks: of the first `k` results the retriever returned, how many were relevant?

## Tiny example

A search returns three passages. One answers the question and two do not.

```text
Precision@3 = 1 relevant result / 3 results = 0.33
```

High precision keeps distracting evidence out of the model's context. It does not tell you whether the retriever missed other relevant passages.

## FDE note

Always state `k`, the relevance-labeling method, and how ties or duplicate passages are handled. Compare precision with [Recall@k](../recall-at-k/); optimizing only one can hide a weak retrieval system.
