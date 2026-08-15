---
title: bind_tools, tool calls, and ToolMessage
description: Follow one tool request from model output through execution and back into model context.
contentType: lesson
level: Intermediate
minutes: 6
topics: [LangChain, bind_tools, ToolMessage]
lastVerified: 2026-08-15
sidebar:
  order: 11
sources:
  - title: Models - tool calling
    url: https://docs.langchain.com/oss/python/langchain/models#tool-calling
    publisher: LangChain
    type: official-doc
  - title: Messages - ToolMessage
    url: https://docs.langchain.com/oss/python/langchain/messages#tool-message
    publisher: LangChain
    type: official-doc
---

`bind_tools()` tells a chat model which tool schemas are available. The model may return requests in `AIMessage.tool_calls`; it does not execute those Python functions by itself.

## The four-step loop

```python
model_with_tools = model.bind_tools([get_order_status])
messages = [{"role": "user", "content": "Where is order A-19?"}]

# 1. Ask the model which action it wants.
ai_message = model_with_tools.invoke(messages)
messages.append(ai_message)

# 2. Validate and execute each request.
for tool_call in ai_message.tool_calls:
    # 3. Tool.invoke(tool_call) returns a matching ToolMessage.
    messages.append(get_order_status.invoke(tool_call))

# 4. Let the model read the result and answer.
answer = model_with_tools.invoke(messages)
```

A `ToolMessage.tool_call_id` must match the originating call ID. That pairing matters when the model requests more than one tool.

## Failure note

Binding a tool grants the model a vocabulary, not permission. Validate every argument and enforce access at execution time. If you create `ToolMessage` manually, mismatched or missing call IDs can break the conversation. An agent automates this loop, but the same security boundary remains.

## Related

[Tools and schemas](../tools-and-schemas/) · [`create_agent`](../create-agent/) · [Retries and backoff](../retries-backoff/)
