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
---

An **embedding** is a list of numbers representing aspects of an input so related inputs can be compared mathematically.

## Tiny example

The phrases “reset my password” and “cannot sign in” may receive nearby vectors even though they do not share the same words. A semantic retriever can therefore find a login troubleshooting passage for either query.

## What it is not

An embedding is not a generated answer and is not a reversible copy of the source text. Your system still needs the original text and metadata to build context and citations.

## FDE note

Evaluate the embedding model with the customer’s language, acronyms, product names, and document types. General benchmark performance does not guarantee useful retrieval in a specialized corpus.
