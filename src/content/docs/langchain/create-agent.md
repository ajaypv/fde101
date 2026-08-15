---
title: create_agent
description: Build LangChain's standard model-and-tools loop when the next action cannot be fixed in advance.
contentType: lesson
level: Intermediate
minutes: 6
topics: [LangChain, agents, create_agent]
lastVerified: 2026-08-15
sidebar:
  order: 12
sources:
  - title: Agents
    url: https://docs.langchain.com/oss/python/langchain/agents
    publisher: LangChain
    type: official-doc
---

`create_agent()` builds a LangGraph-backed loop: call the model, run requested tools, return their results, and repeat until the model gives a final response or a stop condition is reached.

## Tiny example

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[get_order_status],
    system_prompt="Help support staff. Never invent order state.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Where is order A-19?"}]
})
print(result["messages"][-1].text)
```

## Agent or fixed chain?

| Situation | Start with |
| --- | --- |
| The steps are known: validate → fetch → format | Normal Python or a fixed chain |
| The model must choose among several read-only searches | Agent |
| A payment, deletion, or external message needs approval | Deterministic policy plus human approval |

## Failure note

An agent is a loop, so set tool-call limits, timeouts, and cost budgets. Conversation persistence requires a checkpointer and a stable thread ID; `create_agent()` does not make a stateless model remember previous requests by itself.

## Related

[Tool calling](../tool-calling/) · [Middleware](../middleware/) · [LangGraph](../../langgraph/)
