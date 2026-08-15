---
title: Message roles
description: Labels that separate instructions, user input, model output, and tool results in a conversation.
contentType: glossary
level: Beginner
minutes: 3
topics: [message roles, prompts, tool calling]
lastVerified: 2026-08-15
sidebar:
  order: 15
---

**Message roles** tell a model where each part of a conversation came from. Common roles include system, user, assistant, and tool.

## Tiny example

```text
system:    Answer from approved policy only.
user:      What is the refund period?
tool:      Policy 7 says 30 days.
assistant: The refund period is 30 days. [Policy 7]
```

Roles preserve structure, but they do not prove that content is trustworthy.

## FDE note

Do not concatenate every value into one giant string when the model API supports structured messages. Keep tool outputs and user-provided content clearly separated, and validate both before use.
