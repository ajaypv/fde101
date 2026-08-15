---
title: Walk through a production RAG pipeline
description: An interview-ready explanation of the offline and online RAG pipelines, including where quality actually breaks.
contentType: interview
level: Intermediate
minutes: 7
topics: [RAG, retrieval, reranking, evaluation, interview]
lastVerified: 2026-08-15
sidebar:
  order: 4
sources:
  - title: Retrieval-augmented generation for knowledge-intensive NLP tasks
    url: https://arxiv.org/abs/2005.11401
    publisher: arXiv
    type: paper
  - title: Retrieval overview
    url: https://docs.langchain.com/oss/python/langchain/retrieval
    publisher: LangChain
    type: official-doc
---

## 30-second answer

I split production RAG into an **offline evidence pipeline** and an **online answer pipeline**. Offline, I synchronize sources, inspect parsing, chunk around answer units, attach source and permission metadata, and build one or more search indexes. Online, I authorize the request, preserve the original query, optionally rewrite it, retrieve a broad candidate set, fuse and rerank results, pack the best evidence into context, then generate, cite, or abstain. I trace every stage and evaluate retrieval separately from generation.

RAG means retrieving external evidence for generation.[^rag-paper] It does not require embeddings or a vector database. Keyword search, SQL, APIs, or several retrievers together can supply the evidence.

## Think of a search desk

A librarian does not immediately hand you the first book whose title sounds similar. They clarify the request, search by subject and exact catalog terms, compare candidates, and give you the few pages that answer the question.

```text
OFFLINE
sources → parse → chunk → metadata and permissions → index

ONLINE
question → authorize → optional rewrite → broad retrieval
         → fuse and rerank → pack evidence → answer/cite/abstain
         → trace and evaluate
```

Two-step RAG—retrieve first, then generate—is often a fast and predictable starting point.[^retrieval] Additional stages should be earned by measured failures, not added because they sound advanced.

## Tiny example

The user asks, “Why does `ERR-1047` keep sending me back to sign-in?”

```text
original query  → keyword search protects ERR-1047 ─┐
rewritten query → semantic search finds login loop  ├→ fuse candidates
                                                     ↓
                                                  rerank
                                                     ↓
                                      final evidence with source IDs
                                                     ↓
                                         answer, cite, or abstain
```

The candidate and final counts are tuning choices, not universal defaults. Too few candidates can miss the answer. Too many final passages can add noise and consume the context window.

## Where quality actually breaks

| Stage | Typical failure | What I inspect |
| --- | --- | --- |
| Source and parsing | A PDF table, column, or deletion is missing | Extracted text beside the original document |
| Chunking | A rule is separated from its exception | Chunk text and section path |
| Metadata and indexing | Tenant, permission, freshness, or source identity is lost | Stored record and index version |
| Query understanding | A rewrite removes an exact code or changes intent | Original and rewritten queries |
| Retrieval | The answer-bearing passage falls below the candidate cutoff | Full ranked candidate list |
| Fusion, reranking, and packing | Good evidence is demoted, deduplicated, or truncated | Ranks before and after each stage; exact final context |
| Generation | The model ignores or changes correct evidence | Claims beside the supplied passages |
| Citations and delivery | A link exists but does not support the claim | Claim-to-passage mapping and access check |

“RAG usually breaks before the model” is a useful debugging reminder, not a fact. The model can still ignore, distort, or overgeneralize evidence that reached its context.

## Strong closing answer

I begin with the smallest pipeline that passes a representative evaluation. When a case fails, I identify the first broken artifact, change that stage, and rerun the same dataset. That is how I decide whether query rewriting, hybrid search, reranking, or a larger context set is worth its latency and cost.

Continue with [From demo RAG to production retrieval](../../rag/production-retrieval/), [RAG debugging](../rag-debugging/), and [RAG evaluation](../evaluate-rag-system/).

[^rag-paper]: Lewis et al., [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”](https://arxiv.org/abs/2005.11401), NeurIPS 2020.
[^retrieval]: LangChain’s official [retrieval documentation](https://docs.langchain.com/oss/python/langchain/retrieval) distinguishes predictable two-step RAG from agentic retrieval patterns.
