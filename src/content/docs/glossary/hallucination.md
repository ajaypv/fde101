---
title: Hallucination
description: A practical definition of LLM hallucination and the controls used to reduce unsupported claims.
contentType: glossary
level: Beginner
minutes: 3
topics: [hallucination, groundedness, evaluation]
lastVerified: 2026-08-15
sidebar:
  order: 3
---

A **hallucination** is a generated claim that is not supported by the evidence available to the system.

Fluent language is not evidence. A model can confidently produce an incorrect date, source, API, or customer policy.

## Controls

- retrieve authoritative evidence at request time;
- ask for abstention when evidence is insufficient;
- require citations for consequential claims;
- validate structured outputs and tool arguments;
- evaluate groundedness and correct abstention on representative cases;
- keep humans in the loop for high-impact actions.

These controls reduce risk but do not create a guarantee. The acceptable residual risk depends on the workflow.
