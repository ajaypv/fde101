---
title: Agent to UI Protocol (A2UI)
description: A protocol for streaming declarative interfaces that trusted clients validate and render with native components.
contentType: glossary
level: Intermediate
minutes: 4
topics: [A2UI, generative UI, component catalogs]
lastVerified: 2026-08-15
sidebar:
  order: 8
sources:
  - title: A2UI Protocol v0.9.1
    url: https://a2ui.org/specification/v0.9.1-a2ui/
    publisher: A2UI Project
    type: standard
---

The **Agent to UI Protocol**, or **A2UI**, lets an agent describe an interactive interface as declarative JSON. A trusted client validates the description and renders its own web, mobile, or desktop components.

```text
agent → surface and component messages → trusted renderer → native UI
user  → action event → authenticated application server
```

The important pieces are:

- a **surface**, the named UI area;
- a **component catalog**, the allowed vocabulary and schema;
- **components**, a flat list connected by IDs;
- a separate **data model** and JSON Pointer bindings;
- **actions**, which report user interaction.

A2UI does not make an action authorized. The server treats every action name and context value as untrusted input and applies normal authentication, permission, validation, and approval rules.

As checked on 15 August 2026, A2UI 0.9.1 is the current production release and 1.0 remains a candidate. See the full [A2UI lesson](../../protocols/a2ui/).
