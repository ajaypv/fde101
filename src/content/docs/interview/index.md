---
title: Interview room
description: Practice explaining RAG, LangChain, LangGraph, evaluation, and FDE trade-offs with concrete reasoning.
contentType: interview
minutes: 8
topics: [interview, FDE, RAG, LangGraph]
lastVerified: 2026-08-15
sidebar:
  order: 1
---

Good answers reveal how you reason. Define the term, give a tiny example, name a trade-off, and explain how you would verify the result.

## RAG

1. Walk through a RAG request from user question to cited answer.
2. Retrieval returns related documents but not the answer-bearing passage. How do you debug it?
3. When would keyword search beat vector search?
4. How do you enforce document permissions during retrieval?
5. Why can adding more chunks make an answer worse?
6. How would you compare exact search with HNSW, and what does ANN recall@k measure?
7. When would you keep vectors in pgvector instead of adding a dedicated vector database?
8. When would you use vector search, graph traversal, or both for candidate discovery?
9. Does retrieving from several sources automatically require agentic RAG?

Practice the full answers:

- [Walk through a production RAG pipeline](./production-rag-pipeline/)
- [How would you debug a bad RAG answer?](./rag-debugging/)
- [Vector search versus graph search](../rag/vector-vs-graph-search/)
- [When agentic RAG earns its loop](../rag/agentic-rag/)

## LangChain and LangGraph

1. When is a provider SDK simpler than LangChain?
2. What information belongs in graph state?
3. What is the difference between state, a checkpoint, a thread, and a store?
4. Where would you place human approval in a graph?
5. How do you retry a tool node without duplicating a side effect?
6. Two specialist agents recommend opposite actions. Which one should the system trust?
7. How does an MCP-connected application decide which tool may run?

Practice the full answers:

- [Agent or workflow—which should you use?](./agent-vs-workflow/)
- [State versus memory](./langgraph-state-vs-memory/)
- [Resolve agent disagreement](../agents/conflict-resolution/)
- [How MCP-connected tool selection works](../agents/mcp-tool-selection/)

## Models and context

1. What is the difference between prompt engineering and context engineering?
2. How should a coding assistant find the files, interfaces, and tests relevant to a change?
3. Why can sending an entire repository make the result worse?
4. Which repository data must never enter a model context?

Practice: [Prompt engineering versus context engineering](./prompt-vs-context-engineering/) and the full [context-engineering lesson](../foundations/context-engineering/).

## Evaluation

1. Explain precision@k and recall@k using a denominator.
2. How do you evaluate an answer when several phrasings are valid?
3. What should be measured separately in a RAG system?
4. How do you turn production failures into evaluation cases?
5. Which metrics become release gates, and why?
6. The right policy was retrieved, but the final conclusion is wrong. Which layer failed?

Practice: [How do you evaluate a RAG system?](./evaluate-rag-system/)

## LLMOps and security

1. What would you record in a trace so a bad answer can be reproduced?
2. What is the difference between a trace, a metric, an evaluation, and an audit record?
3. How would you gate a prompt or model change in CI?
4. When is semantic response caching unsafe?
5. An email contains an instruction to exfiltrate a confidential file. Which controls stop the action even if the model follows the instruction?

Practice: [LLMOps](../llmops/), [semantic caching](../llmops/semantic-caching/), and [prompt-injection guardrails](../security/prompt-injection/).

## Machine-learning judgment

1. Random forest, SGD, and a neural network all plateau. What do you inspect before choosing another algorithm?
2. Give one feature that would leak future information at prediction time.
3. Why must preprocessing fit inside each training fold rather than on the full dataset?

Practice: [feature engineering](../glossary/feature-engineering/) and the [applied AI roadmap](../foundations/applied-ai-roadmap/).

## FDE judgment

1. A customer asks for an agent, but the workflow is deterministic. What do you propose?
2. The pilot looks good, but the customer has no labeled data. What happens next?
3. Security requires user-level permissions and deletion guarantees. How does the architecture change?
4. Quality and latency move in opposite directions. How do you frame the decision?
5. What do you hand over so the customer can operate the system without you?
