---
title: Mean reciprocal rank
description: The average reciprocal position of the first relevant result across a set of queries.
contentType: glossary
level: Intermediate
minutes: 4
topics: [MRR, retrieval evaluation, ranking]
lastVerified: 2026-08-15
sources:
  - title: Ranking evaluation
    url: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/search-rank-eval
    publisher: Elastic
    type: official-doc
---

**Mean reciprocal rank**, or **MRR**, rewards placing the first relevant result near the top.

## Begin with the denominator

If three questions have their first relevant result at ranks `1`, `2`, and `5`:

```text
MRR = (1/1 + 1/2 + 1/5) / 3
    = (1 + 0.5 + 0.2) / 3
    = 0.567
```

A question with no relevant result contributes `0` under the usual convention.

## FDE note

MRR ignores every relevant item after the first. It fits lookup experiences where one strong result is enough; pair it with [Recall@k](../recall-at-k/) when an answer needs several passages.
