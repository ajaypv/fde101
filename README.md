# FDE 101

> A practical fieldbook for forward-deployed engineers building reliable AI systems.

[Read the book](https://ajaypv.github.io/fde101/) · [Start here](https://ajaypv.github.io/fde101/start-here/) · [Practice interview questions](https://ajaypv.github.io/fde101/interview/) · [Use the production checklist](https://ajaypv.github.io/fde101/field-guide/production-rag-checklist/)

[![Deploy to GitHub Pages](https://github.com/ajaypv/fde101/actions/workflows/deploy.yml/badge.svg)](https://github.com/ajaypv/fde101/actions/workflows/deploy.yml)

FDE 101 explains the systems around an LLM: context, retrieval, tools, orchestration, evaluation, security, observability, and delivery. Chapters use short explanations, concrete comparisons, citations, and complete code listings that you can inspect in the repository.

The material is written for software engineers, forward-deployed engineers, and interview candidates who want to move from a working demo to an operable production system.

## What is inside

| Area | Questions the book answers |
| --- | --- |
| Foundations | What does an LLM receive, what belongs in context, and when should you fine-tune? |
| Production RAG | How should you parse, chunk, retrieve, rerank, cite, abstain, and debug? |
| Agents and MCP | When should a model choose a tool, and where must deterministic controls remain? |
| LangChain | How do messages, models, tools, retrievers, runnables, middleware, and structured output fit together? |
| LangGraph | How do state, reducers, edges, checkpoints, interrupts, retries, streaming, and subgraphs work? |
| Evaluation and LLMOps | How do you measure retrieval and generation separately, gate releases, and reproduce failures? |
| Security | How do authorization, least privilege, approval, and prompt-injection defenses constrain a model? |
| FDE practice | How do you design projects, explain trade-offs, and answer production interview questions? |

## Suggested reading paths

### Learn production RAG

1. [RAG, end to end](https://ajaypv.github.io/fde101/rag/)
2. [Vector search foundations](https://ajaypv.github.io/fde101/rag/vector-search-foundations/)
3. [Production retrieval](https://ajaypv.github.io/fde101/rag/production-retrieval/)
4. [Evaluation](https://ajaypv.github.io/fde101/evals/)
5. [Production RAG checklist](https://ajaypv.github.io/fde101/field-guide/production-rag-checklist/)

### Learn agents and LangGraph

1. [Agent systems without chaos](https://ajaypv.github.io/fde101/agents/)
2. [LangGraph](https://ajaypv.github.io/fde101/langgraph/)
3. [Message history and memory](https://ajaypv.github.io/fde101/agents/message-history-and-memory/)
4. [Prompt-injection boundaries](https://ajaypv.github.io/fde101/security/prompt-injection/)
5. [Agent-versus-workflow interview answer](https://ajaypv.github.io/fde101/interview/agent-vs-workflow/)

### Prepare for interviews

Start in the [interview room](https://ajaypv.github.io/fde101/interview/). Practice defining the concept, giving a small example, naming the trade-off, and explaining how you would verify the result.

## Editorial principles

- Start with the smallest honest implementation.
- Separate retrieval failures from generation failures.
- Keep permissions, calculations, and consequential actions in deterministic code.
- Add complexity only after an evaluation identifies a specific failure.
- Put citations next to the claims they support.
- Prefer provider-neutral examples unless a vendor API teaches an important contract.

## Run locally

The repository pins `pnpm@10.10.0`. Use pnpm rather than npm.

```powershell
pnpm install
pnpm dev
```

Open the local URL printed by Astro. Create and inspect a production build with:

```powershell
pnpm build
pnpm preview
```

Standalone listings under `src/examples/` require Python 3.10 or newer. They are educational examples; the documentation site itself does not require Python.

## Repository map

```text
src/
├── content/docs/   Book chapters, glossary notes, field guides, and interviews
├── examples/       Complete code listings imported into the chapters
├── components/     Small editorial and navigation components
└── styles/         Paper-and-ink typography, responsive layout, and print rules
```

Code examples are imported into MDX with `?raw`, so the code shown in a chapter is the same file that can be checked or executed from `src/examples/`.

## Add or update a chapter

1. Add a Markdown or MDX file under `src/content/docs/`.
2. Include a unique `title`, `description`, `contentType`, `topics`, and `lastVerified` value in its frontmatter.
3. Put complete examples under `src/examples/` and import them into MDX with `?raw`.
4. Cite official documentation or primary sources beside the claim they support.
5. Run `pnpm build` before review.

## Deployment

Every push to `main` runs [the GitHub Pages workflow](./.github/workflows/deploy.yml). The Astro configuration derives the Pages base path from `GITHUB_REPOSITORY`, builds static HTML, generates the sitemap, and creates Pagefind search data.

For a custom deployment, set `SITE_URL` to the public origin. Set `BASE_PATH` only when the site is served from a subpath.

```powershell
$env:SITE_URL='https://docs.example.com'
pnpm build
```

Package installation uses pnpm with the official npm registry configured in [`.npmrc`](./.npmrc).
