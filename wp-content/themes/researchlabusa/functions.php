<?php
/**
 * Research Lab USA theme functions.
 *
 * Starter file for the auto-deploy pipeline. Add theme setup, enqueues,
 * and hooks here.
 *
 * @package researchlabusa
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Prevent direct access.
}

if ( ! function_exists( 'researchlabusa_setup' ) ) {
	/**
	 * Basic theme supports.
	 */
	function researchlabusa_setup() {
		add_theme_support( 'title-tag' );
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'automatic-feed-links' );
		add_theme_support(
			'html5',
			array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' )
		);
		register_nav_menus(
			array(
				'primary' => __( 'Primary Menu', 'researchlabusa' ),
			)
		);
	}
}
add_action( 'after_setup_theme', 'researchlabusa_setup' );

/**
 * Enqueue the theme stylesheet.
 */
function researchlabusa_assets() {
	wp_enqueue_style(
		'researchlabusa-style',
		get_stylesheet_uri(),
		array(),
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'researchlabusa_assets' );
