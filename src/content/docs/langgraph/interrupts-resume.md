---
title: Interrupt and resume
description: A persisted pause for approval, clarification, or another external decision.
contentType: glossary
level: Intermediate
minutes: 6
topics: [LangGraph, interrupt, Command, human-in-the-loop]
lastVerified: 2026-08-15
sidebar:
  order: 17
sources:
  - title: Interrupts
    url: https://docs.langchain.com/oss/python/langgraph/interrupts
    publisher: LangChain
    type: official-doc
---

**`interrupt()` pauses the graph and exposes a JSON-serializable request to the caller. Resume the same checkpoint with `Command(resume=...)` and the same `thread_id`.**[^interrupts]

## Tiny example

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

def approve_refund(state: RefundState) -> dict:
    approved = interrupt({"question": "Approve £450 refund?"})
    return {"approved": bool(approved)}

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "refund-104"}}

paused = graph.invoke({"amount": 450}, config)
finished = graph.invoke(Command(resume=True), config)
```

1. Node calls `interrupt()`.
2. LangGraph saves the pause through the checkpointer.
3. The application shows the request to a reviewer.
4. The application resumes the same thread.
5. The resume value becomes the return value of `interrupt()`.

## Failure note

On resume, LangGraph restarts the node from its beginning. Code before `interrupt()` runs again. Put side effects after approval, move them to another node, or make them idempotent. Do not wrap `interrupt()` in a broad `try/except`; it uses a special exception to reach the runtime.

## Related

- [Checkpoints and threads](../checkpoints-threads/)
- [`Command`](../command/)
- [Async waiting and timeouts](../async-waiting-timeouts/)

[^interrupts]: LangChain, [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts).
