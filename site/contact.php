<?php
/**
 * Contact form handler for researchlabusa.com.
 *
 * Renders the page and, on POST, emails the enquiry to the address in $to.
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
                : 'Website enquiry';

            // From must be an address on this domain or SPF and DKIM fail and
            // the mail lands in spam. The visitor's address goes in Reply-To,
            // so hitting reply still reaches them.
            $headers = implode("\r\n", [
                'From: Research Lab USA <noreply@researchlabusa.com>',
                'Reply-To: ' . $header_safe($values['email']),
                'Content-Type: text/plain; charset=UTF-8',
                'MIME-Version: 1.0',
            ]);

            $body = "New enquiry from the website contact form.\n\n"
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
	<title>Contact | Research Lab USA</title>
	<meta name="description" content="Questions, corrections and suggestions for what to cover next. Reach us at info@researchlabusa.com.">
	<link rel="canonical" href="https://researchlabusa.com/contact.php">
	<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
	<link rel="stylesheet" href="/styles.css?v=10630ac016">
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
		<nav class="utilitybar__social" aria-label="Social media">
			<a href="#" aria-label="X (Twitter)"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 2H22l-7.1 8.1L23.2 22h-6.5l-5.1-6.6L5.8 22H2.7l7.6-8.7L1.5 2H8l4.6 6.1L18.9 2Zm-1.1 18h1.7L7.3 3.7H5.5L17.8 20Z"/></svg></a>
			<a href="#" aria-label="Facebook"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.25-1.5 1.55-1.5H16.7V4.6c-.29-.04-1.28-.13-2.44-.13-2.42 0-4.07 1.47-4.07 4.18v2.24H7.5V14h2.69v8h3.31Z"/></svg></a>
			<a href="#" aria-label="LinkedIn"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.9 21H3.5V9h3.4v12ZM5.2 7.5a2 2 0 1 1 0-4 2 2 0 0 1 0 4ZM21 21h-3.4v-5.8c0-1.4 0-3.2-1.9-3.2s-2.2 1.5-2.2 3.1V21H10V9h3.3v1.6h.05a3.6 3.6 0 0 1 3.25-1.8c3.5 0 4.4 2.3 4.4 5.3V21Z"/></svg></a>
			<a href="#" aria-label="Instagram"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.25.07 1.62.07 4.81 0 3.2 0 3.57-.07 4.81-.15 3.23-1.66 4.77-4.92 4.92-1.25.06-1.62.07-4.85.07-3.2 0-3.57 0-4.81-.07-3.27-.15-4.77-1.7-4.92-4.92C2.21 15.57 2.2 15.2 2.2 12c0-3.19 0-3.56.07-4.81.15-3.23 1.66-4.77 4.92-4.92C8.43 2.21 8.8 2.2 12 2.2Zm0 5.16a4.64 4.64 0 1 0 0 9.28 4.64 4.64 0 0 0 0-9.28Zm0 7.65a3.01 3.01 0 1 1 0-6.02 3.01 3.01 0 0 1 0 6.02Zm4.83-8.89a1.08 1.08 0 1 0 0 2.17 1.08 1.08 0 0 0 0-2.17Z"/></svg></a>
		</nav>
	</div>
</div>

<!-- Header -->
<header class="header">
	<div class="wrap header__inner">
		<a class="logo" href="/">
			<span class="logo__mark" aria-hidden="true">
				<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="currentColor"/><path d="M16 10h8v6l6 12a3 3 0 0 1-2.7 4.3H12.7A3 3 0 0 1 10 28l6-12v-6Z" fill="#fff"/><circle cx="20" cy="26" r="2.5" fill="currentColor"/></svg>
			</span>
			<span class="logo__text">Research<strong>Lab USA</strong></span>
		</a>

		<button class="navtoggle" aria-expanded="false" aria-controls="mainnav">
			<span class="navtoggle__bars" aria-hidden="true"></span>
			<span class="sr-only">Menu</span>
		</button>

		<nav class="nav" id="mainnav" aria-label="Main">
			<a href="/">Home</a>
			<div class="navitem">
				<a href="/sarms.html">SARMs</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-sarms">
					<span class="sr-only">Show SARMs pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-sarms">
					<li><a href="/sarms/gw-501516.html">GW-501516 (Cardarine)</a></li>
					<li><a href="/sarms/mk-2866.html">MK-2866 (Ostarine)</a></li>
					<li><a href="/sarms/rad-140.html">RAD-140 (Testolone)</a></li>
				</ul>
			</div>
			<div class="navitem">
				<a href="/peptides.html">Peptides</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-peptides">
					<span class="sr-only">Show Peptides pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-peptides">
					<li><a href="/peptides/bpc-157.html">BPC-157</a></li>
					<li><a href="/peptides/semaglutide.html">Semaglutide</a></li>
					<li><a href="/peptides/tb-500.html">TB-500</a></li>
				</ul>
			</div>
			<div class="navitem">
				<a href="/nootropics.html">Nootropics</a>
				<button class="navitem__toggle" aria-expanded="false"
				        aria-controls="menu-nootropics">
					<span class="sr-only">Show Nootropics pages</span>
					<span class="navitem__chevron" aria-hidden="true"></span>
				</button>
				<ul class="submenu" id="menu-nootropics">
					<li><a href="/nootropics/adrafinil.html">Adrafinil</a></li>
					<li><a href="/nootropics/cyclazodone.html">Cyclazodone</a></li>
					<li><a href="/nootropics/flmodafinil.html">Flmodafinil</a></li>
					<li><a href="/nootropics/phenylpiracetam.html">Phenylpiracetam</a></li>
				</ul>
			</div>
			<a href="/guides.html">Guides</a>
			<a href="/about.html">About</a>
			<a href="/contact.php" aria-current="page">Contact</a>
		</nav>

		<div class="header__actions">
			<a class="btn btn--ghost" href="/contact.php">Enquire</a>
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
						<img src="/assets/ampoules-microscope.jpg"
						     alt="Glass ampoules on a bench in front of a microscope"
						     width="1600" height="1067" loading="lazy" decoding="async">
					</div>
				</aside>

				<!-- Enquiry form -->
				<div class="contactform">
<?php if ($sent): ?>
					<p class="formnote formnote--ok" role="status">
						<strong>Thank you &mdash; your message has been sent.</strong>
						We reply within one business day.
					</p>
<?php endif; ?>
<?php if ($errors): ?>
					<div class="formnote formnote--error" role="alert">
						<strong>Your message was not sent.</strong>
						<ul>
<?php foreach ($errors as $error): ?>
							<li><?= e($error) ?></li>
<?php endforeach; ?>
						</ul>
					</div>
<?php endif; ?>

					<form method="post" action="/contact.php#form" id="form" novalidate>
						<div class="formgrid">
							<div class="field">
								<label class="label" for="name">Your name</label>
								<input class="input" type="text" id="name" name="name"
								       value="<?= e($values['name']) ?>" required>
							</div>
							<div class="field">
								<label class="label" for="email">Email address</label>
								<input class="input" type="email" id="email" name="email"
								       value="<?= e($values['email']) ?>" required>
							</div>
							<div class="field">
								<label class="label" for="phone">Phone <span class="label__opt">(optional)</span></label>
								<input class="input" type="tel" id="phone" name="phone"
								       value="<?= e($values['phone']) ?>">
							</div>
							<div class="field">
								<label class="label" for="subject">Subject <span class="label__opt">(optional)</span></label>
								<input class="input" type="text" id="subject" name="subject"
								       value="<?= e($values['subject']) ?>">
							</div>
						</div>

						<div class="field">
							<label class="label" for="message">Your message</label>
							<textarea class="textarea" id="message" name="message" rows="8"
							          required><?= e($values['message']) ?></textarea>
						</div>

						<!-- Honeypot: hidden from people, irresistible to bots. -->
						<div class="hp" aria-hidden="true">
							<label for="company">Company</label>
							<input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
						</div>

						<button class="btn btn--primary" type="submit">Send message</button>
						<p class="note-sm">We use your details only to reply to this
						enquiry. Please do not send confidential information through
						this form.</p>
					</form>
				</div>
			</div>
		</div>
	</section>

	<section class="section section--tight">
		<div class="wrap">
			<div class="measure prose">
				<h2>What we can help with</h2>
				<ul>
					<li>Questions about anything in a guide</li>
					<li>Corrections, including sources we have missed or misread</li>
					<li>Suggestions for compounds or topics to cover next</li>
					<li>Requests to cite or reference our material</li>
				</ul>

				<h2>What we cannot help with</h2>
				<p>We do not give dosing guidance, advise on human or veterinary use,
				or recommend where to buy anything. Messages asking for those will not
				get a useful reply, and we would rather say so here than leave you
				waiting for one.</p>
			</div>
		</div>
	</section>

	<section class="section section--tight">
		<div class="wrap">
			<p class="notice">
				<strong>For laboratory and research use only.</strong> The materials
				discussed on this website are not medicines, dietary supplements,
				cosmetics or food. None has been evaluated or approved by the FDA for
				human or veterinary use. Nothing here is medical advice, and nothing
				here should be read as a suggestion that any compound is safe or
				effective for any purpose.
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
					<li><a href="/sarms.html">SARMs</a></li>
					<li><a href="/peptides.html">Peptides</a></li>
					<li><a href="/nootropics.html">Nootropics</a></li>
					<li><a href="/guides.html">All guides</a></li>
				</ul>
			</div>
			<div>
				<p class="footer__title">Site</p>
				<ul class="footer__list">
					<li><a href="/about.html">About</a></li>
					<li><a href="/contact.php">Contact</a></li>
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
