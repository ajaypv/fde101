---
title: How do you evaluate a RAG system?
description: A four-part interview answer that separates retrieval, generation, user outcomes, and production behavior.
contentType: interview
level: Intermediate
minutes: 10
topics: [RAG, evaluation, precision, recall, faithfulness, interview]
lastVerified: 2026-08-16
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
  - title: RAG evaluation quickstart
    url: https://deepeval.com/docs/getting-started-rag
    publisher: DeepEval
    type: official-doc
---

## 60-second answer

I evaluate a RAG system in four parts.

First, I evaluate **retrieval**. Did the system find the evidence needed to answer the question? I measure Precision@k, Recall@k, and MRR on a reviewed test set.

Second, I evaluate **generation**. Did the model answer the question, stay faithful to the retrieved evidence, reach the correct conclusion, and cite passages that support its claims?

Third, I evaluate the **end-to-end outcome**. Did the user receive a correct and useful result? I measure task success, correct abstention, and human ratings for correctness, completeness, clarity, and usefulness.

Finally, I evaluate **production behavior**. I monitor percentile latency, cost, errors, freshness, authorization, and quality drift. I do not report one overall “RAG score,” because one number cannot tell me which layer failed.

## Remember four questions

1. **Retrieval:** Did we find the right evidence?
2. **Generation:** Did we use the evidence correctly?
3. **End-to-end:** Did the user get the right result?
4. **Production:** Is the system fast, affordable, reliable, fresh, and secure?

| Layer | Artifact to inspect | Metrics or checks |
| --- | --- | --- |
| 1. Retrieval | Parsed source, search query, filters, ranked passages, and final packed context | Recall@k, Precision@k, MRR, and evidence survival after context packing |
| 2. Generation | Final context, response claims, and citations | Faithfulness, answer relevance, correctness, completeness, and citation support |
| 3. End-to-end | The complete request, response, and intended user task | Task success, correct abstention, and human review |
| 4. Production | Traces, telemetry, source versions, and authorization decisions | p50/p95 latency, cost, errors, freshness, leakage tests, and drift |

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

Walk the result through the four questions:

1. **Retrieval passes, with noise:** the policy was retrieved, so Recall@5 is `1 / 1`; Precision@5 is only `1 / 5`.
2. **Generation fails:** “Six hours qualifies” is relevant to the question but unsupported and incorrect.
3. **End-to-end fails:** the passenger received a confident answer instead of a request for the two missing facts.
4. **Production evaluation should catch the pattern:** release gates test abstention before deployment; traces and sampled reviews watch for the same failure after deployment.

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

## Use libraries as tools, not as ground truth

Evaluation libraries can run the same checks on every version. They do not decide what “good” means for your product.

| Tool | What it can help with | What your team still owns |
| --- | --- | --- |
| [RAGAS](https://docs.ragas.io/) | RAG-focused metrics and experiments across retrieval and generation | The dataset, expected behavior, metric choice, and release thresholds |
| [DeepEval](https://deepeval.com/docs/getting-started-rag) | Pytest-style regression tests and separate retriever and generator metrics | The rubric, judge configuration, and review of important failures |
| [LangSmith](https://docs.langchain.com/langsmith/evaluate-rag-tutorial) | Datasets, experiments, traces, and offline or online evaluators | Product-specific labels, security tests, and deployment decisions |

An LLM judge is useful when several answers can be valid. It is still another model. Calibrate its rubric against human-reviewed examples. Keep deterministic checks for exact facts such as citation IDs, JSON shape, tenant boundaries, and required fields.

“Hallucination” is also a failure description, not one universal metric. Turn it into a check you can repeat, such as: **Does every factual claim have support in the retrieved evidence?**

## Build a useful dataset

For each case, retain:

- the user question and important segment, such as tenant or language;
- acceptable source passages and, when useful, a reference answer;
- whether the system should answer, abstain, or escalate;
- retrieved candidates, final context, answer, citations, and system version;
- the scoring rubric and reviewer decision.

Include ordinary, edge, adversarial, permission-denied, stale-source, and unanswerable cases. Incomplete relevance labels make recall look better or worse than it is, so review misses rather than trusting only the average.

## Monitor the system after deployment

Offline tests show how a fixed version behaves on a fixed dataset. Production monitoring catches new queries, changed documents, expired permissions, and traffic patterns that the dataset did not contain.

| Production concern | What to record | Failure signal |
| --- | --- | --- |
| Latency | p50 and p95 for retrieval, reranking, and generation | A fast average hides slow requests at the tail |
| Cost | Embedding, reranking, model, and cache cost per query | Cost rises even though successful answers do not |
| Reliability | Timeouts, empty retrievals, model errors, and fallback use | The answer path fails or silently changes |
| Freshness | Source version, ingestion time, and index version | Search returns an older policy after an update |
| Security | User, tenant, ACL filters, and denied results | A user can retrieve evidence they are not allowed to read |
| Quality drift | Sampled production cases and evaluator or human scores | Faithfulness or task success falls after a model, prompt, or corpus change |

## Turn measurements into decisions

```text
Example release gate — values depend on the workflow risk

retrieval recall@5       >= agreed threshold
faithful answer rate     >= agreed threshold
end-to-end task success  >= agreed threshold
correct abstention rate  >= agreed threshold
supported citation rate  >= agreed threshold
p95 latency              <= service objective
critical data leaks       = 0
```

Do not collapse everything into one “RAG score.” A safe but irrelevant answer, a relevant hallucination, and a correct answer retrieved from unauthorized data are three different failures with different owners.

## Strong closing answer

My mental model is simple: retrieval finds the evidence, generation uses it, end-to-end evaluation checks the user's result, and production evaluation checks whether the system remains safe and dependable. When a metric moves, I inspect the changed cases and the earliest failing artifact. That tells me whether to fix parsing, chunking, retrieval depth, reranking, context assembly, generation, or the evaluation labels themselves.

Continue with [Evaluation that changes decisions](../../evals/), [From demo RAG to production retrieval](../../rag/production-retrieval/), and [Faithfulness](../../glossary/faithfulness/).

[^ir-evaluation]: Manning, Raghavan, and Schütze, [*Introduction to Information Retrieval: Evaluation of unranked retrieval sets*](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html).
[^rag-evaluation]: LangChain’s official [RAG evaluation tutorial](https://docs.langchain.com/langsmith/evaluate-rag-tutorial) separates correctness, relevance, groundedness, and retrieval relevance.
[^ragas]: Es et al., [“RAGAs: Automated Evaluation of Retrieval Augmented Generation”](https://aclanthology.org/2024.eacl-demo.16/), EACL 2024.
