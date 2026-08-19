// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Used to build absolute URLs in the sitemap, RSS feed and social tags.
  // Must match the live domain or those links will point at the wrong host.
  site: 'https://researchlabusa.com',
  integrations: [sitemap()],
  build: {
    // Emit `about/index.html` rather than `about.html`, so URLs work as
    // /about/ on Apache without any rewrite rules.
    format: 'directory',
  },
});
