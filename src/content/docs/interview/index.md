---
title: AI engineering interview handbook
description: Practice 56 production questions across LLMs, RAG, evaluation, agents, LangChain, LangGraph, LLMOps, security, backend systems, and FDE judgment.
contentType: interview
level: Intermediate
minutes: 48
topics: [interview, FDE, RAG, evaluation, agents, LangChain, LangGraph, LLMOps]
lastVerified: 2026-08-16
sidebar:
  order: 1
sources:
  - title: Design and develop a RAG solution
    url: https://learn.microsoft.com/en-gb/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide
    publisher: Microsoft
    type: official-doc
  - title: Evaluate a RAG application
    url: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
    publisher: LangChain
    type: official-doc
  - title: Building effective agents
    url: https://www.anthropic.com/engineering/building-effective-agents
    publisher: Anthropic
    type: official-doc
  - title: LangGraph overview
    url: https://docs.langchain.com/oss/python/langgraph/overview
    publisher: LangChain
    type: official-doc
  - title: Model Context Protocol architecture
    url: https://modelcontextprotocol.io/specification/2026-07-28/architecture
    publisher: Model Context Protocol
    type: standard
  - title: Agent2Agent Protocol Specification 1.0.0
    url: https://a2a-protocol.org/latest/specification
    publisher: A2A Protocol Project
    type: standard
  - title: A2UI protocol versions
    url: https://a2ui.org/
    publisher: A2UI Project
    type: standard
  - title: LLM01:2025 Prompt Injection
    url: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
    publisher: OWASP GenAI Security Project
    type: standard
---

There is no reliable public ranking of AI-engineering interview frequency. Job level, company, product, and interviewer change the questions.

The questions below repeatedly test the same production skills: can you explain the system, find where it fails, name the trade-off, and prove that your change helped?

## Start with the production RAG deep dive

The table below is useful for quick practice.

When you need the full answer, open the [Production RAG interview handbook](./production-rag-interview-handbook/).

It covers 26 production questions with an answer strategy, one continuing airline scenario, code, library choices, failure cases, measurements, and follow-up questions. It also compares Pydantic AI, LangChain, and LangGraph and explains production structured-output methods.

For one focused retrieval question, read [Can RAG work without a vector database?](./rag-without-vector-database/).

## How to answer without sounding memorized

Use four moves:

1. **Answer directly.** Give the distinction or decision in one sentence.
2. **Use one example.** Make the abstract idea visible.
3. **Name the trade-off.** Explain what becomes slower, costlier, less safe, or harder to test.
4. **Explain verification.** Name the metric, test, trace, or release gate.

For example:

> Hybrid search combines keyword and semantic retrieval. BM25 protects exact identifiers such as `ERR-1042`, while vector search finds paraphrases such as “payment timed out.” I fuse both candidate lists, rerank the shortlist, and keep the design only if it improves Recall@k and task success within the latency budget.

If you have one hour, begin with questions **7, 8, 9, 11, 12, 13, 19, 20, 27, 31, 33, 39, 43, 45, and 51**.

## 1. LLMs, prompts, and context

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 1 | What does an LLM do when it generates an answer? | An LLM predicts the next token from the tokens already in its context, then repeats. Training provides broad patterns, but the application must supply current private facts, tools, and retrieved evidence. Fluent generation is not proof of correctness. | [LLM foundations](../foundations/llms/) |
| 2 | What is the difference between a token, context window, message history, and memory? | A token is a text unit. The context window is the token budget visible in one call. Message history is earlier conversation resent in that call. Memory is application data stored outside the model and retrieved later; the model does not remember an ordinary API call by itself. | [Message history and memory](../agents/message-history-and-memory/) |
| 3 | Prompt engineering versus context engineering: what changes? | Prompt engineering improves the task, constraints, examples, and output contract. Context engineering selects the instructions, files, evidence, tools, state, and history available at runtime. A strong prompt cannot use a private API definition that never entered the context. | [Prompt versus context](./prompt-vs-context-engineering/) |
| 4 | What is an embedding? | An embedding is a vector used to compare semantic relatedness. It helps retrieval find “hotel accommodation” when the user asks about a “room.” It is not an answer, probability, or truth score; the generation model still reads the retrieved text. | [Embedding](../glossary/embedding/) |
| 5 | What does temperature change? | Temperature changes how the model samples among possible next tokens, so it can affect variation. It does not add knowledge, repair retrieval, or guarantee factuality. I choose generation settings with task-level evals instead of assuming lower temperature makes every answer correct. | [LLM foundations](../foundations/llms/) |
| 6 | Long context or RAG: how do you choose? | I compare corpus size, freshness, permissions, repeated-query cost, latency, and measured answer quality. Long context can suit a small bounded document set. RAG is useful when the corpus is large, changing, attributable, or access-controlled. I test both on the same questions. | [RAG chapter](../rag/) |

## 2. Production RAG and retrieval

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 7 | Walk me through a production RAG pipeline end to end. | Ingestion parses and versions sources, preserves structure and permissions, creates searchable chunks, attaches metadata, creates embeddings, and writes keyword and vector indexes. At request time, the system authenticates, retrieves a broad authorized candidate set, fuses and reranks it, packs evidence, generates a cited answer, validates it, and records a trace. | [Full production answer](./production-rag-pipeline/) |
| 8 | Where does RAG quality usually break? | It often breaks before generation: damaged PDF parsing, missing tables, poor chunk boundaries, stale versions, wrong permission filters, query mismatch, low candidate depth, weak fusion, or context packing that drops the answer. Generation can still fail by ignoring a retrieved condition or inventing a claim. | [RAG debugging](./rag-debugging/) |
| 9 | How do you choose a chunking strategy? | I begin with the smallest answer-bearing unit that preserves a complete idea. Fixed-size chunks are simple but may cut meaning. Recursive splitting preserves separators. Structure-aware splitting follows headings and tables. Semantic splitting can preserve topic boundaries but costs more. I choose with labeled retrieval evals. | [Chunking worked example](../rag/chunking/) |
| 10 | Which metadata would you store with each chunk? | I keep a stable document ID, version, chunk ID, parent ID, source, section path, page or offsets, timestamps, tenant, ACL fields, language, and content hash. Parent-child retrieval can search small child chunks and return a larger parent section for context. Metadata must support filtering, citations, updates, and deletion. | [RAG ingestion](../rag/) |
| 11 | BM25 versus vector search: what is the difference? | BM25 rewards exact term matches using term frequency, document frequency, and length normalization. It is strong for error codes, names, and product IDs. Vector search finds semantic similarity and paraphrases. Neither is universally better; their errors differ. | [Production retrieval](../rag/production-retrieval/) |
| 12 | Why use hybrid search, and how do you combine the lists? | Hybrid search asks both keyword and vector retrievers. I can combine ranked lists with Reciprocal Rank Fusion, which rewards documents that rank well without requiring incomparable raw scores to share a scale. Then I evaluate the fused candidate set against each retriever alone. | [Hybrid retrieval and RRF](../rag/production-retrieval/) |
| 13 | What is reranking, and why is it useful? | Initial retrieval searches broadly and cheaply for recall. A reranker spends more work scoring the query against a small candidate set, then puts the strongest evidence first. It cannot recover a passage the retriever never returned, so I measure candidate recall before blaming the reranker. | [Reranking models](../ecosystem/reranking-models/) |
| 14 | What is MMR? | Maximal Marginal Relevance selects results that balance query relevance with novelty relative to already selected results. It reduces near-duplicate chunks in the final context. Too much diversity can remove useful evidence, and MMR cannot recover missed candidates. | [MMR](../glossary/mmr/) |
| 15 | When does query rewriting help or hurt? | Rewriting can resolve shorthand, spelling, or conversational references. It can also erase exact IDs, names, negation, or user intent while adding latency. I keep the original query, log both forms, and compare original-only, rewrite-only, and combined retrieval on labeled cases. | [Query rewriting](../glossary/query-rewriting/) |
| 16 | Exact vector search versus HNSW: what changes? | Exact search compares against every eligible vector and gives a quality reference. HNSW traverses a layered neighbor graph and visits a subset, trading some recall plus index memory and build cost for lower query latency. I measure ANN Recall@k against exact top-k results on the real corpus and filters. | [Vector search and HNSW](../rag/vector-search-foundations/) |
| 17 | pgvector, Pinecone, or Weaviate: how would you choose? | I start from corpus size, filters, joins, tenancy, latency, operations, recovery, and team ownership. pgvector keeps vectors beside SQL transactions and joins. Managed vector systems provide a vector-focused operating model. I benchmark on my data and avoid choosing from a generic brand ranking. | [Choosing retrieval storage](../rag/choosing-retrieval-storage/) |
| 18 | How do you handle updates, deletion, and permissions? | I use stable IDs, source versions, incremental indexing, tombstones, cache invalidation, and deletion verification across every index. Authorization is applied during retrieval with tenant and ACL filters, not after generation. Tests must prove deleted or unauthorized evidence cannot enter the context. | [Production checklist](../field-guide/production-rag-checklist/) |

## 3. RAG and LLM evaluation

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 19 | How do you evaluate a RAG system? | I use four layers. Retrieval asks whether we found the evidence. Generation asks whether the model used it correctly. End-to-end evaluation asks whether the user completed the task. Production evaluation checks latency, cost, reliability, freshness, security, and drift. I do not hide them inside one score. | [Full evaluation answer](./evaluate-rag-system/) |
| 20 | Explain Precision@k and Recall@k with denominators. | When the evaluation returns `k` ranked positions, `Precision@k = relevant results in the first k / k`. `Recall@k = relevant results in the first k / all known relevant results`. If one of three returned passages is relevant and two relevant passages exist, Precision@3 is `1/3` and Recall@3 is `1/2`. | [Evaluation chapter](../evals/) |
| 21 | What is MRR, and what does it miss? | MRR averages the reciprocal rank of the first relevant result. A first relevant hit at ranks 1, 2, and 5 gives `(1 + 1/2 + 1/5) / 3`. It rewards an early first hit but ignores later relevant evidence, so I pair it with Recall@k. | [MRR](../glossary/mrr/) |
| 22 | Faithfulness, relevance, and correctness: how do they differ? | Faithfulness compares answer claims with retrieved context. Relevance compares the answer with the user’s question. Correctness compares it with a trusted reference or known outcome. A response can answer the right topic, cite the supplied text, and still reach the wrong conclusion. | [Answer correctness](../glossary/answer-correctness/) |
| 23 | How do you evaluate citation quality? | I check more than whether a link exists. Citation precision asks whether each citation supports its attached claim. Citation coverage asks whether claims that require support have citations. I also validate source identity, version, user access, and whether the cited span survived context packing. | [Evaluation chapter](../evals/) |
| 24 | How do you build a useful evaluation dataset? | I include normal, edge, stale-source, exact-ID, unanswerable, permission-denied, and adversarial cases. Each case records expected evidence, answer or behavior, abstention rule, tags, and reviewer decision. Production failures are reviewed and added as regression cases. | [Evaluation chapter](../evals/) |
| 25 | When can you use an LLM as a judge? | I use a judge for semantic or subjective criteria that deterministic code cannot capture. I define a narrow rubric, provide examples, calibrate against human-reviewed cases, and inspect disagreement by segment. A judge is another model, not ground truth. | [RAG evaluation](./evaluate-rag-system/) |
| 26 | How do you prove version B is better than version A? | I freeze the dataset, source and permission snapshot, settings, evaluator, and production budgets. I run paired comparisons and inspect changed cases, not only averages. If several components changed together, I claim the bundle improved; I use ablations before crediting one component. | [Evaluation decisions](../evals/) |

## 4. Agents, LangChain, and LangGraph

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 27 | What is the difference between a workflow, chain, and agent? | A workflow or chain follows steps application code defines. An agent lets a model choose the next action from allowed tools and observations. I use an agent when the next useful step cannot be mapped reliably in advance, then bound tools, steps, cost, permissions, and stopping. | [Agent or workflow](./agent-vs-workflow/) |
| 28 | Explain ReAct in practical terms. | ReAct is an observation loop: decide, act through a tool, observe the result, then decide again or stop. It is useful when a result changes the next action. It needs a step limit, tool policy, trace, and a clear completion condition. | [ReAct](../glossary/react/) |
| 29 | Walk through a tool call. | The host gives the model allowed tool names, descriptions, and schemas. The model proposes a tool and arguments. Application code validates and authorizes the request, executes the function, returns a tool result, and lets the model continue. Tool selection is not authorization. | [Tool calling](../langchain/tool-calling/) |
| 30 | Why do tool descriptions and schemas matter? | The model chooses from the contract it can see. Names should be distinct, descriptions should state when to use and not use the tool, and schemas should make valid arguments easy to express. I evaluate tool choice, argument correctness, and result use on representative tasks. | [Tools and schemas](../langchain/tools-and-schemas/) |
| 31 | LangChain versus LangGraph: when would you use each? | LangChain standardizes models, messages, prompts, tools, retrieval, structured output, and runnable composition. LangGraph makes long-running state, routing, checkpoints, pause, resume, and retries explicit. They can work together; LangGraph does not require LangChain. | [LangChain](../langchain/) and [LangGraph](../langgraph/) |
| 32 | Explain state, nodes, edges, and reducers. | State is the shared typed record. Nodes are small Python functions that return state updates. Edges choose what runs next. Reducers define how multiple updates to the same key combine, which matters when branches run in parallel. | [LangGraph concepts](../langgraph/) |
| 33 | State, checkpoint, thread, store, and memory: what differs? | State is current workflow data. A checkpoint is a persisted state snapshot. A thread identifies one checkpoint history. A store holds data across threads. “Memory” is a product behavior built from selected history, state, or stored facts; it is not one LangGraph object. | [State versus memory](./langgraph-state-vs-memory/) |
| 34 | What happens when a LangGraph interrupt resumes? | `interrupt()` persists a pause through the checkpointer and returns control. The caller later resumes with a `Command`. The node restarts from its beginning, so work before the interrupt may execute again. Side effects before a pause need idempotency or placement in a separate node. | [Interrupt and resume](../langgraph/interrupts-resume/) |
| 35 | How do retries, `await`, and `sleep` differ? | `await` waits for one asynchronous operation. `asyncio.sleep()` delays an in-memory coroutine. Neither is a retry. A retry policy classifies transient exceptions, caps attempts, adds backoff and jitter, and re-runs a safe boundary. Durable waiting requires persisted state, not a sleeping process. | [Retries](../langgraph/retries-tool-failures/) |
| 36 | How do parallel branches merge safely? | Parallel nodes may return updates at the same graph step. A reducer must define how shared keys combine; otherwise concurrent writes can conflict. `Send` creates parallel calls with different inputs. I cap fan-out and make the merge deterministic and testable. | [Parallel fan-out](../langgraph/send-parallel-fanout/) |
| 37 | Two agents disagree. Which one should the system trust? | Neither until the evidence is validated. Each agent should return a structured decision, confidence, evidence, and source version. Deterministic policy resolves known priorities. A supervisor can analyze disagreement but cannot create truth; unresolved high-impact cases go to a person and an audit record. | [Agent conflict](../agents/conflict-resolution/) |
| 38 | How do you evaluate an agent? | I score the final outcome, tool selection, argument correctness, policy compliance, step efficiency, and side effects. I keep the complete trajectory and run multiple trials when output varies. Deterministic graders verify state; model judges and humans handle open-ended quality. | [Agent evaluation principles](../evals/) |

## 5. MCP, A2A, A2UI, and security

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 39 | MCP, A2A, or A2UI: how do you choose? | Choose the boundary. MCP connects an AI host to capability servers. A2A lets an independently operated agent delegate a stateful task to another agent. A2UI lets an agent describe a declarative interface that a trusted client renders. They can appear in one product. | [Protocol map](../protocols/) |
| 40 | Who controls which MCP tool may run? | The MCP server describes capabilities, but the host controls which servers and tools the model can see and what requires confirmation. Application code still authenticates the caller, validates arguments, authorizes the operation, and limits credentials and side effects. | [MCP tool selection](../agents/mcp-tool-selection/) |
| 41 | What belongs in an A2A Agent Card, and what does it not prove? | The card advertises identity, endpoints, protocol versions, capabilities, skills, media types, and authentication requirements. It supports discovery and connection setup. It is not a trust certificate; the client still verifies origin, operator, authorization, inputs, artifacts, and task results. | [A2A](../protocols/a2a/) |
| 42 | How does A2UI avoid executing arbitrary agent code? | The agent emits declarative surface, component, data, and action messages from a catalog the renderer agreed to support. The client validates them and maps them to maintained native widgets. Actions remain untrusted requests and must pass server-side authentication, authorization, and policy. | [A2UI](../protocols/a2ui/) |
| 43 | How do you stop prompt injection from causing a dangerous action? | I assume the model may follow instructions hidden in email, documents, or tool results. I limit consequences with retrieval-time authorization, narrow typed tools, deterministic data-sharing rules, least-privilege credentials, confirmation for high-impact actions, and audit records. A stronger system prompt is not the security boundary. | [Prompt-injection boundaries](../security/prompt-injection/) |
| 44 | How do you secure a multi-tenant AI application? | Bind identity and tenant at the application boundary. Apply ACL filters before retrieval, scope caches and memory by tenant and authorization, minimize tool credentials, validate every resource access, and test leakage directly. Never ask the model to decide whether one customer may read another customer’s data. | [Production checklist](../field-guide/production-rag-checklist/) |

## 6. LLMOps, backend systems, latency, and cost

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 45 | Trace, metric, evaluation, and audit record: what differs? | A trace explains one request and its spans. A metric aggregates behavior over time. An evaluation judges output against a defined criterion. An audit record captures identity, authorization, approval, and consequential actions. One platform may store all four, but the meanings remain separate. | [LLMOps](../llmops/) |
| 46 | What would you monitor in production? | I record request and trace IDs, route, tenant class, model, prompt, tool and index versions, retrieved IDs, scores, final-context reference, citations, tokens, cost, retries, errors, and per-stage p50/p95/p99 latency. Quality monitoring samples task success, faithfulness, abstention, and feedback. | [LLMOps](../llmops/) |
| 47 | How do you reduce latency and cost without hiding quality loss? | I profile each stage first. Then I test parallel independent retrieval, smaller measured candidate sets, selective reranking, batching, safe caching, prompt and context reduction, model routing, and streaming for perceived latency. I compare cost per successful task, not cost per raw request. | [Production RAG checklist](../field-guide/production-rag-checklist/) |
| 48 | When is semantic caching unsafe? | Semantic similarity does not prove answer equivalence. I avoid caching side effects, permission-sensitive data, conversation-dependent answers, and fast-changing facts. Safe entries are scoped by tenant, authorization, locale, source, prompt, and model version, with invalidation and false-hit tests. | [Semantic caching](../llmops/semantic-caching/) |
| 49 | Why does idempotency matter for AI tools? | A timeout can happen after an external side effect succeeded but before the agent received the result. Retrying may send the email, payment, or ticket twice. I use an idempotency key, check external status before retry, and separate side-effecting nodes from retryable read work. | [Tool failures](../langgraph/retries-tool-failures/) |
| 50 | How would you design a FastAPI boundary for an AI feature? | I use typed request and response schemas, authenticated dependencies, tenant binding, explicit timeouts, cancellation handling, bounded concurrency, rate limits, and structured errors. Streaming needs disconnect handling. Long work should return a job ID rather than holding an HTTP request indefinitely. | [Applied AI roadmap](../foundations/applied-ai-roadmap/) |

## 7. FDE and system-design judgment

| # | Interview question | Interview-ready answer | Go deeper |
| ---: | --- | --- | --- |
| 51 | The demo looks good. What makes it production-ready? | I define the user task and failure cost, build a reviewed eval set, enforce identity and permissions, add abstention and human escalation, test adversarial cases, set quality and operational release gates, trace every stage, verify deletion and freshness, and write an operator runbook. A polished demo proves only the happy path. | [Production checklist](../field-guide/production-rag-checklist/) |
| 52 | The customer has no labeled data. What do you do? | I do not pretend a demo score is evidence. I begin with a small set of real questions reviewed by domain experts, record acceptable evidence and behavior, include risky negatives, and use production feedback to grow the set. Five trustworthy cases are more useful than hundreds of unreviewed synthetic ones. | [Evaluation dataset](../evals/) |
| 53 | How do you choose build versus buy? | I separate commodity capability from domain control. I compare time to value, data handling, integration, exportability, reliability, cost at expected volume, team skills, and exit cost. I keep business rules and data contracts behind adapters so a vendor decision remains reversible. | [AI library map](../ecosystem/) |
| 54 | Quality improves but p95 latency gets worse. How do you frame the decision? | I show paired results by user segment and task risk. Then I identify where latency increased and offer options: selective reranking, a faster route for low-risk cases, async work, or a different SLO. The product owner chooses from measured quality, latency, cost, and risk, not one average. | [LLMOps](../llmops/) |
| 55 | What questions do you ask before proposing an architecture? | I ask who the user is, what decision or action they need, which data is authoritative, how permissions work, what errors cost, which steps are deterministic, what latency and volume are expected, what must be logged, and who operates the system. Architecture follows these answers. | [Applied AI roadmap](../foundations/applied-ai-roadmap/) |
| 56 | What should an FDE hand over? | I hand over architecture and trust boundaries, source and configuration ownership, deployment and rollback steps, eval datasets and gates, dashboards and alerts, incident procedures, data deletion paths, known limitations, cost assumptions, and a named owner for each operational decision. | [Projects and acceptance](../projects/) |

## A final practice rule

Do not memorize every sentence.

Choose one example system—such as an airline policy assistant, support assistant, or incident investigator—and reuse it. The interviewer can then see how ingestion, retrieval, tools, permissions, evaluation, latency, and operations connect inside one product.

Practice the full answers:

- [Production RAG interview handbook](./production-rag-interview-handbook/)
- [Production RAG pipeline](./production-rag-pipeline/)
- [RAG without a vector database](./rag-without-vector-database/)
- [RAG evaluation](./evaluate-rag-system/)
- [RAG debugging](./rag-debugging/)
- [Agent versus workflow](./agent-vs-workflow/)
- [LangGraph production questions](./langgraph-production-questions/)
- [LangGraph state versus memory](./langgraph-state-vs-memory/)
- [Prompt versus context engineering](./prompt-vs-context-engineering/)
