---
title: How would you debug a bad RAG answer?
description: An interview-ready method for tracing a bad answer through source data, retrieval, context, generation, and citations.
contentType: interview
level: Intermediate
minutes: 5
topics: [RAG, debugging, interview]
lastVerified: 2026-08-15
sidebar:
  order: 3
---

## Short answer

I trace the request in evidence order instead of changing the prompt first.

1. **Source:** Was the correct, current document ingested and parsed accurately?
2. **Retrieval:** Did the right passage appear in the top results, and at what rank?
3. **Context:** Did formatting, truncation, or deduplication remove the useful text?
4. **Generation:** Did the answer follow the supplied evidence and abstention rule?
5. **Citation:** Does each important claim point to a passage that actually supports it?

## Tiny example

If a refund answer says “30 days” but the policy says “14 days,” inspect the retrieved passages. If “14 days” was absent, it is a data or retrieval problem. If it was present and the model still said “30,” it is a generation or instruction-following problem. The fixes and owners are different.

## Strong follow-up

Add the incident to an evaluation dataset before fixing it. Then measure the change against the full set so one repair does not silently break another segment.
