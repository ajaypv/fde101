# FDE 101

A quiet, code-first field guide for forward-deployed engineers learning LLMs, RAG, LangChain, LangGraph, evaluation, and production delivery.

## Run locally

```powershell
pnpm install
pnpm dev
```

Create a production build with `pnpm build` and inspect it with `pnpm preview`.

Standalone listings under `src/examples/` require Python 3.10 or newer. On Windows, activate a Python 3 virtual environment and confirm `python --version` before using `python`. On macOS or Linux, use `python3` and check `python3 --version`.

## Content model

- `src/content/docs/` contains the book chapters, glossary, field guide, and interview questions.
- `src/examples/` contains complete code listings imported into MDX so displayed code and repository code cannot drift apart.
- `src/components/` contains small editorial components such as concept flows and takeaways.
- `src/styles/book.css` contains the paper-and-ink reading system, responsive layout, accessibility focus states, and print rules.

Each chapter has a unique title and description plus structured topics, verification date, and optional source metadata. Add citations next to the claim they support, preferring official documentation and primary sources.

## Deployment and SEO

Set `SITE_URL` to the public origin before building:

```powershell
$env:SITE_URL='https://your-domain.example'
pnpm build
```

The build generates canonical metadata through Starlight, a sitemap, `robots.txt`, Pagefind search data, and static HTML for every chapter.

## Add a chapter

1. Add a Markdown or MDX file under `src/content/docs/`.
2. Include `title`, `description`, `contentType`, `topics`, and `lastVerified` in frontmatter.
3. Put full examples in `src/examples/` and import them with `?raw` into MDX.
4. Cite authoritative sources in the paragraph or footnote where they are used.
5. Run `pnpm build` before review.
