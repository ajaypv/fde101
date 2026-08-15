---
title: Semantic search
description: Retrieval based on similarity of meaning rather than exact word overlap alone.
contentType: glossary
level: Beginner
minutes: 3
topics: [semantic search, embeddings, retrieval]
lastVerified: 2026-08-15
sidebar:
  order: 8
---

**Semantic search** retrieves text whose embedding is close to the query embedding. It can match related meaning even when the words differ.

## Tiny example

The query “I cannot log in” may retrieve a passage titled “Resetting an expired password.” The terms are different, but the meanings are related.

## Where it struggles

Exact product codes, error numbers, names, dates, and uncommon acronyms may be better served by keyword search. Similar meaning can also retrieve a plausible but wrong procedure.

## FDE note

Test with real user phrasing and real failure cases. For mixed corpora, compare semantic retrieval with [hybrid search](../hybrid-search/) rather than assuming one method wins everywhere.
