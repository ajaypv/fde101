---
title: Semantic cache
description: A response cache that reuses an earlier answer when a new query embedding is sufficiently similar.
contentType: glossary
level: Intermediate
minutes: 4
topics: [semantic cache, latency, cost]
lastVerified: 2026-08-15
sources:
  - title: Semantic cache
    url: https://redis.io/docs/latest/develop/use-cases/semantic-cache/
    publisher: Redis
    type: official-doc
---

A **semantic cache** returns a stored answer for a new question whose embedding is near a previous question.

## Tiny example

“How do I install the VPN?” may reuse a validated answer for “Steps to set up the company VPN.”

## Main risk

Similar questions are not always answer-equivalent. Scope by tenant, permission, locale, model, prompt, and knowledge version; expire stale entries; exclude side effects; and measure false-hit and stale-hit rates.

See [semantic caching without serving the wrong answer](../../llmops/semantic-caching/).
