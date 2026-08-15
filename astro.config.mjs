// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

const [githubOwner, githubRepository] = (process.env.GITHUB_REPOSITORY ?? '').split('/');
const isGitHubPages = process.env.GITHUB_ACTIONS === 'true' && githubOwner && githubRepository;
const configuredBase = process.env.BASE_PATH ?? (isGitHubPages ? `/${githubRepository}` : '');
const base = configuredBase ? `/${configuredBase.replace(/^\/+|\/+$/g, '')}` : undefined;
const basePath = base ?? '';
const site =
	process.env.SITE_URL ??
	(isGitHubPages ? `https://${githubOwner}.github.io` : 'https://fde101.example');

// https://astro.build/config
export default defineConfig({
	site,
	base,
	integrations: [
		starlight({
			title: 'FDE 101',
			description: 'A practical field guide to LLMs, RAG, agents, evaluation, and delivery.',
			favicon: '/favicon.svg',
			customCss: [
				'@fontsource-variable/source-serif-4/wght.css',
				'@fontsource-variable/source-sans-3/wght.css',
				'./src/styles/book.css',
			],
			lastUpdated: true,
			pagefind: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			head: [
				{
					tag: 'meta',
					attrs: { name: 'theme-color', content: '#ffffff', media: '(prefers-color-scheme: light)' },
				},
				{
					tag: 'meta',
					attrs: { name: 'theme-color', content: '#000000', media: '(prefers-color-scheme: dark)' },
				},
				{ tag: 'link', attrs: { rel: 'sitemap', href: `${basePath}/sitemap-index.xml` } },
			],
			sidebar: [
				{
					label: 'Start here',
					items: [{ label: 'How to use this book', slug: 'start-here' }],
				},
				{ label: 'Foundations', items: [{ autogenerate: { directory: 'foundations' } }] },
				{ label: 'RAG', items: [{ autogenerate: { directory: 'rag' } }] },
				{ label: 'Agent systems', items: [{ autogenerate: { directory: 'agents' } }] },
				{
					label: 'Frameworks',
					items: [
						{ label: 'LangChain', slug: 'langchain' },
						{ label: 'LangGraph', slug: 'langgraph' },
					],
				},
				{ label: 'Evaluation', items: [{ autogenerate: { directory: 'evals' } }] },
				{ label: 'FDE field guide', items: [{ autogenerate: { directory: 'field-guide' } }] },
				{
					label: 'Interview room',
					collapsed: true,
					items: [{ autogenerate: { directory: 'interview' } }],
				},
				{
					label: 'Glossary',
					collapsed: true,
					items: [{ autogenerate: { directory: 'glossary' } }],
				},
			],
		}),
		sitemap(),
	],
});
