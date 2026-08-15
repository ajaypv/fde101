---
title: Agent2Agent Protocol (A2A)
description: A protocol for discovery and stateful task exchange between independently built agent systems.
contentType: glossary
level: Intermediate
minutes: 4
topics: [A2A, agents, interoperability]
lastVerified: 2026-08-15
sidebar:
  order: 6
sources:
  - title: Agent2Agent Protocol Specification 1.0.0
    url: https://a2a-protocol.org/latest/specification
    publisher: A2A Protocol Project
    type: standard
---

The **Agent2Agent Protocol**, or **A2A**, gives independently deployed agent systems a shared contract for discovery, messages, stateful tasks, updates, and task outputs.

## Tiny example

```text
airline assistant (A2A client)
          ↓ delegates policy review
passenger-care agent (A2A server)
          ↓ returns task updates and an artifact
airline assistant
```

The remote agent may use any framework, prompt, tools, or model internally. A2A exposes the interaction boundary without requiring either side to reveal that implementation.

## Remember the boundary

- **Agent Card:** what the remote agent claims to offer and how to connect.
- **Message:** one communication turn made of typed parts.
- **Task:** stateful work with a lifecycle.
- **Artifact:** the concrete result of a task.

A2A does not make a discovered agent trustworthy. The client still verifies identity, authenticates, authorizes each operation, validates artifacts, and records the exchange.

Continue with the full [A2A lesson](../../protocols/a2a/) or compare [MCP, A2A, and A2UI](../../protocols/).
