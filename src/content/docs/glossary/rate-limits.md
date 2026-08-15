---
title: TPM and RPM rate limits
description: Provider limits on tokens per minute and requests per minute.
contentType: glossary
level: Beginner
minutes: 3
topics: [TPM, RPM, rate limits, reliability]
lastVerified: 2026-08-15
sources:
  - title: Rate limits
    url: https://platform.openai.com/docs/guides/rate-limits
    publisher: OpenAI
    type: official-doc
---

**TPM** means tokens per minute; **RPM** means requests per minute. Providers may enforce both, so either can throttle a workload.

## Tiny example

Ten large requests might exhaust TPM before RPM. Thousands of tiny classification calls might hit RPM first.

## FDE note

Use bounded concurrency, exponential backoff with jitter, provider-reported retry timing, and a queue or admission policy. A retry storm can make throttling worse. Track the applicable model, account, and regional limits because limits change.
