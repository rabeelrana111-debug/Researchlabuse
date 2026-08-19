import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
	const posts = (await getCollection('blog', ({ data }) => data.draft !== true))
		.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

	return rss({
		title: 'Research Lab USA — Blog',
		description:
			'Articles, guides and laboratory notes from the Research Lab USA team.',
		// context.site comes from the `site` value in astro.config.mjs.
		site: context.site,
		items: posts.map((post) => ({
			title: post.data.title,
			description: post.data.description,
			pubDate: post.data.pubDate,
			link: `/blog/${post.id}/`,
		})),
		customData: '<language>en-us</language>',
	});
}
