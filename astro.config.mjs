// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

const site = process.env.SITE_URL ?? 'https://fde101.example';

// https://astro.build/config
export default defineConfig({
	site,
	integrations: [
		starlight({
			title: 'FDE 101',
			description: 'A practical field guide to LLMs, RAG, agents, evaluation, and delivery.',
			favicon: '/favicon.svg',
			customCss: ['@fontsource-variable/newsreader/wght.css', './src/styles/book.css'],
			lastUpdated: true,
			pagefind: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			head: [
				{ tag: 'meta', attrs: { name: 'theme-color', content: '#f7f3e9' } },
				{ tag: 'link', attrs: { rel: 'sitemap', href: '/sitemap-index.xml' } },
			],
			sidebar: [
				{
					label: 'Start here',
					items: [{ label: 'How to use this book', slug: 'start-here' }],
				},
				{ label: 'Foundations', items: [{ autogenerate: { directory: 'foundations' } }] },
				{ label: 'RAG', items: [{ autogenerate: { directory: 'rag' } }] },
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
