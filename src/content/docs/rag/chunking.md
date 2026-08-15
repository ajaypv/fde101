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
sources:
  - title: Develop a RAG solution — chunking phase
    url: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase
    publisher: Microsoft
    type: official-doc
  - title: Text splitters
    url: https://docs.langchain.com/oss/python/integrations/splitters/index
    publisher: LangChain
    type: official-doc
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

## One document, five possible strategies

Start with the shape of the source, not a fashionable splitter.

| Strategy | A sensible use | Main risk |
| --- | --- | --- |
| Fixed tokens with overlap | Logs, transcripts, and uniform prose with few reliable headings | A window can cut a rule from its exception |
| Sentence or paragraph boundaries | Emails, reviews, FAQs, and short prose | One answer may span several paragraphs |
| Structure-aware chunks | Policies, manuals, Markdown, HTML, API docs, and well-parsed PDFs | A long section can still exceed the useful answer size |
| Parent-child retrieval | Long sections where search needs precision but the model needs wider context | Returning the full parent can add unrelated text |
| Semantic boundaries | Prose whose topic changes are real but not marked by structure | More processing, less predictable boundaries, and no guarantee of better retrieval |

Structure-aware splitting is a good first candidate when headings, lists, tables, or code blocks survive parsing. Microsoft’s chunking guidance likewise starts with document structure, while LangChain documents structure-based splitters for Markdown, HTML, JSON, and code.[^microsoft-chunking][^langchain-splitters]

## Worked example: keep the condition with the promise

An airline policy contains this section:

```text
## Hotel accommodation

We provide a hotel only when the delay requires an overnight stay
and the disruption was caused by the airline.

## Meal vouchers

We provide a meal voucher after a delay of three hours.
```

The passenger asks, “My flight is delayed by six hours. Do I get a hotel?”

A fixed boundary can produce two incomplete chunks:

```text
Chunk A: We provide a hotel only when the delay requires an overnight stay
Chunk B: and the disruption was caused by the airline. Meal vouchers ...
```

If retrieval returns only Chunk A, the model may miss the cause requirement. If it returns only Chunk B, the model may not know what the condition controls.

A structure-aware chunk keeps the answer unit together:

```text
section: Hotel accommodation
text: We provide a hotel only when the delay requires an overnight stay
      and the disruption was caused by the airline.
metadata: source=passenger-care-policy, version=2026-07, access=public
```

Now the model has both conditions. The correct response is not an automatic yes: six hours alone does not establish an overnight stay or an airline-controlled cause.

## A small structure-aware splitter

This example splits Markdown on level-two headings and repeats the heading in the searchable text. It is intentionally small enough to inspect. A production parser must also preserve tables, lists, page references, document versions, and access-control metadata.

```python title="structure_aware_chunking.py"
from pathlib import Path


def split_markdown_sections(text: str) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    heading = "Document"
    body: list[str] = []

    def save_section() -> None:
        section_text = "\n".join(body).strip()
        if section_text:
            chunks.append({
                "section": heading,
                "text": f"{heading}\n{section_text}",
            })

    for line in text.splitlines():
        if line.startswith("## "):
            save_section()
            heading = line.removeprefix("## ").strip()
            body = []
        else:
            body.append(line)

    save_section()
    return chunks


policy = Path("passenger-care-policy.md").read_text(encoding="utf-8")
for chunk in split_markdown_sections(policy):
    print(chunk)
```

Runnable copy: [`src/examples/rag/structure_aware_chunking.py`](https://github.com/ajaypv/fde101/blob/main/src/examples/rag/structure_aware_chunking.py).

## Overlap reduces one risk and creates another

```text
Source:      Returns are allowed for 30 days | except final-sale items.

No overlap: [Returns are allowed for 30 days] [except final-sale items]
Risk:        the rule is retrieved without its exception

Large overlap:
             [Returns are allowed ... except final-sale items]
             [allowed ... except final-sale items]
Risk:        near-duplicates occupy two result slots
```

Overlap cannot guarantee that an idea stays intact. Prefer structure-aware boundaries first, then add and tune enough overlap to improve measured retrieval without flooding the context with duplicates.

## Tune three variables together

| Variable | Too low | Too high |
| --- | --- | --- |
| Chunk size | Missing explanation or qualifiers | Several topics compete inside one result |
| Overlap | Boundary facts disappear | Duplicate results consume context |
| Retrieved count, `k` | Relevant evidence is missed | Noise, latency, and token use increase |

## A practical experiment

Create 30–50 representative questions and label the passages that can answer them. Compare a few chunking strategies using recall at a fixed `k`, then inspect the misses. Do not choose by intuition alone.

Use the same evaluation cases for each candidate:

1. **Parse once.** Save an inspectable representation so parser changes do not masquerade as chunking gains.
2. **Define the answer unit.** Label the source span that contains a complete answer, including qualifications and exceptions.
3. **Build candidates.** Compare a simple paragraph baseline with one or two strategies suited to the document structure.
4. **Hold retrieval constant.** Use the same corpus snapshot, questions, embedding model, query transformation, and `k`.
5. **Measure and inspect.** Compare Recall@k and Precision@k, then read the misses and near-duplicate results.
6. **Check the whole system.** Confirm answer correctness, citation quality, latency, index size, and re-indexing cost before shipping.

If several pipeline components change together, you have measured the new bundle, not the isolated effect of chunking.

## FDE questions

- What is the smallest source unit a user would accept as a citation?
- Are tables, diagrams, or code being flattened incorrectly?
- Can a chunk retain source, section, tenant, and permission metadata?
- Which document changes trigger re-indexing?

## Interview answer in 30 seconds

> I choose chunking from the answer unit and document structure, not from a universal token count. For a policy manual, I would keep each heading with its complete rule, list, table, exceptions, source identity, version, and ACL metadata. If a section is too long, I would search smaller child chunks and return a larger parent section. Then I would compare that strategy with a paragraph or fixed-token baseline on labeled questions, holding the corpus, query path, embedding model, and `k` constant. I would ship the strategy only if retrieval and end-to-end answer quality improve without unacceptable latency, storage, or citation costs.

[^microsoft-chunking]: Microsoft, [“Develop a RAG solution — chunking phase”](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase), recommends choosing approaches from document structure and testing alternatives for the use case.
[^langchain-splitters]: LangChain, [“Text splitters”](https://docs.langchain.com/oss/python/integrations/splitters/index), documents token-, character-, and structure-based splitting approaches.
