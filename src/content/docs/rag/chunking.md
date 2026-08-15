---
title: Chunking without folklore
description: Choose RAG chunk boundaries from the answer unit and measure whether retrieval preserves enough context.
contentType: lesson
level: Intermediate
minutes: 9
topics: [RAG, chunking, retrieval]
lastVerified: 2026-08-15
sidebar:
  order: 2
---

Chunking converts source documents into the units your retriever can return. There is no universally correct character count.

## Begin with the answer unit

Imagine a support page with three headings: **Eligibility**, **Required documents**, and **Approval time**. A paragraph-sized chunk may preserve one complete answer. A fixed slice through the middle of two headings may not.

Prefer boundaries that preserve meaning:

- headings and their body text;
- list introductions with their list items;
- table headers with the matching rows;
- code signatures with their explanation;
- document identity and access metadata on every chunk.

## Tune three variables together

| Variable | Too low | Too high |
| --- | --- | --- |
| Chunk size | Missing explanation or qualifiers | Several topics compete inside one result |
| Overlap | Boundary facts disappear | Duplicate results consume context |
| Retrieved count, `k` | Relevant evidence is missed | Noise, latency, and token use increase |

## A practical experiment

Create 30–50 representative questions and label the passages that can answer them. Compare a few chunking strategies using recall at a fixed `k`, then inspect the misses. Do not choose by intuition alone.

## FDE questions

- What is the smallest source unit a user would accept as a citation?
- Are tables, diagrams, or code being flattened incorrectly?
- Can a chunk retain source, section, tenant, and permission metadata?
- Which document changes trigger re-indexing?
