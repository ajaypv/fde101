---
title: HNSW
description: A graph-based algorithm for fast approximate nearest-neighbor search.
contentType: glossary
level: Intermediate
minutes: 4
topics: [HNSW, vector search, retrieval]
lastVerified: 2026-08-15
sidebar:
  order: 6
---

**HNSW** means **Hierarchical Navigable Small World**. It builds layers of links between nearby vectors so a search can move quickly from a broad neighborhood to close candidates.

## Tiny example

Instead of comparing a query with every one of a million embeddings, HNSW follows promising graph links and examines a much smaller set. The result is fast, but approximate: the exact nearest item can sometimes be missed.

## What to tune

- More search effort usually improves recall and increases latency.
- A denser index can improve search quality and increase memory and build cost.
- Metadata filtering can change the effective search space.

## FDE note

HNSW is an indexing algorithm, not a vector database. Measure the latency–recall tradeoff on the customer's corpus instead of selecting defaults from a generic benchmark.
