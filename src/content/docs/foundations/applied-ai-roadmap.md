---
title: Applied AI engineering, from first call to production
description: Learn software, prompting, context, retrieval, tools, agents, evaluation, operations, and fine-tuning in an evidence-led order.
contentType: lesson
level: Beginner
minutes: 22
topics: [roadmap, context engineering, evaluation, fine-tuning]
lastVerified: 2026-08-16
sidebar:
  order: 2
sources:
  - title: Effective context engineering for AI agents
    url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    publisher: Anthropic
    type: official-doc
  - title: Model optimization
    url: https://developers.openai.com/api/docs/guides/model-optimization
    publisher: OpenAI
    type: official-doc
  - title: FastAPI tutorial
    url: https://fastapi.tiangolo.com/tutorial/
    publisher: FastAPI
    type: official-doc
  - title: LangGraph overview
    url: https://docs.langchain.com/oss/python/langgraph/overview
    publisher: LangChain
    type: official-doc
  - title: What is Terraform
    url: https://developer.hashicorp.com/terraform/intro
    publisher: HashiCorp
    type: official-doc
  - title: Dataset transformations
    url: https://scikit-learn.org/stable/data_transforms.html
    publisher: scikit-learn
    type: official-doc
  - title: Common pitfalls and recommended practices
    url: https://scikit-learn.org/stable/common_pitfalls.html
    publisher: scikit-learn
    type: official-doc
---

You do not need to train a foundation model before you can build useful AI systems. An applied AI engineer connects models to software, data, tools, tests, and operations. Training models from scratch is a valuable but separate specialization.

This chapter gives you an order for learning. It also gives you a rule for debugging: change the layer that owns the measured failure.

## What you will understand

| Chapter | Question you will be able to answer |
| --- | --- |
| 1. Diagnosis | Why are “prompting is 10%” claims misleading? |
| 2. Levers | What can prompts, context, retrieval, code, and fine-tuning each fix? |
| 3. Capabilities | Which technologies teach which engineering skill? |
| 4. Learning order | What should be built first, second, and later? |
| 5. Failure diagnosis | Which layer should change when quality plateaus? |
| 6. Model work | When do feature engineering, PyTorch, or fine-tuning belong? |
| 7. Career proof | How does a target role become one measured project? |

## Chapter 1: Replace percentages with diagnosis

“Prompting is 10%” and “retrieval, context, and evals solve 90%” sound memorable, but neither number has a denominator or universal evidence.

Use this rule instead:

> Measure the failure, identify which layer owns it, change that layer, and rerun the same evaluation cases.

## Chapter 2: Keep six engineering levers separate

| Lever | What you change | Good first use | It cannot fix |
| --- | --- | --- | --- |
| Prompt | Instructions, examples, and output contract | Clarify a task or response format | Missing private or current facts |
| Context engineering | Which instructions, tools, history, state, and evidence enter this call | Give the model the smallest high-signal working set | Broken authorization or business logic |
| Retrieval | Which external evidence is found at request time | Private, attributable, or changing knowledge | A generator that ignores correct evidence |
| Deterministic code | Validation, calculation, routing, permissions, and side effects | Known rules that must behave predictably | Open-ended decisions not expressible as rules |
| Fine-tuning | Model weights from labeled examples and feedback | Stable repeated behavior, style, classification, or efficiency | Fresh knowledge that changes every day |
| Training from scratch | The general model and its capabilities | Model research or platform work at large scale | A fast application iteration loop |

Anthropic defines context engineering as curating the full set of tokens used for inference—system instructions, tools, retrieved data, message history, and other runtime information—not merely polishing a prompt.[^context]

The [prompt-versus-context lesson](../context-engineering/) shows this distinction through one Python authentication change and a permission-filtered repository context packet.

## Chapter 3: Learn capabilities, not a shopping list

| Technology | Capability it can teach | Reach for it when |
| --- | --- | --- |
| Python | Typed application logic, async I/O, tests, data handling | You need a service or pipeline you can inspect and test |
| FastAPI | HTTP routes, request validation, dependency injection, auth, streaming | The AI feature needs a Python API boundary |
| LangChain | Common interfaces and integrations for models, messages, tools, and retrieval | Its abstraction removes repeated integration work |
| LangGraph | Explicit state, branches, persistence, resume, and human approval | A workflow must survive or adapt across several steps |
| Langfuse **or** LangSmith | Traces, datasets, evaluation, and production feedback | A team needs reproducible failures and release evidence |
| Terraform | Versioned, reviewable infrastructure changes | Environments and managed services must be reproduced safely |
| pgvector, Pinecone, or Weaviate | Vector retrieval plus different storage and operating models | Measured corpus, filtering, latency, and ownership needs justify the choice |

You do not need every row in one project. A provider SDK may be simpler than LangChain; ordinary functions may be clearer than LangGraph; existing telemetry may remove the need for a new LLMOps vendor. [Choose retrieval storage](../../rag/choosing-retrieval-storage/) from evidence, not a brand checklist.

## Chapter 4: Follow a practical learning order

### 1. Software foundations

Learn Python or TypeScript, HTTP, JSON schemas, databases, async work, tests, authentication, logging, and latency. Models live inside ordinary software systems.

### 2. One model call done well

Build one typed request with clear instructions, structured output, validation, error handling, and five to ten representative evaluation cases.

### 3. Context and retrieval

Learn message roles, token budgets, chunking, metadata, keyword search, vectors, hybrid retrieval, reranking, citations, and abstention. Measure retrieval before asking the model to answer.

### 4. Tools and fixed workflows

Let the model request a typed tool, but keep argument checks, user permissions, calculations, and database writes in code. Build a fixed chain before adding a loop.

### 5. Bounded agents

Add model-directed tool choice only when the next action depends on an observation. Set step limits, timeouts, budgets, and approval boundaries.

### 6. Durable orchestration

Add explicit state, checkpoints, resume behavior, and long-term storage when the workflow must survive multiple steps or sessions. Make retries safe for side effects.

### 7. Evaluation and operations throughout

Track task success, tool correctness, retrieval quality, groundedness, latency, cost, safety, and production failures. Turn important failures into regression cases.

### 8. Fine-tune when evidence supports it

OpenAI's model-optimization workflow begins with evals, then prompt engineering, then fine-tuning where it improves the measured task.[^optimization] Fine-tuning is a good candidate when:

- the behavior is stable and repeated;
- you have enough high-quality examples;
- prompt and context changes have plateaued;
- the gain matters at your expected traffic, cost, or latency.

It is a poor store for a policy that changes weekly. Put changing facts in a governed source and retrieve them at request time.

## Chapter 5: Diagnose the failed layer

| Symptom | First place to look | Why |
| --- | --- | --- |
| Model says the old refund period | Source freshness and retrieval | The fact changed; weights are the wrong database |
| Correct passage was retrieved but answer adds an unsupported exception | Context, instructions, groundedness evaluation | Evidence reached the model; generation behavior failed |
| Output format fails in the same way across thousands of stable cases | Schema, prompt, then fine-tuning | The target behavior is repeated and measurable |

## Chapter 6: Inspect data before changing the algorithm

If random forest, SGD, and a neural network all perform similarly, pause the algorithm search. They may be hitting the same data ceiling.

Check the measurement and representation first:

```text
labels → split → raw inputs → features → model → segment-level errors
```

- Verify that the label measures the real outcome and is not noisy or delayed.
- Compare against a simple baseline on an untouched test set.
- Inspect errors by time period and important user segment.
- Ask which useful facts are missing from the current inputs.
- Derive features only from information available at prediction time.
- Put preprocessing inside the evaluation pipeline so test data cannot influence fitting.

For a transaction model, raw timestamps can become “transactions in the last hour,” and an amount can become “amount divided by this account's normal amount.” These features may expose behavior that the raw columns hide. They can also leak future information or encode sensitive proxies.

scikit-learn describes transformations as learned operations that must fit on training data and then apply to unseen data.[^transformations] Its common-pitfalls guide recommends splitting before preprocessing to prevent optimistic scores from data leakage.[^leakage]

### Where PyTorch fits

Learn tensors, gradients, attention, and optimization when you want deeper model intuition. Go further into PyTorch, GPUs, distributed training, and research papers for model-training or ML-platform roles. Do not use that path as a gate before building and evaluating an applied system.

## Chapter 7: Turn a target role into a measured gap

Collect current job descriptions from the role, location, and company type you are targeting. For every claimed requirement, retain the source posting and record:

```text
problem and user → required capability → evidence you already have → missing proof
```

An AI assistant can group the rows and draft a gap analysis, but it should cite the underlying descriptions. Do not let it manufacture salary, hiring-timeline, or interview-probability claims.

Choose one real micro-problem from a target team's domain and build the smallest project that closes a high-value gap. The [project briefs](../../projects/) show how routing, caching, regression CI, failure forensics, and documentation drift can become portfolio evidence.

## Chapter 8: Make the project prove its claims

A strong project should let another engineer answer these questions:

1. What user problem does the system solve?
2. Why is a model needed at this step?
3. What context, data, and permissions can it access?
4. What is deterministic?
5. How do retrieval and generation fail separately?
6. Which eval gates a release?
7. What do latency and cost look like at the expected load?
8. Can someone trace and reproduce a bad result?

Also require one documented failure and its measured fix. A polished happy path proves less than a reproducible before-and-after experiment.

## Interview answer in 30 seconds

> I learn applied AI in layers. First I build ordinary software and one typed model call. Then I add context and retrieval for private or changing knowledge, typed tools for external actions, and agents only when the next step depends on observations. Evaluation and tracing start with the first version and continue through production. I fine-tune only when the target behavior is stable, the dataset is strong, and measured prompt or context changes have plateaued. I choose libraries from requirements, not from a checklist.

Next: build [RAG end to end](../../rag/), study [agent systems](../../agents/), and make [evaluation](../../evals/) part of both.

[^context]: Anthropic, [“Effective context engineering for AI agents”](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
[^optimization]: OpenAI, [model optimization](https://developers.openai.com/api/docs/guides/model-optimization), describes an eval-driven cycle across prompting and fine-tuning rather than a universal one-time sequence.
[^transformations]: scikit-learn, [dataset transformations](https://scikit-learn.org/stable/data_transforms.html).
[^leakage]: scikit-learn, [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), explains how fitting preprocessing or feature selection on test data leaks information.
