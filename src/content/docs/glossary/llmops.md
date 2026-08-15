---
title: LLMOps
description: The evaluation, observability, release, monitoring, and incident practices around an LLM-powered system.
contentType: glossary
level: Beginner
minutes: 3
topics: [LLMOps, observability, evaluation]
lastVerified: 2026-08-15
sources:
  - title: Generative AI semantic conventions
    url: https://github.com/open-telemetry/semantic-conventions-genai
    publisher: OpenTelemetry
    type: standard
---

**LLMOps** is the work required to release and operate an LLM feature: versioned evaluation, tracing, monitoring, cost and latency control, safety gates, incident review, and rollback.

## Tiny example

A prompt change passes a golden-set test, deploys to 10% of traffic, and is monitored for groundedness, p95 latency, errors, and cost. A reviewed production failure becomes a new regression case.

## FDE note

Tracing is not evaluation. A perfect trace can reveal exactly how the system produced a bad answer. Read the full [LLMOps lesson](../../llmops/).
