---
title: Memory
description: Application-managed information preserved and supplied across model calls or conversations.
contentType: glossary
level: Beginner
minutes: 3
topics: [memory, context, state]
lastVerified: 2026-08-15
sources:
  - title: Memory overview
    url: https://docs.langchain.com/oss/python/concepts/memory
    publisher: LangChain
    type: official-doc
---

**Memory** in an AI application is information the application saves and later supplies to a model or workflow. It is not one automatic capability inside every model call.

## Tiny example

Conversation history keeps recent messages for one thread. A long-term store keeps an approved language preference across threads. A checkpoint saves workflow state so an interrupted job can resume.

## FDE note

Name the lifecycle precisely: context, history, state, checkpoint, summary, or long-term store. Each needs its own scope, retention, access, correction, and deletion policy. Read [message history is not durable memory](../../agents/message-history-and-memory/).
