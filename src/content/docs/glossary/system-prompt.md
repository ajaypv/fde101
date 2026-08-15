---
title: System prompt
description: High-priority instructions that establish a model's role, rules, and response contract.
contentType: glossary
level: Beginner
minutes: 3
topics: [system prompt, prompting, security]
lastVerified: 2026-08-15
sidebar:
  order: 14
---

A **system prompt** provides high-priority instructions for a model call: the task, allowed behavior, constraints, tone, and expected output format.

## Tiny example

```text
You are a support assistant.
Use only the supplied policy passages.
If the evidence is insufficient, say so.
Return the answer and source IDs.
```

## Important limit

System instructions guide model behavior; they are not a security boundary. They cannot safely replace authentication, authorization, input validation, or tool permissions.

## FDE note

Keep the prompt short enough to audit. Put stable policy in tests and application controls, and treat untrusted retrieved text as data rather than instructions.
