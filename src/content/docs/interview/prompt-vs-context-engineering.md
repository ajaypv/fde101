---
title: Prompt engineering versus context engineering
description: Explain how instructions differ from the complete working set supplied to a model.
contentType: interview
level: Beginner
minutes: 7
topics: [prompt engineering, context engineering, coding assistants, interview]
lastVerified: 2026-08-15
sidebar:
  order: 7
sources:
  - title: Effective context engineering for AI agents
    url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    publisher: Anthropic
    type: official-doc
  - title: Indexing repositories for GitHub Copilot
    url: https://docs.github.com/en/copilot/concepts/context/repository-indexing
    publisher: GitHub
    type: official-doc
  - title: LLM01:2025 Prompt Injection
    url: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
    publisher: OWASP Gen AI Security Project
    type: standard
---

## 30-second answer

Prompt engineering designs the task instructions, examples, and output contract. Context engineering selects and maintains the complete working set available for this inference: those instructions plus relevant code, data, tool definitions, history, state, and runtime results.[^context]

The prompt is part of the context. The two practices work together.

## One authentication request

The instruction sounds strong:

> You are an expert Python developer. Write clean, production-ready authentication code.

It still leaves important questions unanswered:

- Does the service use FastAPI, Django, or another framework?
- Does authentication use sessions, JWTs, or an external identity provider?
- Which route and service currently own the behavior?
- What user model, error schema, and database transaction pattern already exist?
- Which dependency versions and tests constrain the change?

A coding assistant needs a small, trusted context packet before it proposes a patch:

```text
user task
+ repository instructions
+ current route and caller
+ authentication service interface
+ user model and token utility
+ relevant tests and dependency versions
```

Repository indexing and semantic code search can help find related code, but the application still has to respect access policy and choose useful, current material.[^repo-index]

## The engineering flow

```text
request
  ↓
permission-filtered search
  ↓
relevant files + definitions + tests
  ↓
rank, trim, and label the context packet
  ↓
instructions + context → model proposal
  ↓
compile, test, review, and evaluate
```

The model may still produce a bad patch. Context improves the evidence available to it; tests and review decide whether the change works.

## Too much context also fails

Do not send the entire repository by default. Extra content can add stale APIs, duplicate definitions, generated files, secrets, and irrelevant examples. Treat the context window as a budget:

1. filter by the caller's permissions;
2. retrieve candidates from the current checkout;
3. expand only required definitions and dependencies;
4. prefer source code, schemas, and tests over summaries;
5. record which files and revisions were supplied;
6. test the resulting patch.

Treat repository text as untrusted data. An issue, comment, or Markdown file can contain an indirect prompt injection. Filesystem, network, and tool permissions must limit impact even when the model follows a hostile instruction; a system prompt is not that boundary.[^prompt-injection]

## Do not turn the distinction into a slogan

“Prompting improves instructions; context engineering improves information” is a useful shortcut, not a strict boundary. Instructions are themselves context, and context quality includes structure, labels, order, freshness, trust, and permissions—not only more information.

There is no universal evidence that context changes always matter more than prompt changes. Diagnose the failure and compare versions on the same task set.

## Strong closing answer

> Prompt engineering tells the model what job to do and how to return the result. Context engineering gives it the smallest trusted working set needed to do that job in this system. For authentication code, I would supply the current route, service, models, utility contracts, dependency versions, and tests—then compile and test the patch instead of trusting fluent output.

Continue with the full [context-engineering lesson](../../foundations/context-engineering/), the [context-engineering glossary note](../../glossary/context-engineering/), and [evaluation](../../evals/).

[^context]: Anthropic, [“Effective context engineering for AI agents”](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), defines prompt engineering as writing and organizing instructions and context engineering as curating the broader token set used during inference.
[^repo-index]: GitHub, [“Indexing repositories for GitHub Copilot”](https://docs.github.com/en/copilot/concepts/context/repository-indexing), documents repository indexing and semantic code search for locating relevant code by meaning. Product behavior varies by tool and policy.
[^prompt-injection]: OWASP Gen AI Security Project, [“LLM01:2025 Prompt Injection”](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), covers indirect instructions in external files and recommends least privilege, output validation, and human approval for high-risk actions.
