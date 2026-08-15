---
title: Checkpoint
description: A persisted snapshot of workflow state that supports resuming or inspecting an execution.
contentType: glossary
level: Intermediate
minutes: 3
topics: [checkpoint, persistence, LangGraph]
lastVerified: 2026-08-15
sidebar:
  order: 22
---

A **checkpoint** is a saved snapshot of workflow state at a particular step. It can let a system resume after interruption, inspect history, or pause for human approval.

## Tiny example

A support workflow saves state after drafting a refund. A reviewer approves it later, and execution resumes from that checkpoint instead of repeating every previous model and tool call.

## Important limit

Restoring state does not undo or safely repeat external side effects such as sending an email or charging a card.

## FDE note

Use idempotency keys for side effects, define checkpoint retention, encrypt sensitive state, and test resumes across application-version changes.
