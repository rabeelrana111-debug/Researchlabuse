<?php
/**
 * Hello Elementor Child theme functions.
 *
 * Add custom PHP here — hooks, filters, shortcodes, custom post types.
 * Editing the parent Hello Elementor theme directly is not safe: its files are
 * replaced whenever the theme updates.
 *
 * @package hello-elementor-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Prevent direct access.
}

/**
 * Load the child theme stylesheet after the parent's.
 */
function researchlabusa_child_enqueue_styles() {
	// Hello Elementor lets its theme styles be switched off in Appearance
	// settings, so depend on its handles only when they're actually registered.
	// Naming a missing dependency would stop this stylesheet loading entirely.
	$deps = array_values(
		array_filter(
			array( 'hello-elementor', 'hello-elementor-theme-style' ),
			'wp_style_is'
		)
	);

	wp_enqueue_style(
		'hello-elementor-child-style',
		get_stylesheet_directory_uri() . '/style.css',
		$deps,
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'researchlabusa_child_enqueue_styles', 20 );
