import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro/zod';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			extend: z.object({
				contentType: z
					.enum(['lesson', 'glossary', 'interview', 'field-guide', 'landing'])
					.default('lesson'),
				level: z.enum(['Beginner', 'Intermediate', 'Advanced']).optional(),
				minutes: z.number().int().positive().optional(),
				topics: z.array(z.string()).default([]),
				lastVerified: z.coerce.date().optional(),
				sources: z
					.array(
						z.object({
							title: z.string(),
							url: z.string().url(),
							publisher: z.string().optional(),
							type: z.enum(['official-doc', 'paper', 'standard', 'book']),
						}),
					)
					.default([]),
			}),
		}),
	}),
};
