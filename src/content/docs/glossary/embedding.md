---
title: Embedding
description: A plain-English definition of embeddings and how they are used in semantic retrieval.
contentType: glossary
level: Beginner
minutes: 3
topics: [embedding, retrieval, vector search]
lastVerified: 2026-08-15
sidebar:
  order: 2
sources:
  - title: Introduction to embeddings
    url: https://docs.cohere.com/v1/docs/embeddings
    publisher: Cohere
    type: official-doc
  - title: Create a vector query
    url: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-query
    publisher: Microsoft
    type: official-doc
---

An **embedding** is a list of numbers representing aspects of an input so related inputs can be compared mathematically.

## Tiny example

The phrases “reset my password” and “cannot sign in” may receive nearby vectors even though they do not share the same words. A semantic retriever can therefore find a login troubleshooting passage for either query.

## What it is not

An embedding is not a generated answer and is not a reversible copy of the source text. Your system still needs the original text and metadata to build context and citations.

## Keep one compatible space

Query and document vectors must come from a compatible model configuration. Equal dimensions do not prove compatibility. Pin the provider, model, version, dimensions, preprocessing, input mode, and distance function with the index.

Some models intentionally expose different compatible modes for queries and documents.[^cohere] A model change normally requires a new index, re-embedding, and evaluation before cutover.

## FDE note

Evaluate the embedding model with the customer’s language, acronyms, product names, and document types. General benchmark performance does not guarantee useful retrieval in a specialized corpus. Continue to [cosine and vector search](../../rag/vector-search-foundations/).

[^cohere]: Cohere's [embedding documentation](https://docs.cohere.com/v1/docs/embeddings) distinguishes compatible `search_query` and `search_document` modes.
