---
title: Faithfulness
description: Whether every answer claim is supported by the retrieved context supplied to the model.
contentType: glossary
level: Intermediate
minutes: 3
topics: [faithfulness, groundedness, evaluation]
lastVerified: 2026-08-15
sidebar:
  order: 28
sources:
  - title: Evaluate a RAG application
    url: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
    publisher: LangChain
    type: official-doc
---

**Faithfulness** asks whether the retrieved context supports the claims in an answer. Many evaluation systems use it as a synonym for [groundedness](../groundedness/).

## Tiny example

```text
Context: Returns are accepted for 30 days.
Answer:  Returns are accepted for 30 days without a receipt.
```

The first claim is supported. “Without a receipt” is not, so the answer is not fully faithful.

## Do not confuse it with

- **Answer relevance:** does the answer address the question?
- [**Correctness:**](../answer-correctness/) does it match trusted truth or a reference answer?
- **Retrieval relevance:** do the passages relate to the question?

LangSmith's RAG evaluation guide separates these comparison pairs explicitly.[^rag-eval]

## FDE note

A faithful answer can repeat a stale or incorrect source. Groundedness is not proof that the underlying document is true or current.

[^rag-eval]: LangChain, [“Evaluate a RAG application”](https://docs.langchain.com/langsmith/evaluate-rag-tutorial).
