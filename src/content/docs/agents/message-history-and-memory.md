---
title: Message history is not durable memory
description: Separate one-call context, conversation history, graph state, checkpoints, summaries, and long-term memory.
contentType: lesson
level: Beginner
minutes: 11
topics: [memory, message history, state, LangGraph]
lastVerified: 2026-08-15
sidebar:
  order: 2
sources:
  - title: Conversation state
    url: https://developers.openai.com/api/docs/guides/conversation-state
    publisher: OpenAI
    type: official-doc
  - title: LangGraph persistence
    url: https://docs.langchain.com/oss/python/langgraph/persistence
    publisher: LangChain
    type: official-doc
  - title: Memory overview
    url: https://docs.langchain.com/oss/python/concepts/memory
    publisher: LangChain
    type: official-doc
---

For one model call, the model can use only the context supplied to that call. Your application—or a provider-managed conversation service—decides what to save and supply next time.[^conversation]

## One tiny conversation

```python
history = [{"role": "user", "content": "My name is Maya."}]
history.append({"role": "assistant", "content": call_model(history)})

history.append({"role": "user", "content": "What is my name?"})
answer = call_model(history[-20:])
```

The second request contains the earlier message, so the model can answer “Maya.” The Python list is the application's memory mechanism. The model did not update its weights or privately remember Maya between calls.

Some APIs can store conversation objects or link responses for you. That changes who manages the state, not what the model can infer from the context it receives.

## Six things often called memory

| Concept | Plain meaning | Support-assistant example |
| --- | --- | --- |
| Model context | Tokens supplied to this call | Current question, instructions, and retrieved policy |
| Message history | Stored transcript of prior turns | User and assistant messages from this chat |
| Working context | The selected part of history sent now | Last 20 messages plus a running summary |
| Structured state | Fields the workflow reads and updates | Account ID, current step, tool results, retry count |
| Checkpoint | Persisted snapshot of state | State immediately before a human approval |
| Long-term store | Approved information available across threads | The user's saved language preference |

LangGraph persists thread-scoped state through checkpointers and uses a store for application-defined information shared across threads.[^persistence] A message list may be part of state, but state can also contain values that should never be shown to the model.

## More history is not always better

Raw conversation history grows until it is expensive, distracting, or too large for the context window. Common policies are:

```text
recent window     keep the last N turns
filter            remove irrelevant tool chatter
summary           compress older turns
structured state  extract durable facts into typed fields
retrieval         fetch only memories relevant to this request
```

Each policy can lose information. A summary can silently change a customer number; a recent window can drop the instruction that governs the current task. Test long and branching conversations, not only two-turn demos.

## Persistence is a product decision

Before storing a “memory,” answer:

- Did the user consent to retaining it?
- Is it scoped to a thread, user, tenant, or organization?
- Who can read, correct, and delete it?
- How long is it retained and encrypted?
- Can untrusted content write durable instructions?
- What happens when a summary or extracted fact is wrong?

Do not automatically convert every conversation sentence into long-term memory. Save the smallest approved fact with provenance and an expiration or deletion policy.

Next: compare [state, checkpoints, threads, and stores](../../interview/langgraph-state-vs-memory/) or build a [durable LangGraph workflow](../../langgraph/).

[^conversation]: OpenAI, [conversation state](https://developers.openai.com/api/docs/guides/conversation-state), distinguishes manually supplied history, linked responses, and durable conversation objects.
[^persistence]: LangChain, [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) and [memory overview](https://docs.langchain.com/oss/python/concepts/memory).
