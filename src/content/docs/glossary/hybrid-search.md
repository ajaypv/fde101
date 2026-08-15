---
title: Hybrid search
description: Retrieval that combines semantic vector search with keyword or lexical search.
contentType: glossary
level: Intermediate
minutes: 4
topics: [hybrid search, semantic search, keyword search]
lastVerified: 2026-08-15
sidebar:
  order: 9
---

**Hybrid search** combines two signals: semantic similarity from embeddings and lexical relevance from matching words or terms.

## Tiny example

For “ERR-1047 session reset,” keyword search protects the exact error code while semantic search finds passages about interrupted sessions. A fusion step merges the two ranked lists.

```text
query → keyword results ─┐
                         ├→ rank fusion → candidates
query → vector results  ─┘
```

## FDE note

The combination method matters. Score scales from two retrievers may not be directly comparable, so rank-based fusion is often a practical baseline. Evaluate hybrid search by query type; it should earn its added complexity.
