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
    draft: z.boolean().default(false),
  }),
});

// Catalogue entries. Each markdown file becomes one product page, and the
// body of the file is the "About this material" section.
//
// Fields describe the MATERIAL — identity, purity, physical form, storage.
// There is deliberately no field for effects or benefits: describing what a
// compound does in a body turns a listing into an unapproved drug claim.
const products = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/products' }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    category: z.string().default('Research compounds'),
    cas: z.string().optional(),
    formula: z.string().optional(),
    molecularWeight: z.string().optional(),
    purity: z.string(),
    batch: z.string().optional(),
    format: z.string(),
    quantity: z.string(),
    price: z.number().optional(),
    currency: z.string().default('USD'),
    storage: z.string(),
    /** Link to the certificate of analysis PDF for the current batch. */
    coaUrl: z.string().optional(),
    inStock: z.boolean().default(true),
    order: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, products };
