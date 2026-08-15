---
title: LoRA
description: A parameter-efficient fine-tuning method that trains small low-rank updates while keeping base weights frozen.
contentType: glossary
level: Intermediate
minutes: 4
topics: [LoRA, fine-tuning, model training]
lastVerified: 2026-08-15
sources:
  - title: LoRA — Low-Rank Adaptation of Large Language Models
    url: https://arxiv.org/abs/2106.09685
    publisher: arXiv
    type: paper
---

**LoRA**, or **Low-Rank Adaptation**, freezes the pretrained weights and learns smaller low-rank matrices that modify selected layers.[^lora]

## Tiny example

Instead of updating every weight in a large model for a classifier, train a compact adapter and keep the base checkpoint unchanged.

## FDE note

LoRA changes *how* you fine-tune, not whether fine-tuning is the correct lever. Begin with a stable task, good examples, and a versioned eval; use retrieval for facts that change.

[^lora]: Hu et al., [“LoRA: Low-Rank Adaptation of Large Language Models”](https://arxiv.org/abs/2106.09685), 2021.
