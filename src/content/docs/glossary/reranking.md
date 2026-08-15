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
sources:
  - title: Rerank overview
    url: https://docs.cohere.com/docs/rerank-overview
    publisher: Cohere
    type: official-doc
---

**Reranking** applies a more precise scoring method to a small set of retrieved candidates, then reorders them before context is assembled.[^rerank]

## Tiny example

A fast retriever finds 20 passages. A cross-encoder scores each query–passage pair and sends the best five to the language model.

```text
20 fast candidates → precise reranker → 5 context passages
```

## Important limit

A reranker can reorder only what the first retriever found. It cannot recover a relevant passage missing from the candidate set.

## FDE note

Measure end-to-end answer quality and latency. Better ranking metrics are useful only if the added model call improves the customer outcome within the response-time budget.

[^rerank]: Cohere's [Rerank overview](https://docs.cohere.com/docs/rerank-overview) describes the query-plus-documents interface and returned relevance ordering. Other providers may implement the same pattern differently.
