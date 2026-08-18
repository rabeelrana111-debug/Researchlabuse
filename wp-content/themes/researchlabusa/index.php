<?php
/**
 * Main template file.
 *
 * @package researchlabusa
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<main id="main" class="site-main">
	<?php
	if ( have_posts() ) {
		while ( have_posts() ) {
			the_post();
			?>
			<article <?php post_class(); ?>>
				<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
				<div class="entry-content"><?php the_content(); ?></div>
			</article>
			<?php
		}
	} else {
		echo '<p>' . esc_html__( 'Nothing here yet.', 'researchlabusa' ) . '</p>';
	}
	?>
</main>

<?php
get_footer();
