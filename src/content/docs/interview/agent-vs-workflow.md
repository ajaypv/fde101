---
title: Agent or workflow—which should you use?
description: An interview-ready comparison of deterministic workflows, model-directed agents, and practical hybrid systems.
contentType: interview
level: Intermediate
minutes: 6
topics: [agents, workflows, LangGraph, tools, interview]
lastVerified: 2026-08-15
sidebar:
  order: 5
sources:
  - title: Workflows and agents
    url: https://docs.langchain.com/oss/python/langgraph/workflows-agents
    publisher: LangChain
    type: official-doc
  - title: Custom workflow
    url: https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow
    publisher: LangChain
    type: official-doc
---

## 30-second answer

A **workflow** follows steps and branches chosen by application code. An **agent** runs in a feedback loop where a model can choose the next action from an allowed set after seeing the current state and tool results.[^workflows-agents] I start with a workflow when the path is known because it is usually cheaper, faster, and easier to test. I use a bounded agent only where the next useful step genuinely depends on an observation I could not map in advance.

The common production design is hybrid: deterministic code owns permissions, validation, money, and writes; a small agentic node handles one uncertain decision.

## Tiny comparison

| Problem | Better starting point | Why |
| --- | --- | --- |
| Read an invoice, validate totals, request approval, write to ERP | Workflow | The steps and business rules are known |
| Investigate an unfamiliar outage using logs, metrics, and runbooks | Bounded agent | Each result changes the next useful check |
| Search uncertain evidence, then issue a refund | Hybrid | An agent may search; code authorizes and performs the refund |

```text
WORKFLOW
extract → validate totals → human approval → write

AGENT INSIDE A WORKFLOW
authorize → [model chooses search or log tool in a bounded loop]
          → deterministic validator → human approval → write
```

LangGraph can represent fixed edges, conditional branches, or an agent loop. Using LangGraph does not automatically make a system an agent.

## One tool call is not automatically an agent

If application code always calls `lookup_order` and the model only fills its typed arguments, the application still controls the sequence. It becomes agentic when the model can observe the result and choose whether to call another allowed tool, answer, or stop.

## When an agent is the wrong choice

Prefer a workflow when:

- the required sequence can be specified and tested;
- the action has a strict business rule or calculation;
- low latency and predictable cost matter more than flexibility;
- a mistake creates a payment, deletion, permission change, or other side effect;
- there is no reliable signal that tells a loop whether it improved.

An agent also needs scoped tools, validated arguments, step and token limits, timeouts, observable state, and approval before consequential actions.

## Important caveat

“If I can draw the workflow, I never use an agent” is a strong starting heuristic, not a law. You can draw an agent loop, and a known outer workflow may still contain one uncertain inner step. Current LangChain guidance explicitly supports custom workflows that mix deterministic nodes with agentic behavior.[^custom-workflow]

## Strong closing answer

I ask, “Which exact decision cannot be predetermined?” If there is no such decision, I build ordinary code. If there is one, I confine model choice to that point, expose only the necessary tools, bound the loop, and keep authorization and side effects deterministic.

Continue with [Agent systems without chaos](../../agents/), [LangGraph](../../langgraph/), and the [Workflow glossary note](../../glossary/workflow/).

[^workflows-agents]: LangChain’s [workflows and agents guide](https://docs.langchain.com/oss/python/langgraph/workflows-agents) describes workflows as predetermined code paths and agents as feedback loops with more autonomy over tools and problem solving.
[^custom-workflow]: LangChain’s [custom workflow guide](https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow) shows deterministic and agentic components composed in the same graph.
