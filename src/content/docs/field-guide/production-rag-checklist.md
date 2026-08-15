---
title: Production RAG checklist
description: A compact delivery checklist for data access, retrieval quality, grounded answers, reliability, and customer handoff.
contentType: field-guide
level: Intermediate
minutes: 8
topics: [RAG, production, FDE, checklist]
lastVerified: 2026-08-15
sidebar:
  order: 1
---

Use this before a pilot, design review, or production handoff. A checked box should point to evidence—not confidence.

## Data and access

- [ ] Source owners and freshness expectations are named.
- [ ] Deletions and access changes propagate to the index.
- [ ] Document and chunk metadata retain tenant and permission boundaries.
- [ ] Retrieved content is authorized for the requesting user.
- [ ] Sensitive data handling and retention are documented.

## Retrieval

- [ ] Representative questions have labeled supporting passages.
- [ ] Chunking preserves headings, lists, tables, and source identity.
- [ ] Retrieval metrics include the value of `k` and an explicit denominator.
- [ ] Filters, hybrid search, or reranking have evidence that they improve a baseline.
- [ ] Operators can inspect retrieved passages for one request.

## Generation and citations

- [ ] The model is told what to do when evidence is insufficient.
- [ ] Claims that affect user decisions require source support.
- [ ] Citations resolve to content the user can access.
- [ ] Prompt injection in retrieved content is treated as untrusted input.
- [ ] Model and prompt versions are recorded with evaluation results.

## Reliability and operations

- [ ] Each external call has a timeout and bounded retry policy.
- [ ] Retried side effects are idempotent or explicitly guarded.
- [ ] Latency, cost, error, and quality signals are observable per stage.
- [ ] A safe degraded path exists when retrieval or the model is unavailable.
- [ ] An owner can reproduce a bad answer from request traces.

## Customer handoff

- [ ] Success criteria and release thresholds are written down.
- [ ] Known limitations are visible to users and support staff.
- [ ] Runbooks cover stale data, bad retrieval, provider failure, and data isolation.
- [ ] The customer can add evaluation cases from real failures.
- [ ] Ownership after launch is unambiguous.
