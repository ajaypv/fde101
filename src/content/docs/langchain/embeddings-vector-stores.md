---
title: Embeddings and vector stores
description: Convert text into vectors, store them with documents, and search for semantic neighbors.
contentType: lesson
level: Beginner
minutes: 6
topics: [LangChain, embeddings, vector stores]
lastVerified: 2026-08-15
sidebar:
  order: 17
sources:
  - title: Build a semantic search engine with LangChain
    url: https://docs.langchain.com/oss/python/langchain/knowledge-base
    publisher: LangChain
    type: official-doc
---

An **embedding model** maps text to a numeric vector. A **vector store** keeps vectors beside their text and metadata, then finds nearby vectors for a query.

## Tiny example

```python
from langchain_core.vectorstores import InMemoryVectorStore

store = InMemoryVectorStore(embeddings)
store.add_documents(chunks)

matches = store.similarity_search(
    "How long do I have to return an order?",
    k=4,
)
```

## Keep the contracts aligned

| Contract | What to keep consistent |
| --- | --- |
| Embedding | Model, version, vector dimension, and query/document mode |
| Vector store | Distance metric, index settings, and metadata schema |
| Permissions | Tenant and access filters applied before evidence reaches the model |
| Evaluation | Frozen questions and answer-bearing source spans |

## Failure note

Similarity is not truth or permission. Using different embedding models for indexed documents and queries can collapse retrieval quality. Re-embedding only part of an index can mix incompatible vectors. Always version the index and measure retrieval after a migration.

## Related

[Text splitters](../text-splitters/) · [Retrievers](../retrievers/) · [Vector store glossary](../../glossary/vector-store/)
