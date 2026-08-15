---
title: Maximal marginal relevance
description: A selection rule that balances query relevance with novelty to reduce redundant results.
contentType: glossary
level: Intermediate
minutes: 4
topics: [MMR, diversity, reranking]
lastVerified: 2026-08-15
sources:
  - title: Using MMR for diversity-based reranking
    url: https://aclanthology.org/X98-1025/
    publisher: Association for Computational Linguistics
    type: paper
---

**Maximal marginal relevance**, or **MMR**, selects results by balancing relevance to the query with novelty compared with items already selected.[^mmr]

## Tiny example

Ordinary top four results may contain three copies of the same refund paragraph. MMR can keep one copy and promote the enterprise-exception passage, giving the model more varied evidence.

## What it cannot do

MMR cannot recover a passage missing from the candidate set. Too much diversity can also promote a less relevant item. It reduces redundancy; it does not verify factual accuracy.

[^mmr]: Goldstein and Carbonell, [“Using MMR for Diversity-Based Reranking”](https://aclanthology.org/X98-1025/), 1998.
