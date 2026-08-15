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

The standalone examples require Python 3.10 or newer. On Windows, activate a Python 3 virtual environment and confirm `python --version` before using `python`. On macOS or Linux, use `python3` and check `python3 --version`.

## Choose your path

| If you need to… | Read this first | Then read |
| --- | --- | --- |
| Understand the vocabulary | [LLM foundations](../foundations/llms/) | [Glossary](../glossary/) |
| Build a grounded assistant | [RAG, end to end](../rag/) | [Chunking](../rag/chunking/) |
| Move RAG from demo to production | [Production retrieval](../rag/production-retrieval/) | [Evaluation](../evals/) |
| Understand vector search at scale | [Cosine to HNSW](../rag/vector-search-foundations/) | [Choosing retrieval storage](../rag/choosing-retrieval-storage/) |
| Choose vector, graph, or both | [Vector versus graph search](../rag/vector-vs-graph-search/) | [Choosing retrieval storage](../rag/choosing-retrieval-storage/) |
| Research across several sources | [Agentic RAG](../rag/agentic-rag/) | [Evaluation](../evals/) |
| Build a bounded agent | [Agent systems without chaos](../agents/) | [LangGraph](../langgraph/) |
| Connect an assistant to tools | [MCP tool selection](../agents/mcp-tool-selection/) | [Prompt injection](../security/prompt-injection/) |
| Resolve agent disagreement | [Agent conflict resolution](../agents/conflict-resolution/) | [Evaluation](../evals/) |
| Build a stateful workflow | [LangGraph](../langgraph/) | [State vs memory](../interview/langgraph-state-vs-memory/) |
| Separate context from memory | [Message history and memory](../agents/message-history-and-memory/) | [State vs memory](../interview/langgraph-state-vs-memory/) |
| Give a coding assistant the right repository context | [Prompt versus context engineering](../foundations/context-engineering/) | [Interview answer](../interview/prompt-vs-context-engineering/) |
| Follow an applied AI roadmap | [Applied AI engineering roadmap](../foundations/applied-ai-roadmap/) | [Context engineering glossary](../glossary/context-engineering/) |
| Prove a system works | [Evaluation](../evals/) | [Production checklist](../field-guide/production-rag-checklist/) |
| Operate and debug a live system | [LLMOps](../llmops/) | [Semantic caching](../llmops/semantic-caching/) |
| Protect tools from injected content | [Prompt injection](../security/prompt-injection/) | [Agent systems](../agents/) |
| Build a portfolio project | [Projects that prove engineering](../projects/) | [Production checklist](../field-guide/production-rag-checklist/) |
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
