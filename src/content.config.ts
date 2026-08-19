import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Blog posts are markdown files in src/content/blog/.
// The schema is validated at build time, so a typo in a post's front matter
// fails the build instead of silently producing a broken page.
const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Research Lab USA'),
    tags: z.array(z.string()).default([]),
    // Drafts are excluded from the site when building for production.
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
