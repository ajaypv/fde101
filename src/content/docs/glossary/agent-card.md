---
title: Agent Card
description: An A2A discovery document describing a remote agent's interfaces, skills, capabilities, media types, and authentication requirements.
contentType: glossary
level: Intermediate
minutes: 4
topics: [A2A, Agent Card, discovery]
lastVerified: 2026-08-15
sidebar:
  order: 7
sources:
  - title: Agent2Agent Protocol Specification 1.0.0
    url: https://a2a-protocol.org/latest/specification
    publisher: A2A Protocol Project
    type: standard
---

An **Agent Card** is the JSON discovery document published by an A2A server. A client can fetch it from `https://{agent-domain}/.well-known/agent-card.json`.

## Read it like a business card

| Field group | Question it answers |
| --- | --- |
| Identity and provider | Who claims to operate this agent? |
| Supported interfaces | Which URL, binding, and A2A version can I use? |
| Capabilities | Does it support streaming, push updates, or an extended card? |
| Security declarations | How must the client authenticate? |
| Skills and media modes | What work and content types does it claim to handle? |

The card supports discovery and connection setup. It does not prove that the agent is accurate, safe, approved for this tenant, or entitled to receive the user's data.

Optional JWS signatures can protect card integrity and identify a signer. The application must still trust the signer, verify the runtime endpoint, and authorize the requested work.

See an annotated card in the full [A2A lesson](../../protocols/a2a/).
