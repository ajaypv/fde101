---
title: Projects that prove applied AI engineering
description: Turn a target role into one measured project with evaluation, operations, security, and a reproducible handoff.
contentType: lesson
level: Beginner
minutes: 18
topics: [projects, portfolio, roadmap, FDE]
lastVerified: 2026-08-15
sidebar:
  order: 1
sources:
  - title: Python tutorial
    url: https://docs.python.org/3/tutorial/
    publisher: Python Software Foundation
    type: official-doc
  - title: FastAPI tutorial
    url: https://fastapi.tiangolo.com/tutorial/
    publisher: FastAPI
    type: official-doc
  - title: What is Terraform
    url: https://developer.hashicorp.com/terraform/intro
    publisher: HashiCorp
    type: official-doc
  - title: Building effective agents
    url: https://www.anthropic.com/engineering/building-effective-agents
    publisher: Anthropic
    type: official-doc
---

A portfolio project is useful when it proves a decision, not when it contains the longest list of libraries. One deeply explained system can demonstrate more judgment than five cloned chatbots.

## Begin with a target, not a stack

Collect 10–20 current job descriptions from the role, location, and company type you actually want. Extract evidence rather than asking AI to invent a market analysis:

| Column | Example evidence |
| --- | --- |
| User and domain | Support engineers answering policy questions |
| Repeated problem | Slow incident diagnosis across runbooks and traces |
| Required capabilities | Python, APIs, retrieval, evaluation, observability |
| Operational constraints | Multi-tenancy, p95 latency, audit trail |
| Your demonstrated evidence | Link to a tested RAG service and eval report |
| Gap | No deployment or threat-model example yet |

An LLM can group and summarize the collected descriptions. It should cite the exact postings behind each conclusion. Hiring dates, salary claims, “80% coverage,” and interview guarantees are not evidence-backed roadmap inputs.

## Learn the stack in layers

| Layer | Learn first | Add when the project needs it |
| --- | --- | --- |
| Software | Python types, functions, exceptions, async, HTTP/JSON, tests | FastAPI request models, auth, errors, timeouts, streaming |
| AI application | One model call, structured output, context, retrieval, evals | LangChain integrations or provider SDKs |
| Workflow | Fixed functions and explicit state | LangGraph when branching, persistence, resume, or approval matter |
| Retrieval | BM25, embeddings, filters, exact search | HNSW, hybrid search, reranking, pgvector/Pinecone/Weaviate |
| Operations | Logs, traces, p95 latency, versioned evals | Langfuse, LangSmith, or existing OpenTelemetry tooling |
| Delivery | Environment config and one reproducible deploy | Terraform when infrastructure must be versioned and reviewed |

Python, FastAPI, LangChain, LangGraph, Langfuse, LangSmith, Terraform, and every vector database are **not** mandatory in one project. Use each tool only when it owns a real requirement.

## Five focused project briefs

### 1. Model cost router

Route a stable FAQ to a smaller model and a complex analysis to a stronger path. Begin with readable rules for risk, domain, required capability, and request size before training a router.

Prove routing accuracy, end-task quality, p95 latency, and cost per successful task. Always send high-risk writes through the protected route; a cheap classifier must not downgrade authority.

### 2. Safe semantic cache

Cache only stable, read-only FAQ responses. Scope entries by tenant, authorization, locale, model, prompt, and knowledge version.

Prove hit rate, false-hit rate, stale-hit rate, zero cross-tenant hits, added lookup latency, and saved model calls. Include the [unsafe cases](../llmops/semantic-caching/) in tests.

### 3. Model regression CI

Create a versioned golden set and run it when the prompt, model, chunking, retriever, tool schema, or code changes. Deliberately introduce one bad prompt and show the build blocking it.

Prove per-case failures, retrieval and answer metrics, deterministic safety invariants, dataset version, and comparison with the last accepted baseline.

### 4. Failure-forensics viewer

Render one RAG trace from authorization through retrieval, reranking, model generation, and citation validation. Make the first broken stage obvious.

Prove that a reviewer can reproduce one real failure from trace, prompt/model/index versions, retrieved IDs, and the exact final context—without exposing secrets in telemetry.

### 5. Documentation drift detector

Detect when a code or API change may make a linked document stale. Generate a proposed patch, run link/code checks, and require a human review before modifying the authoritative page.

Call it **drift detection and reviewed repair**, not “self-healing docs.” Automatic rewriting can propagate a model error into the source of truth.

## One stronger capstone

Combine the ideas only after each part is understandable:

```text
multi-tenant support assistant
├─ hybrid retrieval + reranking
├─ bounded read-only order tool
├─ citations, abstention, and human escalation
├─ versioned golden-set CI
├─ Langfuse or LangSmith traces
├─ quality, p95 latency, and cost report
├─ tenant and prompt-injection tests
├─ semantic cache on a safe FAQ route only
└─ reproducible deployment + runbook
```

## The acceptance checklist

Your repository should let a reviewer find:

- the user problem and explicit non-goals;
- an architecture and trust-boundary diagram;
- a small versioned evaluation dataset;
- quality, safety, p95 latency, and cost results;
- one failure, its root cause, and the measured fix;
- exact setup and test commands;
- a threat model and known limitations;
- deployment configuration and an operator runbook.

Only claim what the evidence shows. A good project can improve your skill and give an interviewer something concrete to discuss; it cannot guarantee a referral, salary, interview, or job.

Next: follow the [applied AI roadmap](../foundations/applied-ai-roadmap/) or use the [production checklist](../field-guide/production-rag-checklist/) as your definition of done.
