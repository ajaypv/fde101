---
title: Reranking
description: A second retrieval stage that scores a small candidate set more carefully.
contentType: glossary
level: Intermediate
minutes: 3
topics: [reranking, retrieval, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 10
---

**Reranking** applies a more precise scoring method to a small set of retrieved candidates, then reorders them before context is assembled.

## Tiny example

A fast retriever finds 20 passages. A cross-encoder scores each query–passage pair and sends the best five to the language model.

```text
20 fast candidates → precise reranker → 5 context passages
```

## Important limit

A reranker can reorder only what the first retriever found. It cannot recover a relevant passage missing from the candidate set.

## FDE note

Measure end-to-end answer quality and latency. Better ranking metrics are useful only if the added model call improves the customer outcome within the response-time budget.
