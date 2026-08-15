---
title: Agentic RAG
description: Retrieval in which model decisions can change the query, source, or number of retrieval steps while a request runs.
contentType: glossary
level: Advanced
minutes: 4
topics: [agentic RAG, adaptive retrieval, agents]
lastVerified: 2026-08-15
sidebar:
  order: 42
sources:
  - title: Adaptive-RAG
    url: https://arxiv.org/abs/2403.14403
    publisher: arXiv
    type: paper
---

**Agentic RAG** lets model-driven decisions change whether, where, or how often a system retrieves evidence.

## Tiny comparison

```text
fixed RAG:     question → known retriever → answer
agentic RAG:   question → choose search → inspect evidence
                        → refine or search elsewhere → answer
```

Several sources do not automatically make a system agentic. Code can search known sources in parallel. The agentic part begins when model judgment changes the path from observations.

## FDE note

Allowlist sources, preserve evidence provenance, cap rounds and cost, define an evidence-completeness rule, and test source selection separately from answer quality. Prefer a fixed workflow when the path is already known.

Continue with [Agentic RAG earns its loop](../../rag/agentic-rag/).
