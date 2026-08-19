/* Small progressive enhancements. The site works without this file: the nav
   is a plain list of links, dropdowns open on hover and keyboard focus via
   CSS alone, and the back-to-top link is an ordinary anchor. */

(function () {
	'use strict';

	// Marks that scripting is available. The stylesheet uses this to decide
	// whether :focus-within should open dropdowns: without JavaScript it is
	// the only way to reach them by keyboard, but with JavaScript it fights
	// the explicit close (Escape returns focus to the toggle, which sits
	// inside the menu, re-opening it immediately).
	document.documentElement.classList.add('has-js');

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

	// --- Dropdown submenus -------------------------------------------------
	// CSS already opens these on hover and on focus-within. This adds click
	// and touch support, where hover does not exist, and keeps aria-expanded
	// accurate so screen readers announce the state correctly.
	var dropdowns = [].slice.call(document.querySelectorAll('.navitem__toggle'));

	function setOpen(btn, open) {
		btn.setAttribute('aria-expanded', String(open));
		var item = btn.closest('.navitem');
		if (item) { item.classList.toggle('is-open', open); }
	}

	function closeAll(except) {
		dropdowns.forEach(function (btn) {
			if (btn !== except) { setOpen(btn, false); }
		});
	}

	dropdowns.forEach(function (btn) {
		btn.addEventListener('click', function (event) {
			event.preventDefault();
			var open = btn.getAttribute('aria-expanded') === 'true';
			// Only one menu open at a time, so panels cannot overlap.
			closeAll(btn);
			setOpen(btn, !open);
		});
	});

	if (dropdowns.length) {
		document.addEventListener('keydown', function (event) {
			if (event.key !== 'Escape') { return; }
			var open = document.querySelector('.navitem__toggle[aria-expanded="true"]');
			if (!open) { return; }
			closeAll();
			// Return focus to the control that opened the menu, rather than
			// leaving it stranded inside a panel that has just closed.
			open.focus();
		});

		document.addEventListener('click', function (event) {
			if (!event.target.closest('.navitem')) { closeAll(); }
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
