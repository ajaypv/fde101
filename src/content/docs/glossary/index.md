---
title: Glossary
description: Plain-English definitions for the LLM, RAG, agent, and evaluation terms an FDE uses in design discussions.
contentType: glossary
topics: [glossary, LLM, RAG, agents]
lastVerified: 2026-08-15
sidebar:
  order: 1
---

This is the alphabetical reference behind the front-page field index. Each note gives a plain definition, a small example, and the implementation detail an FDE should remember.

## A–F

- [A2A](./agent2agent-protocol/) — discovery and stateful task exchange between independently built agents.
- [A2UI](./agent-to-ui-protocol/) — declarative interfaces streamed from agents to trusted renderers.
- [Abstention](./abstention/) — choosing not to guess when evidence is insufficient.
- [Agent](./agent/) — a model-driven loop that can choose actions and tools.
- [Agent Card](./agent-card/) — A2A metadata for an agent's interfaces, skills, capabilities, and authentication requirements.
- [Agent conflict](./agent-conflict/) — disagreement between specialist findings with different roles or evidence.
- [Agentic RAG](./agentic-rag/) — retrieval whose path can change from model decisions and observations.
- [Accuracy](../evals/classification-metrics/#2-accuracy-asks-one-broad-question) — the correct share of all classification predictions.
- [Answer correctness](./answer-correctness/) — whether a response agrees with trusted truth or a reviewed reference.
- [Answer relevance](./answer-relevance/) — whether a response directly addresses the user's question.
- [BM25](./bm25/) — lexical ranking based on term frequency, rarity, and document length.
- [Chain or workflow](./workflow/) — a predefined sequence controlled by application code.
- [Checkpoint](./checkpoint/) — a persisted snapshot of workflow state.
- [Chain-of-thought prompting](./chain-of-thought/) — using intermediate-reasoning examples for some multi-step tasks.
- [Context engineering](./context-engineering/) — curating the instructions, tools, history, state, and evidence a model sees.
- [Context window](./context-window/) — the token capacity available to one model call.
- [Cosine similarity](./cosine-similarity/) — a normalized vector-direction score, not a relevance probability.
- [Embedding](./embedding/) — a numeric representation used to compare meaning.
- [Faithfulness](./faithfulness/) — whether answer claims are supported by retrieved context.
- [Fine-tuning](./fine-tuning/) — updating model weights to improve a defined, repeated behavior.
- [Feature engineering](./feature-engineering/) — turning raw observations into useful model inputs without leaking future data.
- [F1 score](../evals/classification-metrics/#4-f1-requires-both) — a harmonic mean that balances precision and recall for one class.

## G–R

- [Groundedness](./groundedness/) — whether answer claims are supported by supplied evidence.
- [Graph database](./graph-database/) — storing entities and explicit relationships for connected-path queries.
- [Hallucination](./hallucination/) — a generated claim unsupported by available evidence.
- [HNSW](./hnsw/) — a graph index for approximate nearest-neighbor search.
- [Hybrid search](./hybrid-search/) — combining semantic and keyword retrieval.
- [LLMOps](./llmops/) — evaluation, observability, release, monitoring, and incident practices for LLM systems.
- [LoRA](./lora/) — low-rank, parameter-efficient adaptation of model weights.
- [Maximal marginal relevance (MMR)](./mmr/) — balancing relevance with diversity during result selection.
- [Mean reciprocal rank (MRR)](./mrr/) — the average reciprocal position of the first relevant result.
- [Memory](./memory/) — application-managed information retained and supplied across calls or threads.
- [Micro-F1](../evals/classification-metrics/#5-micro-macro-and-weighted-answer-different-questions) — F1 after pooling decisions across classes.
- [Macro-F1](../evals/classification-metrics/#5-micro-macro-and-weighted-answer-different-questions) — the equal-weight mean of per-class F1 scores.
- [Message roles](./message-roles/) — labels separating instructions, user input, model output, and tool results.
- [Model Context Protocol (MCP)](./model-context-protocol/) — a protocol for connecting AI applications to external capabilities.
- [Precision@k](./precision-at-k/) — the relevant share of the first `k` retrieved results.
- [Prompt](./prompt/) — the instructions and context supplied for a task.
- [Prompt injection](./prompt-injection/) — untrusted content that tries to redirect a model or unsafe action.
- [Query rewriting](./query-rewriting/) — turning a question into search-friendly wording while preserving intent.
- [RLHF](./rlhf/) — using human preference data as a model-training signal.
- [RAG](./retrieval-augmented-generation/) — retrieval followed by evidence-grounded generation.
- [ReAct](./react/) — interleaving model decisions, actions, and observations.
- [Recall@k](./recall-at-k/) — the known relevant share found in the first `k` results.
- [Reranking](./reranking/) — scoring a candidate set more carefully in a second stage.

## S–V

- [Semantic search](./semantic-search/) — retrieval based on similarity of meaning.
- [Semantic cache](./semantic-cache/) — reusing an earlier answer for a sufficiently similar query.
- [State](./state/) — data carried from one workflow step to the next.
- [System prompt](./system-prompt/) — high-priority instructions for model behavior.
- [Thread](./thread/) — an identity grouping one workflow's saved state.
- [Token](./token/) — a unit of text processed or generated by a model.
- [TPM and RPM](./rate-limits/) — token-per-minute and request-per-minute provider limits.
- [Tool calling](./tool-calling/) — a structured model request for application code to invoke a capability.
- [Vector store](./vector-store/) — storage and nearest-neighbor retrieval for embeddings and metadata.
- [Weighted-F1](../evals/classification-metrics/#5-micro-macro-and-weighted-answer-different-questions) — the support-weighted mean of per-class F1 scores.

For longer treatments, continue to [production retrieval](../rag/production-retrieval/), [agent systems](../agents/), [the applied AI roadmap](../foundations/applied-ai-roadmap/), or [evaluations](../evals/).
