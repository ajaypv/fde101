---
title: Answer correctness
description: Whether a generated answer agrees with trusted truth or a reviewed reference answer.
contentType: glossary
level: Beginner
minutes: 4
topics: [answer correctness, evaluation, RAG]
lastVerified: 2026-08-15
sidebar:
  order: 44
sources:
  - title: Evaluate a RAG application
    url: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
    publisher: LangChain
    type: official-doc
---

**Answer correctness** asks whether the response agrees with trusted truth or an accepted reference answer. It compares the answer with the reference, not merely with the retrieved context.[^rag-eval]

## Tiny example

Use this synthetic airline policy:

```text
Hotel accommodation applies only when:
1. the delay requires an overnight stay, and
2. the airline caused the delay.
```

The passenger says only that the flight is six hours late. The correct conclusion is: **there is not enough information yet**. An answer that says “Yes, six hours qualifies” addresses the question, but it is incorrect.

## Keep the comparisons separate

| Check | Compares the answer with | Question |
| --- | --- | --- |
| [Faithfulness](../faithfulness/) | Retrieved context | Does the evidence support each claim? |
| [Answer relevance](../answer-relevance/) | User question | Did the response address the request? |
| **Answer correctness** | Trusted reference | Did it reach an accepted conclusion? |

A faithful answer can repeat a stale policy and still be incorrect. A correct answer can come from unsupported model memory and still be unfaithful.

## FDE note

Reference answers can also be incomplete. Store the policy version, allow equivalent valid wording, define partial credit, and send disputed or high-impact cases to human review. A model judge is an evaluator, not ground truth.

[^rag-eval]: LangChain, [“Evaluate a RAG application”](https://docs.langchain.com/langsmith/evaluate-rag-tutorial), defines correctness as response versus reference answer and separates it from response relevance and groundedness.
