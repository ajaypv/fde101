---
title: Thread
description: An identifier that groups the checkpoints and state history of one workflow instance.
contentType: glossary
level: Intermediate
minutes: 3
topics: [thread, persistence, LangGraph]
lastVerified: 2026-08-15
sidebar:
  order: 23
---

A **thread** is the identity used to group saved state for one conversation, task, or workflow run. A checkpointer uses the thread ID to load the correct history when execution continues.

## Tiny example

```text
thread: support-case-1842
  checkpoint 1 → question received
  checkpoint 2 → evidence retrieved
  checkpoint 3 → waiting for reviewer
```

This is an application-level identity. It is not an operating-system thread and does not itself provide concurrency or security.

## FDE note

Generate thread IDs server-side or verify ownership before every read and write. Define retention and deletion behavior, because a thread can contain user messages, retrieved data, and tool results.
