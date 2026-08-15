---
title: Retrieval-augmented generation (RAG)
description: A concise definition of RAG, its two lifecycles, and when it is a useful architecture.
contentType: glossary
level: Beginner
minutes: 4
topics: [RAG, retrieval, grounding]
lastVerified: 2026-08-15
sidebar:
  order: 4
sources:
  - title: Retrieval overview
    url: https://docs.langchain.com/oss/python/langchain/retrieval
    publisher: LangChain
    type: official-doc
---

**Retrieval-augmented generation**, or **RAG**, retrieves external evidence for a request and supplies that evidence to a generative model.

## Tiny example

```text
question: What is our enterprise cancellation window?
retrieve: the current enterprise cancellation policy
generate: answer from that passage
cite: link to the policy section
```

RAG is useful when answers depend on private, current, attributable, or frequently changing information.

## Two lifecycles

1. **Indexing:** load, parse, split, embed, and store the source material.
2. **Answering:** retrieve, assemble context, generate, and cite.

The distinction matters during debugging. A generation prompt cannot repair missing or stale indexed content.

Continue with the full [RAG, end to end](../../rag/) chapter.
