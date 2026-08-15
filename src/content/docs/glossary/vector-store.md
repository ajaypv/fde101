---
title: Vector store
description: A system for storing embeddings and retrieving nearby items with their source metadata.
contentType: glossary
level: Beginner
minutes: 3
topics: [vector store, embeddings, retrieval]
lastVerified: 2026-08-15
sidebar:
  order: 7
---

A **vector store** keeps embeddings and returns nearby items according to a similarity function. Useful records also keep the original text, source location, permissions, tenant, and other metadata.

## Tiny example

A query embedding is compared with stored passage embeddings. The store returns five passage IDs, their similarity scores, and the metadata needed to fetch and cite the source text.

## What it is not

A vector store does not make retrieved content correct, current, or authorized. It also does not replace lexical search for exact identifiers.

## FDE note

Apply tenant and document-permission filters inside retrieval. Filtering results after search can leak metadata and reduce the useful result count.
