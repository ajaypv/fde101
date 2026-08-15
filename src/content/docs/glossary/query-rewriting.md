---
title: Query rewriting
description: Transforming a user's question into search-friendly wording while preserving the original intent.
contentType: glossary
level: Intermediate
minutes: 4
topics: [query rewriting, retrieval, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 25
sources:
  - title: Rewrite queries with semantic ranker
    url: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-rewrite
    publisher: Microsoft
    type: official-doc
---

**Query rewriting** transforms a user's question into wording that a search system may retrieve more effectively. A rewrite may add corpus terminology, correct spelling, resolve conversation references, or create several focused queries.

## Tiny example

```text
User:     Can I send it back after two weeks?
Rewrite:  return policy after 14 days
```

The rewrite matches likely policy language. It might also lose an exact order ID or misunderstand what “it” means.

## Safe pattern

Search with the original query and one or more rewrites, record each version, and compare retrieval quality with and without rewriting. Microsoft's query-rewrite documentation follows this original-plus-rewrites pattern and warns about losing exact terms such as product codes.[^rewrite]

## FDE note

Rewriting adds another fallible model operation, latency, and cost. Use it for a measured query-understanding problem, not as a mandatory RAG stage.

[^rewrite]: Microsoft, [query rewriting in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-rewrite). The documented API is vendor-specific and currently preview.
