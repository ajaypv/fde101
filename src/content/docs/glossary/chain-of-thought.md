---
title: Chain-of-thought prompting
description: Prompting with intermediate reasoning examples to improve some multi-step tasks.
contentType: glossary
level: Intermediate
minutes: 4
topics: [chain of thought, prompting, reasoning]
lastVerified: 2026-08-15
sources:
  - title: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
    url: https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract.html
    publisher: NeurIPS
    type: paper
---

**Chain-of-thought prompting**, often shortened to **CoT**, uses examples with intermediate reasoning steps to improve performance on some multi-step tasks.[^cot]

## Tiny example

For a word problem, the prompt demonstrates how to identify quantities, apply operations, and then give a final answer instead of showing only the answer.

## FDE note

Do not treat hidden model reasoning as a reliable audit trail. Ask for concise, verifiable outputs—calculations, citations, tool results, and decision fields—and evaluate the final behavior.

[^cot]: Wei et al., [“Chain-of-Thought Prompting Elicits Reasoning in Large Language Models”](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract.html), NeurIPS 2022.
