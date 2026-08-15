---
title: RetryPolicy and tool failures
description: Classify failures, let retryable exceptions escape, and retry the whole node with bounded backoff.
contentType: glossary
level: Advanced
minutes: 9
topics: [LangGraph, RetryPolicy, ToolNode, backoff, errors]
lastVerified: 2026-08-15
sidebar:
  order: 19
sources:
  - title: Fault tolerance
    url: https://docs.langchain.com/oss/python/langgraph/fault-tolerance
    publisher: LangChain
    type: official-doc
  - title: ToolNode API reference
    url: https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode
    publisher: LangChain
    type: official-doc
  - title: Thinking in LangGraph — error handling
    url: https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph
    publisher: LangChain
    type: official-doc
---

**`RetryPolicy` re-runs a failed node attempt when its exception matches `retry_on`.** It waits between attempts with bounded exponential backoff and jitter; you do not add `sleep()` yourself.[^fault]

## The exact tool-failure call chain

```text
model emits tool call
  → tools_condition routes to "tools"
  → ToolNode validates arguments
  → ToolNode invokes the tool
  → tool raises a transient execution error
  → default ToolNode re-raises it
  → exception escapes the "tools" node
  → RetryPolicy classifies it
  → LangGraph waits, then reruns the whole node attempt
  → after exhaustion: error_handler runs, or the error bubbles to the caller
```

The retry boundary is the node. A broad `try/except` in the tool node, or `ToolNode(handle_tool_errors=True)`, can turn the exception into a normal `ToolMessage`. Then `RetryPolicy` has nothing to retry.

## Tiny policy

```python
from langgraph.types import RetryPolicy

class TransientToolError(Exception):
    pass

retry_transient = RetryPolicy(
    max_attempts=3,       # first attempt + at most two retries
    initial_interval=0.5,
    backoff_factor=2.0,
    max_interval=4.0,
    jitter=True,
    retry_on=TransientToolError,
)

builder.add_node(
    "tools",
    ToolNode([lookup_order]),
    retry_policy=retry_transient,
)
```

The planned waits begin around 0.5 and 1.0 seconds before jitter, capped by `max_interval`. LangGraph's current defaults are three total attempts, 0.5-second initial interval, factor 2, 128-second cap, and jitter enabled.[^fault]

## Classify before retrying

| Failure | Retry? | Owner |
| --- | ---: | --- |
| Bad tool arguments from the model | No system retry | Return error `ToolMessage`; let model correct once within its loop budget |
| Network interruption, rate limit, upstream 5xx | Usually, bounded | `RetryPolicy` with explicit exception or predicate |
| `NodeTimeoutError` | Usually, bounded | Timeout raises; retry policy evaluates it |
| Authentication, authorization, policy denial | No | Stop safely or request corrected access |
| Unknown programming error | No automatic retry | Bubble, trace, alert, fix |
| Still failing after attempts | No more retries | Error handler, fallback, or human review |

Node-level `error_handler=` runs only after retries are exhausted and requires LangGraph 1.2 or later. It can return `Command(goto="human_review")`. If the handler raises, that error bubbles.

## Failure note

The whole failed node attempt runs again. A tool that creates a payment, ticket, email, or record must use an idempotency key or check the remote system before writing. Never automatically retry an operation whose repeat effect is unknown.

## Related

- [`ToolNode` and `tools_condition`](../toolnode-tools-condition/)
- [Async waiting and timeouts](../async-waiting-timeouts/)
- [Interrupt and resume](../interrupts-resume/)
- [Durability modes](../durability/)

[^fault]: LangChain, [Fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance).
