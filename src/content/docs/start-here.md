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
| Understand the vocabulary | [LLM foundations](/foundations/llms/) | [Glossary](/glossary/) |
| Build a grounded assistant | [RAG, end to end](/rag/) | [Chunking](/rag/chunking/) |
| Build a stateful workflow | [LangGraph](/langgraph/) | [State vs memory](/interview/langgraph-state-vs-memory/) |
| Prove a system works | [Evaluation](/evals/) | [Production checklist](/field-guide/production-rag-checklist/) |
| Prepare for an interview | [Interview room](/interview/) | [RAG debugging](/interview/rag-debugging/) |

## How each chapter works

Every lesson uses the same reading rhythm:

1. **One sentence** — the idea without framework language.
2. **Tiny example** — the smallest concrete case.
3. **Code** — a readable reference, not a magic abstraction.
4. **Failure modes** — what breaks in a customer environment.
5. **FDE questions** — what to ask before proposing a design.
6. **Sources** — official documentation or primary research at the point of the claim.

## A sensible first week

Read [LLM foundations](/foundations/llms/), [RAG](/rag/), and [evaluation](/evals/). Then run the three examples in `src/examples`. That gives you enough vocabulary to discuss a real use case without pretending the hard production questions are already solved.
