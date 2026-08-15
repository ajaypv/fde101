---
title: Retrievers
description: Use the Runnable interface that accepts a query and returns relevant Document objects.
contentType: lesson
level: Intermediate
minutes: 5
topics: [LangChain, retrievers, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 18
sources:
  - title: Build a semantic search engine with LangChain - retrievers
    url: https://docs.langchain.com/oss/python/langchain/knowledge-base#use-retrievers
    publisher: LangChain
    type: official-doc
  - title: Retriever integrations
    url: https://docs.langchain.com/oss/python/integrations/retrievers/index
    publisher: LangChain
    type: official-doc
---

A **retriever** accepts an unstructured query and returns `Document` objects. It is broader than a vector store: it can wrap vector search, keyword search, an external API, or a custom fusion pipeline.

## Tiny example

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20},
)

documents = await retriever.ainvoke(
    "What is the refund window for damaged goods?"
)
```

LangChain retrievers are Runnables, so the familiar `invoke`, `ainvoke`, and batch interfaces apply. Vector stores themselves do not subclass `Runnable`.

## Remember the contract

1. Input: one query.
2. Output: a ranked list of `Document` objects.
3. Metadata: enough provenance to cite and authorize every result.
4. Evaluation: answer-bearing evidence appears within the chosen `k`.

## Failure note

Increasing `k` can hide poor recall while filling the prompt with irrelevant text. Apply permission filters before generation, log document IDs and scores, and evaluate retrieval separately from the final answer.

## Related

[Embeddings and vector stores](../embeddings-vector-stores/) · [Callbacks and tracing](../callbacks-tracing/) · [RAG evaluation](../../evals/)
