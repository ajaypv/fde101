---
title: How do you evaluate a RAG system?
description: An interview-ready evaluation method that separates retrieval, generation, behavior, and operations with explicit denominators.
contentType: interview
level: Intermediate
minutes: 7
topics: [RAG, evaluation, precision, recall, faithfulness, interview]
lastVerified: 2026-08-15
sidebar:
  order: 6
sources:
  - title: Evaluation of unranked retrieval sets
    url: https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html
    publisher: Stanford NLP Group
    type: book
  - title: Evaluate a RAG application
    url: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
    publisher: LangChain
    type: official-doc
  - title: RAGAs — Automated Evaluation of Retrieval Augmented Generation
    url: https://aclanthology.org/2024.eacl-demo.16/
    publisher: Association for Computational Linguistics
    type: paper
---

## 30-second answer

I use three passes: **Find, Answer, Ship**. First, did retrieval find the labeled evidence? I report precision@k, recall@k, rank, and `k`. Second, did the model answer from that evidence? I check faithfulness, relevance, correctness, and completeness. Third, should we ship the behavior? I test citations, abstention, permissions, latency, cost, and errors against release gates on a versioned dataset.

## The 1–2–3 mental model

1. **Find and preserve the evidence.** Inspect the query, filters, ranked passages, and exact final context.
2. **Answer from the evidence.** Inspect the final context, claims, and citations.
3. **Ship only after gates pass.** Inspect the end-to-end trace, safety checks, latency, and cost.

| Pass | Interview question to ask | Metrics or checks |
| --- | --- | --- |
| 1. Find | Did retrieval return the answer-bearing passage, and did packing keep it? | Recall@k, Precision@k, and MRR on retrieval; evidence-survival check on final context |
| 2. Answer | Did the response use that passage correctly? | Faithfulness, relevance, correctness, completeness |
| 3. Ship | Would I trust this behavior for real users? | Abstention, citation support, permissions, p95 latency, cost, errors |

## Begin with the denominator

For one question, suppose two passages are labeled relevant:

```text
known relevant:  us-return-policy, country-exceptions

top 3 retrieved:
1. us-return-policy     relevant
2. pricing              not relevant
3. security             not relevant
```

- **Precision@3 = 1 / 3**: one of the three returned passages is relevant.
- **Recall@3 = 1 / 2**: one of the two known relevant passages was found.

Precision and recall describe different failure costs.[^ir-evaluation] High recall helps the answer-bearing evidence enter the candidate set. High precision keeps distracting evidence out of the final context.

## Diagnose one airline answer

Use this fictional support ticket, not a real airline rule:

```text
Hotel accommodation applies only when:
1. the delay requires an overnight stay, and
2. the airline caused the delay.
```

A passenger asks, “My flight is delayed by six hours. Am I eligible for a free hotel?” The booking record confirms six hours, but it does not say whether the trip now requires an overnight stay. The operations feed has not classified the cause.

| Ticket fact | Known? | Decision consequence |
| --- | --- | --- |
| Delay is six hours | Yes | Not enough by itself |
| Overnight stay is required | No | Ask the passenger or inspect the itinerary |
| Airline caused the delay | No | Check the operations record |
| Policy requires both conditions | Yes | Do not promise a hotel yet |

Suppose the correct policy is one of five retrieved passages and the other four are irrelevant:

```text
Hit@5       = 1
Precision@5 = 1 / 5
Recall@5    = 1 / 1
```

Hit@5 asks whether at least one relevant result appeared. It equals the pass/fail interpretation of Recall@5 here only because this case has one known relevant policy. Retrieval found all labeled evidence, but it also supplied noise. Suppose context packing preserves all five passages and the model answers, “Yes, a six-hour delay qualifies.”

| Check | Result | Why |
| --- | --- | --- |
| Retrieval recall@5 | Passes this case | The policy appeared in the retrieved top five |
| Context preservation | Passes this case | The policy remained in the final model context |
| Answer relevance | Passes | The response addresses hotel eligibility |
| Faithfulness | Fails | The policy never says six hours alone qualifies |
| Correctness | Fails | Overnight need and airline-controlled cause are still unknown |

Walk the result through the mental model:

1. **Find passes, with noise:** the policy was retrieved, so Recall@5 is `1 / 1`; Precision@5 is only `1 / 5`.
2. **Answer fails:** “Six hours qualifies” is relevant to the question but unsupported and incorrect.
3. **Ship blocks the reply:** ask for the two missing facts or send the ticket to a support agent.

The safe conclusion is not automatically “yes” or “no.” A good retrieval score cannot prove the final answer is good.

## Score the answer separately

The retrieved evidence says:

> US orders may be returned within 14 days.

The model answers:

> US orders may be returned within 14 days. This policy applies worldwide.

| Check | Compares | Result in this tiny example |
| --- | --- | --- |
| Faithfulness or groundedness | Answer claims vs retrieved evidence | 1 of 2 explicit claims is supported |
| Answer relevance | Answer vs user question | It addresses the topic, despite adding a bad claim |
| Correctness | Answer vs trusted reference answer | Partly wrong if the reference limits the rule to the US |
| Completeness | Answer vs required points | Missing the country exception |
| Citation support | Each cited claim vs cited passage | The worldwide claim has no supporting passage |

These checks are related but not interchangeable. RAG evaluation guides commonly separate response correctness, response relevance, groundedness, and retrieval relevance by the artifacts each one compares.[^rag-evaluation] The RAGAS paper likewise treats retrieval focus, faithful use of context, and generation quality as separate dimensions.[^ragas]

The `1 / 2` faithfulness result above is a hand-labeled teaching example, not a universal automatic formula. In a real evaluation, define how claims are split, what counts as support, and how disagreements are reviewed.

## Build a useful dataset

For each case, retain:

- the user question and important segment, such as tenant or language;
- acceptable source passages and, when useful, a reference answer;
- whether the system should answer, abstain, or escalate;
- retrieved candidates, final context, answer, citations, and system version;
- the scoring rubric and reviewer decision.

Include ordinary, edge, adversarial, permission-denied, stale-source, and unanswerable cases. Incomplete relevance labels make recall look better or worse than it is, so review misses rather than trusting only the average.

## Turn measurements into decisions

```text
Example release gate — values depend on the workflow risk

retrieval recall@5       >= agreed threshold
faithful answer rate     >= agreed threshold
correct abstention rate  >= agreed threshold
p95 latency              <= service objective
critical data leaks       = 0
```

Do not collapse everything into one “RAG score.” A safe but irrelevant answer, a relevant hallucination, and a correct answer retrieved from unauthorized data are three different failures with different owners.

## Strong closing answer

When a metric moves, I inspect the individual changed cases and the earliest failing artifact. That tells me whether to fix parsing, chunking, retrieval depth, reranking, context assembly, generation, or the evaluation labels themselves.

Continue with [Evaluation that changes decisions](../../evals/), [From demo RAG to production retrieval](../../rag/production-retrieval/), and [Faithfulness](../../glossary/faithfulness/).

[^ir-evaluation]: Manning, Raghavan, and Schütze, [*Introduction to Information Retrieval: Evaluation of unranked retrieval sets*](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html).
[^rag-evaluation]: LangChain’s official [RAG evaluation tutorial](https://docs.langchain.com/langsmith/evaluate-rag-tutorial) separates correctness, relevance, groundedness, and retrieval relevance.
[^ragas]: Es et al., [“RAGAs: Automated Evaluation of Retrieval Augmented Generation”](https://aclanthology.org/2024.eacl-demo.16/), EACL 2024.
