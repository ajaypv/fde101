---
title: Document and loaders
description: Normalize source text and provenance into Document objects before retrieval.
contentType: lesson
level: Beginner
minutes: 5
topics: [LangChain, Document, document loaders]
lastVerified: 2026-08-15
sidebar:
  order: 15
sources:
  - title: Build a semantic search engine with LangChain
    url: https://docs.langchain.com/oss/python/langchain/knowledge-base
    publisher: LangChain
    type: official-doc
  - title: Document loader integrations
    url: https://docs.langchain.com/oss/python/integrations/document_loaders
    publisher: LangChain
    type: official-doc
---

A LangChain `Document` holds `page_content`, a metadata dictionary, and an optional ID. A **loader** converts a file or external source into these objects.

## Tiny example

```python
from langchain_core.documents import Document

document = Document(
    page_content="Refunds are available for 30 days after delivery.",
    metadata={
        "source": "returns-policy.pdf",
        "page": 4,
        "tenant_id": "shop-17",
        "version": "2026-08-01",
    },
)
```

## Ingestion checklist

1. Load bytes from the authorized source.
2. Preserve headings, tables, page numbers, and document IDs where possible.
3. Attach version, tenant, permission, and provenance metadata.
4. Inspect extracted text before chunking.

## Failure note

Retrieval cannot recover text a loader lost. PDFs can scramble columns, omit scanned pages, or flatten tables. Test representative files, record parse failures, and never trust a source filename as an authorization boundary.

## Related

[Text splitters](../text-splitters/) · [Embeddings and vector stores](../embeddings-vector-stores/) · [Retrievers](../retrievers/)
