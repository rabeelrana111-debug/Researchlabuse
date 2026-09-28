<?php
/**
 * Contact form handler for researchlabusa.com.
 *
 * Renders the page and, on POST, emails the inquiry to the address in $to.
 * Kept in one file so a failed submission can redisplay the form with the
 * visitor's text still in it, rather than losing what they typed.
 */

$sent   = false;
$errors = [];
$values = ['name' => '', 'email' => '', 'phone' => '', 'subject' => '', 'message' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    foreach ($values as $key => $_) {
        $values[$key] = trim((string) ($_POST[$key] ?? ''));
    }

    // Honeypot. The field is hidden from people, so anything in it came from
    // a bot. Report success rather than an error: telling a bot it failed
    // just invites a retry with the field left empty.
    if (trim((string) ($_POST['company'] ?? '')) !== '') {
        $sent   = true;
        $values = array_fill_keys(array_keys($values), '');
    } else {

        if ($values['name'] === '') {
            $errors[] = 'Please tell us your name.';
        }
        if (!filter_var($values['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = 'Please enter an email address we can reply to.';
        }
        if ($values['message'] === '') {
            $errors[] = 'Please write a message.';
        }

        if (!$errors) {
            $to = 'info@researchlabusa.com';

            // Strip CR and LF from anything that reaches a mail header.
            // Without this a crafted address could append its own headers and
            // turn the form into an open relay.
            $header_safe = static function ($value) {
                return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $value));
            };

            $subject = $values['subject'] !== ''
                ? $header_safe($values['subject'])
                : 'Website inquiry';

            // From must be an address on this domain or SPF and DKIM fail and
            // the mail lands in spam. The visitor's address goes in Reply-To,
            // so hitting reply still reaches them.
            $headers = implode("\r\n", [
                'From: Research Lab USA <noreply@researchlabusa.com>',
                'Reply-To: ' . $header_safe($values['email']),
                'Content-Type: text/plain; charset=UTF-8',
                'MIME-Version: 1.0',
            ]);

            $body = "New inquiry from the website contact form.\n\n"
                  . 'Name:    ' . $values['name'] . "\n"
                  . 'Email:   ' . $values['email'] . "\n"
                  . 'Phone:   ' . ($values['phone'] !== '' ? $values['phone'] : '(not given)') . "\n"
                  . 'Subject: ' . ($values['subject'] !== '' ? $values['subject'] : '(none)') . "\n\n"
                  . "Message:\n" . $values['message'] . "\n";

            $sent = @mail($to, '[Website] ' . $subject, $body, $headers);

            if ($sent) {
                $values = array_fill_keys(array_keys($values), '');
            } else {
                $errors[] = 'Something went wrong sending your message. '
                          . 'Please email us directly at info@researchlabusa.com.';
            }
        }
    }
}

/** Escape a value for safe output in HTML. */
function e($value) {
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}
?>
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
	<!-- Google tag (gtag.js) -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=G-X5GMPYGNT2"></script>
	<script>
		window.dataLayer = window.dataLayer || [];
		function gtag(){dataLayer.push(arguments);}
		gtag('js', new Date());

		gtag('config', 'G-X5GMPYGNT2');
	</script>
	<title>Contact Research Lab USA — Questions & Corrections</title>
	<meta name="description" content="Questions about a guide, corrections and suggestions for what to cover next are all welcome. Reach the editorial team at info@researchlabusa.com.">
	<link rel="canonical" href="https://researchlabusa.com/contact/">
	<meta name="theme-color" content="#0A2342">
	<meta property="og:type" content="website">
	<meta property="og:site_name" content="Research Lab USA">
	<meta property="og:title" content="Contact Research Lab USA — Questions & Corrections">
	<meta property="og:description" content="Questions about a guide, corrections and suggestions for what to cover next are all welcome. Reach the editorial team at info@researchlabusa.com.">
	<meta property="og:url" content="https://researchlabusa.com/contact/">
	<meta property="og:image" content="https://researchlabusa.com/assets/og-cover.jpg">
	<meta property="og:image:width" content="1200">
	<meta property="og:image:height" content="630">
	<meta property="og:image:alt" content="Research Lab USA — research compound reference guides">
	<meta property="og:locale" content="en_US">
	<meta name="twitter:card" content="summary_large_image">
	<meta name="twitter:title" content="Contact Research Lab USA — Questions & Corrections">
	<meta name="twitter:description" content="Questions about a guide, corrections and suggestions for what to cover next are all welcome. Reach the editorial team at info@researchlabusa.com.">
	<meta name="twitter:image" content="https://researchlabusa.com/assets/og-cover.jpg">
	<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"ContactPage","name":"Contact","description":"Questions about a guide, corrections and suggestions for what to cover next are all welcome. Reach the editorial team at info@researchlabusa.com.","url":"https://researchlabusa.com/contact/","inLanguage":"en-US","isPartOf":{"@id":"https://researchlabusa.com/#website"},"datePublished":"2026-08-20","dateModified":"2026-09-28"},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://researchlabusa.com/"},{"@type":"ListItem","position":2,"name":"Contact"}]}]}</script>
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
	<link rel="preload" as="image" type="image/webp"
	      imagesrcset="/assets/ampoules-microscope-480.webp 480w, /assets/ampoules-microscope-960.webp 960w, /assets/ampoules-microscope-1600.webp 1600w"
	      imagesizes="(min-width: 60rem) 34rem, calc(100vw - 3rem)" fetchpriority="high">
	<link rel="stylesheet" href="/styles.css?v=5952556a49">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<!-- Utility bar -->
<div class="utilitybar">
	<div class="wrap utilitybar__inner">
		<ul class="utilitybar__contact">
			<li>
				<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8L4.2 7.2v.9L12 14l7.8-5.9v-.9Z"/></svg>
				<a href="mailto:info@researchlabusa.com">info@researchlabusa.com</a>
			</li>
		</ul>
	</div>
</div>

<!-- Header -->
<header class="header">
	<div class="wrap header__inner">
		<a class="logo" href="/">
			<span class="logo__mark" aria-hidden="true">
				<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="currentColor"/><path d="M16 10h8v6l6 12a3 3 0 0 1-2.7 4.3H12.7A3 3 0 0 1 10 28l6-12v-6Z" fill="#fff"/><circle cx="20" cy="26" r="2.5" fill="currentColor"/></svg>
			</span>
			<span class="logo__text">Research <strong>Lab USA</strong></span>
		</a>

		<button class="navtoggle" aria-expanded="false" aria-controls="mainnav">
			<span class="navtoggle__bars" aria-hidden="true"></span>
			<span class="sr-only">Menu</span>
		</button>

		<nav class="nav" id="mainnav" aria-label="Main">
			<a href="/">Home</a>
			<div class="navitem">
				<a href="/sarms/">SARMs</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-sarms">
					<span class="sr-only">Show SARMs pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-sarms">
					<li><a href="/sarms/gw-501516/">GW-501516 (Cardarine)</a></li>
					<li><a href="/sarms/mk-2866/">MK-2866 (Ostarine)</a></li>
					<li><a href="/sarms/rad-140/">RAD-140 (Testolone)</a></li>
				</ul>
			</div>
			<div class="navitem">
				<a href="/peptides/">Peptides</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-peptides">
					<span class="sr-only">Show Peptides pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-peptides">
					<li><a href="/peptides/bpc-157/">BPC-157</a></li>
					<li><a href="/peptides/semaglutide/">Semaglutide</a></li>
					<li><a href="/peptides/tb-500/">TB-500</a></li>
				</ul>
			</div>
			<div class="navitem">
				<a href="/nootropics/">Nootropics</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-nootropics">
					<span class="sr-only">Show Nootropics pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-nootropics">
					<li><a href="/nootropics/adrafinil/">Adrafinil</a></li>
					<li><a href="/nootropics/cyclazodone/">Cyclazodone</a></li>
					<li><a href="/nootropics/flmodafinil/">Flmodafinil</a></li>
					<li><a href="/nootropics/phenylpiracetam/">Phenylpiracetam</a></li>
				</ul>
			</div>
			<a href="/guides/">Guides</a>
			<a href="/about/">About</a>
			<a href="/contact/" aria-current="page">Contact</a>
		</nav>

		<div class="header__actions">
			<a class="btn btn--ghost" href="/contact/">Inquire</a>
		</div>
	</div>
</header>

<main id="main">
	<section class="section">
		<div class="wrap">
			<div class="sectionhead">
				<p class="eyebrow"><svg class="eyebrow__ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2c0 4 10 4 10 8s-10 4-10 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M17 2c0 4-10 4-10 8s10 4 10 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg> Contact us</p>
				<h1>Write to us any time</h1>
				<p class="lede">Questions about a guide, corrections, and suggestions
				for what to cover next are all welcome. We reply within one business
				day.</p>
			</div>

			<div class="contactgrid">
				<!-- Contact details panel -->
				<aside class="contactpanel">
					<div class="contactpanel__top">
						<div class="contactpanel__item">
							<span class="contactpanel__icon" aria-hidden="true">
								<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8L4.2 7.2v.9L12 14l7.8-5.9v-.9Z"/></svg>
							</span>
							<div>
								<p class="contactpanel__label">Send an email</p>
								<p class="contactpanel__value">
									<a href="mailto:info@researchlabusa.com">info@researchlabusa.com</a>
								</p>
							</div>
						</div>

						<div class="contactpanel__item">
							<span class="contactpanel__icon" aria-hidden="true">
								<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>
							</span>
							<div>
								<p class="contactpanel__label">Response time</p>
								<p class="contactpanel__value">Within one business day</p>
							</div>
						</div>
					</div>

					<div class="contactpanel__media">
						<picture>
							<source type="image/webp" srcset="/assets/ampoules-microscope-480.webp 480w, /assets/ampoules-microscope-960.webp 960w, /assets/ampoules-microscope-1600.webp 1600w" sizes="(min-width: 60rem) 30rem, calc(100vw - 3rem)">
							<img src="/assets/ampoules-microscope-960.jpg" srcset="/assets/ampoules-microscope-480.jpg 480w, /assets/ampoules-microscope-960.jpg 960w, /assets/ampoules-microscope-1600.jpg 1600w"
							     sizes="(min-width: 60rem) 30rem, calc(100vw - 3rem)" alt="Glass ampoules on a bench in front of a microscope" width="1600" height="1067" loading="lazy" decoding="async">
						</picture>
\t\t\t\t\t</div>
\t\t\t\t</aside>

\t\t\t\t<!-- Inquiry form -->
\t\t\t\t<div class="contactform">
<?php if ($sent): ?>
\t\t\t\t\t<p class="formnote formnote--ok" role="status">
\t\t\t\t\t\t<strong>Thank you &mdash; your message has been sent.</strong>
\t\t\t\t\t\tWe reply within one business day.
\t\t\t\t\t</p>
<?php endif; ?>
<?php if ($errors): ?>
\t\t\t\t\t<div class="formnote formnote--error" role="alert">
\t\t\t\t\t\t<strong>Your message was not sent.</strong>
\t\t\t\t\t\t<ul>
<?php foreach ($errors as $error): ?>
\t\t\t\t\t\t\t<li><?= e($error) ?></li>
<?php endforeach; ?>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
<?php endif; ?>

\t\t\t\t\t<form method="post" action="/contact/#form" id="form" novalidate>
\t\t\t\t\t\t<div class="formgrid">
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="name">Your name</label>
\t\t\t\t\t\t\t\t<input class="input" type="text" id="name" name="name"
\t\t\t\t\t\t\t\t       value="<?= e($values['name']) ?>" required>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="email">Email address</label>
\t\t\t\t\t\t\t\t<input class="input" type="email" id="email" name="email"
\t\t\t\t\t\t\t\t       value="<?= e($values['email']) ?>" required>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="phone">Phone <span class="label__opt">(optional)</span></label>
\t\t\t\t\t\t\t\t<input class="input" type="tel" id="phone" name="phone"
\t\t\t\t\t\t\t\t       value="<?= e($values['phone']) ?>">
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="subject">Subject <span class="label__opt">(optional)</span></label>
\t\t\t\t\t\t\t\t<input class="input" type="text" id="subject" name="subject"
\t\t\t\t\t\t\t\t       value="<?= e($values['subject']) ?>">
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t<label class="label" for="message">Your message</label>
\t\t\t\t\t\t\t<textarea class="textarea" id="message" name="message" rows="8"
\t\t\t\t\t\t\t          required><?= e($values['message']) ?></textarea>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<!-- Honeypot: hidden from people, irresistible to bots. -->
\t\t\t\t\t\t<div class="hp" aria-hidden="true">
\t\t\t\t\t\t\t<label for="company">Company</label>
\t\t\t\t\t\t\t<input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<button class="btn btn--primary" type="submit">Send message</button>
\t\t\t\t\t\t<p class="note-sm">We use what you send through this form only to
\t\t\t\t\t\tread and answer your inquiry. Please do not submit confidential,
\t\t\t\t\t\tpatient or medical information. We do not sell contact-form
\t\t\t\t\t\tinformation or share it with anyone for their own marketing. It
\t\t\t\t\t\tmay be handled by the service providers that run our website and
\t\t\t\t\t\temail, under confidentiality obligations. For the detail, read our
\t\t\t\t\t\t<a href="/privacy/">Privacy Policy</a> and
\t\t\t\t\t\t<a href="/terms/">Terms of Use</a>.</p>
\t\t\t\t\t</form>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>What we can help with</h2>
\t\t\t\t<ul>
\t\t\t\t\t<li>Questions about anything in a guide</li>
\t\t\t\t\t<li>Corrections, including sources we have missed or misread</li>
\t\t\t\t\t<li>Suggestions for compounds or topics to cover next</li>
\t\t\t\t\t<li>Requests to cite or reference our material</li>
\t\t\t\t</ul>

\t\t\t\t<h2>What we cannot help with</h2>
\t\t\t\t<p>We do not give dosing guidance or advise on human or veterinary
\t\t\t\tuse, and we do not vet suppliers or settle disputes with them.
\t\t\t\tMessages asking for those will not get a useful reply, and we would
\t\t\t\trather say so here than leave you waiting for one.</p>
\t\t\t\t<p>Avid Peptides is our peptide supply partner, and you
				will see them featured on our peptide pages. Questions about their
				catalogue, an order or a batch should go to them directly &mdash; we
				cannot answer those for them.</p>
			</div>
		</div>
	</section>

	<section class="section section--tight">
		<div class="wrap">
			<p class="notice">
				<strong>For laboratory research use only.</strong> The research
				materials described on this website are not intended for human or
				veterinary use. Where we refer to an approved drug or active
				ingredient, we are describing the published regulatory status of that
				specific approved product &mdash; it does not mean a research material
				supplied by a third party is FDA-approved. Nothing here is medical
				advice or a recommendation about diagnosis, treatment, dosing or
				personal use.
			</p>
		</div>
	</section>
</main>

<!-- Footer -->
<footer class="footer">
	<div class="wrap">
		<div class="footer__grid">
			<div>
				<p class="footer__title">Research Lab USA</p>
				<p>Independent reference material for laboratory researchers.</p>
			</div>
			<div>
				<p class="footer__title">Topics</p>
				<ul class="footer__list">
					<li><a href="/sarms/">SARMs</a></li>
					<li><a href="/peptides/">Peptides</a></li>
					<li><a href="/nootropics/">Nootropics</a></li>
					<li><a href="/guides/">All guides</a></li>
				</ul>
			</div>
			<div>
				<p class="footer__title">Site</p>
				<ul class="footer__list">
					<li><a href="/about/">About</a></li>
					<li><a href="/contact/">Contact</a></li>
					<li><a href="/privacy/">Privacy Policy</a></li>
					<li><a href="/terms/">Terms of Use</a></li>
				</ul>
			</div>
			<div>
				<p class="footer__title">Contact</p>
				<ul class="footer__list">
					<li><a href="mailto:info@researchlabusa.com">info@researchlabusa.com</a></li>
				</ul>
			</div>
		</div>
		<div class="footer__bottom">
			<p>&copy; <span id="year">2026</span> Research Lab USA. All rights reserved.</p>
			<p>For research use only. Not for human or veterinary consumption.</p>
		</div>
	</div>
</footer>

<a class="totop" href="#main" aria-label="Back to top"><span aria-hidden="true">Back to top</span></a>

<script src="/script.js?v=68dfb9a39d" defer></script>
</body>
</html>
