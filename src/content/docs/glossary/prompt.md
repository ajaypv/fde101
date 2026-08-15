---
title: Prompt
description: The instructions and context supplied to a model for a particular task.
contentType: glossary
level: Beginner
minutes: 3
topics: [prompt, context, language models]
lastVerified: 2026-08-15
sidebar:
  order: 13
---

A **prompt** is the input that shapes a model response. In an application it may include system instructions, a user message, examples, retrieved evidence, tool descriptions, and formatting rules.

## Tiny example

```text
Task: Answer only from the evidence.
Evidence: Refunds are allowed within 30 days.
Question: Can I return an item after 14 days?
```

## What it is not

A prompt is not a security control. A model can misunderstand instructions, and untrusted content can conflict with them.

## FDE note

Version prompts like code, test them against a stable evaluation set, and keep authorization and data-access decisions in deterministic application logic.
