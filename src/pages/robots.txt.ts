import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
	const configuredBase = import.meta.env.BASE_URL;
	const basePath = configuredBase.endsWith('/') ? configuredBase : `${configuredBase}/`;
	const sitemapUrl = new URL(
		`${basePath}sitemap-index.xml`,
		site ?? new URL('https://fde101.example'),
	);

	return new Response(`User-agent: *\nAllow: ${basePath}\nSitemap: ${sitemapUrl.href}\n`, {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
