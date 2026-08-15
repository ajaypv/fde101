---
title: Groundedness
description: The degree to which answer claims are supported by the evidence supplied to the model.
contentType: glossary
level: Intermediate
minutes: 3
topics: [groundedness, evaluation, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 16
---

**Groundedness** measures whether an answer's claims are supported by the evidence available in the request, such as retrieved passages or tool results.

## Tiny example

Evidence says “Returns are accepted for 30 days.” The answer “Returns are accepted for 60 days” is ungrounded, even if another company happens to use that policy.

## Related but different

- **Correctness** asks whether a claim is true according to a reference.
- **Groundedness** asks whether the supplied evidence supports it.
- **Completeness** asks whether important parts of the question were answered.

## FDE note

Evaluate claim by claim and retain source IDs. A fluent answer with a citation is not necessarily grounded if the cited passage does not entail the claim.
