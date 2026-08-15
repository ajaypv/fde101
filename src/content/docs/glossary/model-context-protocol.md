---
title: Model Context Protocol (MCP)
description: An open protocol for connecting AI applications to external tools, resources, and prompts.
contentType: glossary
level: Intermediate
minutes: 4
topics: [MCP, tools, integrations]
lastVerified: 2026-08-15
sidebar:
  order: 20
sources:
  - title: Introduction to Model Context Protocol
    url: https://modelcontextprotocol.io/docs/getting-started/intro
    publisher: Model Context Protocol
    type: official-doc
---

The **Model Context Protocol**, or **MCP**, is an open protocol for connecting AI applications to external systems. An MCP server can expose capabilities such as tools, resources, and reusable prompts to an MCP client.

## Tiny example

```text
AI application (MCP client)
        ↓ discovers tools
customer-data MCP server
        ↓ calls approved API
customer system
```

MCP standardizes the connection and message exchange. It does not automatically make a server, tool, or returned value safe or trustworthy.

## FDE note

Treat every server as an integration boundary. Review authentication, user consent, tool permissions, data exposure, timeouts, and audit logging before enabling it.
