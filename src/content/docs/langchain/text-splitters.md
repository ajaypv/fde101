---
title: Text splitters
description: Divide source documents into retrievable chunks while retaining enough context and provenance.
contentType: lesson
level: Beginner
minutes: 5
topics: [LangChain, text splitters, chunking]
lastVerified: 2026-08-15
sidebar:
  order: 16
sources:
  - title: Build a semantic search engine with LangChain - load and split
    url: https://docs.langchain.com/oss/python/langchain/knowledge-base#load-and-split-a-pdf
    publisher: LangChain
    type: official-doc
  - title: Text splitter integrations
    url: https://docs.langchain.com/oss/python/integrations/splitters
    publisher: LangChain
    type: official-doc
---

A **text splitter** turns large `Document` objects into smaller `Document` objects that can be indexed and retrieved separately.

## Tiny example

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    add_start_index=True,
)
chunks = splitter.split_documents(documents)
```

`RecursiveCharacterTextSplitter` tries common separators such as paragraphs and newlines before splitting more aggressively. `add_start_index=True` records each chunk's character offset in its source document.

## Tune with questions, not taste

1. Collect real questions and the source spans that answer them.
2. Split and index a fixed corpus.
3. Measure whether the answer-bearing span appears in top-k results.
4. Inspect failures around headings, tables, lists, and chunk boundaries.
5. Change one setting, then rerun the same evaluation.

## Failure note

Large overlap increases storage and can return near-duplicate evidence. Tiny chunks can lose definitions or table headers. A character count also does not equal the model's token count.

## Related

[`Document` and loaders](../documents-loaders/) · [Embeddings and vector stores](../embeddings-vector-stores/) · [RAG evaluation](../../evals/)
