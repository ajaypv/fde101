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
sources:
  - title: Efficient and robust approximate nearest neighbor search using HNSW
    url: https://arxiv.org/abs/1603.09320
    publisher: arXiv
    type: paper
  - title: pgvector
    url: https://github.com/pgvector/pgvector
    publisher: pgvector
    type: official-doc
---

**HNSW** means **Hierarchical Navigable Small World**. It builds layers of links between nearby vectors so a search can move quickly from a broad neighborhood to close candidates.

## Tiny example

Instead of comparing a query with every one of a million embeddings, HNSW follows promising graph links and examines a much smaller set. The result is fast, but approximate: the exact nearest item can sometimes be missed.

## What to tune

- More search effort—often `ef_search`—usually improves ANN recall and increases latency.
- More neighbors per node—often `M`—can improve graph reachability and increase memory.
- More construction effort—often `ef_construction`—can improve index quality and increase build time.
- Metadata filtering can change the effective search space.

The names and behavior are implementation-specific. HNSW often scales much better than a full scan, but “always O(log n)” and “visits a few hundred vectors” are not production guarantees.

## FDE note

HNSW is an approximate indexing algorithm, not a vector database. Compare its top `k` with exact search, then measure ANN recall, latency, memory, and filtered queries on the customer's corpus. See [vector search, from cosine to HNSW](../../rag/vector-search-foundations/).
