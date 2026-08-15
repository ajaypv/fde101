---
title: Choose a retrieval store without a vendor reflex
description: Compare pgvector, search engines, and vector-first databases, then reduce storage only with quality evidence.
contentType: lesson
level: Intermediate
minutes: 16
topics: [vector database, pgvector, Pinecone, Weaviate, tiered retrieval]
lastVerified: 2026-08-15
sidebar:
  order: 5
sources:
  - title: pgvector
    url: https://github.com/pgvector/pgvector
    publisher: pgvector
    type: official-doc
  - title: How full-text search works
    url: https://www.elastic.co/docs/solutions/search/full-text/how-full-text-works
    publisher: Elastic
    type: official-doc
  - title: Pinecone database architecture
    url: https://docs.pinecone.io/guides/get-started/database-architecture
    publisher: Pinecone
    type: official-doc
  - title: Weaviate vector indexes
    url: https://docs.weaviate.io/weaviate/concepts/vector-index
    publisher: Weaviate
    type: official-doc
  - title: Vector quantization
    url: https://docs.weaviate.io/weaviate/concepts/vector-quantization
    publisher: Weaviate
    type: official-doc
---

A vector database stores and searches vectors, but “use a vector database” is not a complete architecture decision. PostgreSQL, a search engine, a vector-first service, and even an in-process index can all supply vector retrieval.

## SQL search versus vector search

SQL is not “search without meaning,” and a vector store does not understand truth. These systems expose different retrieval tools:

```text
relational query → exact fields, joins, transactions, permissions
BM25 search      → rare terms, names, identifiers, error codes
vector search    → learned similarity and paraphrases
```

One product can support several of these. pgvector adds exact and approximate vector search to PostgreSQL,[^pgvector] while search engines can combine [BM25](../../glossary/bm25/) with vectors.

## Start from the system you need to operate

| Option | Sensible starting point | Trade-off to make explicit |
| --- | --- | --- |
| PostgreSQL + pgvector | Source records, joins, transactions, and ACL data already live in PostgreSQL | The team owns database capacity, index tuning, filtering behavior, replicas, backups, and vacuuming |
| Search engine with vectors | Keyword search, filters, facets, and hybrid ranking dominate | Adds search mappings, synchronization, and cluster operations |
| Pinecone | A managed vector-oriented data plane and namespaces fit the team's operating model | Adds a provider API, synchronization path, and its cost model |
| Weaviate | Built-in vector, inverted/hybrid search, filtering, and index choices fit the workload | Adds another schema, index, backup, and operational model |
| In-process exact index | A tutorial, unit test, or bounded corpus fits in one process | Limited durability, concurrency, filtering, and scale |

Pinecone documents records, namespaces, and distributed indexing as service concepts.[^pinecone] Weaviate documents flat, HNSW, and dynamic index types plus filtered search.[^weaviate] These are capabilities to test—not a ranking of vendors.

Compare options at the **same quality target** using:

- tenant isolation and permission filtering;
- update and deletion freshness;
- corpus size and filter selectivity per tenant;
- RAG recall@k and ANN recall@k at the latency SLO;
- ingest, backup, recovery, and rebuild behavior;
- operator ownership and total cost per accepted grounded answer.

Vendor benchmarks are not comparable when corpus, hardware, filters, concurrency, and recall targets differ.

## Tiered retrieval can reduce work

Suppose a company has ten million documents but only a few dozen are about yesterday's payment incident:

```text
authorize user and apply tenant/date/service filters
                         ↓
      BM25 finds exact error and deployment IDs
                         ↓
        50 candidate documents remain
                         ↓
 dense chunk search + rerank inside those candidates
                         ↓
             5 passages enter the prompt
```

This is a **coarse-to-fine** design. It can keep rarely used documents in a colder tier and cache or permanently index hot content. It can also fail badly: if the metadata or BM25 stage drops the correct document, later embeddings cannot recover it.

Measure stage-one recall separately. Creating chunk embeddings on demand moves work from ingestion to request time, so also measure cold-query latency, cache hit rate, duplicate work, and failure behavior.

## Storage reductions are experiments

| Technique | Possible benefit | What can break |
| --- | --- | --- |
| Remove duplicates and obsolete versions | Fewer vectors and less stale evidence | Bad identity rules can delete distinct content |
| Reduce chunk overlap | Less duplicated storage and context | Boundary evidence can disappear |
| Lower embedding dimensions | Smaller vectors | Retrieval quality may fall |
| Half precision or quantization | Lower memory and disk use | Compression is lossy and can reduce ANN recall |
| One summary vector per document | Much smaller coarse index | A summary can omit the one fact needed by a query |
| Partition by tenant or namespace | Smaller eligible search space | Tiny or skewed partitions complicate operations |

Quantized indexes commonly overfetch compressed candidates and rescore them with higher-precision vectors.[^quantization] Keep the optimization only if labeled recall, [MRR](../../glossary/mrr/), final answer quality, p95 latency, and cost remain acceptable.

## One decision record

Do not write “we chose Pinecone because it scales” or “we chose pgvector because it is cheaper.” Write the tested decision:

```text
At 4 million authorized chunks and 40 concurrent queries,
configuration B met recall@10 ≥ 0.92 and p95 retrieval ≤ 180 ms.
It also preserved transactional ACL updates within the required freshness window.
```

That evidence survives product fashion.

[^pgvector]: [pgvector](https://github.com/pgvector/pgvector) supports exact nearest-neighbor search plus HNSW and IVFFlat approximate indexes inside PostgreSQL.
[^pinecone]: Pinecone, [database architecture](https://docs.pinecone.io/guides/get-started/database-architecture) and [data modeling](https://docs.pinecone.io/guides/index-data/data-modeling).
[^weaviate]: Weaviate, [vector indexes](https://docs.weaviate.io/weaviate/concepts/vector-index) and [filtering](https://docs.weaviate.io/weaviate/concepts/filtering).
[^quantization]: Weaviate, [vector quantization](https://docs.weaviate.io/weaviate/concepts/vector-quantization), documents compressed indexes and rescoring with original vectors.
