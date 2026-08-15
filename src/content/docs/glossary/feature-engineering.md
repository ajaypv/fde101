---
title: Feature engineering
description: Turning raw observations into measurable inputs that expose useful patterns to a machine-learning model.
contentType: glossary
level: Beginner
minutes: 5
topics: [machine learning, features, data leakage]
lastVerified: 2026-08-15
sidebar:
  order: 43
sources:
  - title: Dataset transformations
    url: https://scikit-learn.org/stable/data_transforms.html
    publisher: scikit-learn
    type: official-doc
  - title: Common pitfalls and recommended practices
    url: https://scikit-learn.org/stable/common_pitfalls.html
    publisher: scikit-learn
    type: official-doc
---

**Feature engineering** turns raw data into inputs that make a useful signal easier for a model to learn.

## Tiny example

Raw transaction records contain timestamps and amounts. A fraud model may benefit from derived features:

```text
transactions in the last hour
amount ÷ the account's normal amount
days since the account was opened
country changed since the previous transaction
```

Changing random forest to a neural network cannot recover information that the inputs never represent.

## Before changing the algorithm again

1. Verify labels, missing values, class balance, and the evaluation split.
2. Inspect errors by user, time period, and important segment.
3. Add only features available at the real prediction time.
4. Fit transformations on training data, then apply them to validation and test data.
5. Compare against the same baseline and check latency, drift, fairness, and maintainability.

scikit-learn's pipeline guidance warns that fitting preprocessing or feature selection on test data leaks information and creates an optimistic score.[^leakage]

## FDE note

Feature engineering is an experiment, not a guaranteed fix. Watch for label leakage, future information, unstable identifiers, and proxy variables that encode sensitive attributes.

[^leakage]: scikit-learn, [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), recommends splitting before preprocessing and fitting transformations only on training data.
