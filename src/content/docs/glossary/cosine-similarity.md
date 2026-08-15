---
title: Cosine similarity
description: The normalized dot product used to compare vector direction, not a probability of relevance.
contentType: glossary
level: Beginner
minutes: 4
topics: [cosine similarity, embeddings, vector search]
lastVerified: 2026-08-15
sources:
  - title: Cosine similarity
    url: https://scikit-learn.org/stable/modules/metrics.html
    publisher: scikit-learn
    type: official-doc
---

**Cosine similarity** compares the direction of two vectors by dividing their dot product by their lengths.

```text
cosine(a, b) = (a · b) / (length(a) × length(b))
```

## Tiny example

`[1, 0]` and `[0.9, 0.1]` point in similar directions, so their cosine score is near `1`. `[1, 0]` and `[0, 1]` are perpendicular and score `0`.

## What it does not mean

A score of `0.82` does not mean “82% relevant,” correct, or confident. It is a geometric score inside one embedding model's space. Calibrate relevance thresholds on the chosen model and corpus.

See the worked code in [vector search foundations](../../rag/vector-search-foundations/).
