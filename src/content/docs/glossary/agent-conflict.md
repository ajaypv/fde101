---
title: Agent conflict
description: A disagreement between specialist agent findings caused by different roles, evidence, instructions, or data state.
contentType: glossary
level: Beginner
minutes: 4
topics: [multi-agent, conflict resolution, human review]
lastVerified: 2026-08-15
sidebar:
  order: 44
sources:
  - title: AI Risk Management Framework Core
    url: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
    publisher: NIST
    type: standard
---

**Agent conflict** occurs when specialist agents return findings that point toward different actions.

## Tiny example

```text
eligibility finding: income and credit checks pass
fraud finding:       a recent transaction needs investigation
```

Both findings can accurately describe their evidence while the overall case remains unresolved.

## FDE note

Do not choose the most confident agent or assume a majority vote creates truth. Validate source evidence, apply deterministic priority rules, and escalate when the policy or evidence does not support an automatic action. Record the findings, evidence IDs, versions, policy, reviewer, and final reason.

Continue with [When agents disagree, resolve evidence—not votes](../../agents/conflict-resolution/).
