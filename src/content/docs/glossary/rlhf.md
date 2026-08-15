---
title: Reinforcement learning from human feedback
description: A family of training methods that uses human preference data to shape model behavior.
contentType: glossary
level: Intermediate
minutes: 4
topics: [RLHF, training, alignment]
lastVerified: 2026-08-15
sources:
  - title: Training language models to follow instructions with human feedback
    url: https://arxiv.org/abs/2203.02155
    publisher: arXiv
    type: paper
---

**Reinforcement learning from human feedback**, or **RLHF**, uses human judgments of model outputs as a learning signal. One well-known pipeline trains a reward model from ranked responses and then optimizes the response model against that reward.[^instruct]

## Tiny example

Reviewers prefer answer A over answer B for many prompts. A model learns to predict those preferences, and training shifts the generator toward outputs that score better.

## FDE note

RLHF is a model-development technique, not an application-time feedback button. It does not replace retrieval, authorization, or evaluation, and “human preference” depends on the people, rubric, and data collected.

[^instruct]: Ouyang et al., [“Training language models to follow instructions with human feedback”](https://arxiv.org/abs/2203.02155), 2022.
