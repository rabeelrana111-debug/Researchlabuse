/* Small progressive enhancements. The site works without this file — the nav
   is a plain list and the back-to-top link is an ordinary anchor. */

(function () {
	'use strict';

	// --- Mobile navigation -------------------------------------------------
	var toggle = document.querySelector('.navtoggle');
	var nav = document.getElementById('mainnav');

	if (toggle && nav) {
		toggle.addEventListener('click', function () {
			var open = nav.classList.toggle('is-open');
			toggle.setAttribute('aria-expanded', String(open));
		});

		// Close the menu when a link is followed, so the next page does not
		// load with the panel still expanded.
		nav.addEventListener('click', function (event) {
			if (event.target.tagName === 'A') {
				nav.classList.remove('is-open');
				toggle.setAttribute('aria-expanded', 'false');
			}
		});
	}

	// --- Back to top -------------------------------------------------------
	var toTop = document.querySelector('.totop');

	if (toTop) {
		var update = function () {
			toTop.classList.toggle('is-visible', window.scrollY > 600);
		};
		update();
		window.addEventListener('scroll', update, { passive: true });

		toTop.addEventListener('click', function (event) {
			event.preventDefault();
			var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
			window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
			// Move keyboard focus back to the top of the document, not just
			// the scroll position.
			var main = document.getElementById('main');
			if (main) {
				main.setAttribute('tabindex', '-1');
				main.focus({ preventScroll: true });
			}
		});
	}

	// --- Footer year -------------------------------------------------------
	var year = document.getElementById('year');
	if (year) { year.textContent = String(new Date().getFullYear()); }
})();
