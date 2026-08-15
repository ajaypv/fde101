---
title: Context window
description: The token capacity available to a model for one request and its generated response.
contentType: glossary
level: Beginner
minutes: 3
topics: [context window, tokens, prompting]
lastVerified: 2026-08-15
sidebar:
  order: 11
---

The **context window** is the token budget a model can consider in one call. It includes instructions, conversation history, retrieved passages, tool results, the user's message, and room for the answer.

## Tiny example

```text
system instructions  1,000 tokens
conversation history 3,000 tokens
retrieved evidence   8,000 tokens
answer allowance     2,000 tokens
total               14,000 tokens
```

## What it is not

A large context window is not long-term memory, and fitting more text does not ensure the model will use every detail well.

## FDE note

Set an explicit budget for every part of the request. Preserve the highest-value evidence and source metadata when trimming.
