---
title: How to use this book
description: Choose a short learning path through FDE 101 and understand how every chapter is structured.
contentType: lesson
level: Beginner
minutes: 5
topics: [learning path, FDE]
lastVerified: 2026-08-15
sidebar:
  order: 1
---

This is a reference book, not a course you must finish in order. Start with a customer problem, read the smallest useful chapter, and keep the code nearby.

## Choose your path

| If you need to… | Read this first | Then read |
| --- | --- | --- |
| Understand the vocabulary | [LLM foundations](../foundations/llms/) | [Glossary](../glossary/) |
| Build a grounded assistant | [RAG, end to end](../rag/) | [Chunking](../rag/chunking/) |
| Move RAG from demo to production | [Production retrieval](../rag/production-retrieval/) | [Evaluation](../evals/) |
| Build a bounded agent | [Agent systems without chaos](../agents/) | [LangGraph](../langgraph/) |
| Build a stateful workflow | [LangGraph](../langgraph/) | [State vs memory](../interview/langgraph-state-vs-memory/) |
| Follow an applied AI roadmap | [Applied AI engineering roadmap](../foundations/applied-ai-roadmap/) | [Context engineering](../glossary/context-engineering/) |
| Prove a system works | [Evaluation](../evals/) | [Production checklist](../field-guide/production-rag-checklist/) |
| Prepare for an interview | [Interview room](../interview/) | [RAG debugging](../interview/rag-debugging/) |

## How each chapter works

Every lesson uses the same reading rhythm:

1. **One sentence** — the idea without framework language.
2. **Tiny example** — the smallest concrete case.
3. **Code** — a readable reference, not a magic abstraction.
4. **Failure modes** — what breaks in a customer environment.
5. **FDE questions** — what to ask before proposing a design.
6. **Sources** — official documentation or primary research at the point of the claim.

## A sensible first week

Begin with the [applied AI engineering roadmap](../foundations/applied-ai-roadmap/), then read [LLM foundations](../foundations/llms/), [RAG](../rag/), and [evaluation](../evals/). Choose [production retrieval](../rag/production-retrieval/) if the system answers from documents, or [agent systems without chaos](../agents/) if it must choose tools and actions. Then run the examples in `src/examples`.
