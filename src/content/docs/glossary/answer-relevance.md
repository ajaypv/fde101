---
title: Answer relevance
description: Whether a generated answer directly addresses the user's question.
contentType: glossary
level: Beginner
minutes: 3
topics: [answer relevance, evaluation, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 31
sources:
  - title: Evaluate a RAG application
    url: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
    publisher: LangChain
    type: official-doc
---

**Answer relevance** asks whether the response addresses the user's question. It compares the answer with the question, not with the retrieved context or a reference answer.[^rag-eval]

## Tiny example

```text
Question: What is the return window?
Answer:   The company was founded in 1998.
```

The answer could be true and supported by a retrieved company-history page. It is still irrelevant to the question.

## Keep the axes separate

- [Faithfulness](../faithfulness/) compares answer claims with retrieved context.
- **Answer relevance** compares the answer with the question.
- **Correctness** compares the answer with trusted truth or a reference answer.
- **Retrieval relevance** compares retrieved passages with the question.

## FDE note

Score these dimensions separately. One blended “quality score” makes it harder to decide whether to fix retrieval, context assembly, or generation.

[^rag-eval]: LangChain, [“Evaluate a RAG application”](https://docs.langchain.com/langsmith/evaluate-rag-tutorial).
