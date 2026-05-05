"""Upwork CSS selectors — ordered by reliability (Upwork DOM changes frequently)."""

# Auth
LOGGED_IN = "[data-test='nav-logged-in'], img.up-avatar, [data-qa='header-desktop-user-avatar']"
NOT_LOGGED_IN = "a[href*='/ab/account-security/login'], [data-test='nav-login-button']"
USER_AVATAR = "img.up-avatar, [data-qa='header-desktop-user-avatar']"

# Job search results
JOB_TILE = "article.job-tile, [data-test='job-tile'], section.air3-card-section"
JOB_TITLE_LINK = "h2.h5.job-tile-title a, a.job-title-link, [data-test='job-title'] a"
JOB_BUDGET = "[data-test='budget'], strong[data-test='budget'], [data-test='job-type-label']"
JOB_DESCRIPTION = "[data-test='job-description-text'] p, .break span, [data-test='description']"
JOB_SKILLS = "[data-test='skills-list'] a, [data-test='attr-item'], span.air3-badge-tagline"
JOB_POSTED_DATE = "[data-test='job-pubilshed-date'], [data-test='posted-date']"
JOB_PAYMENT_VERIFIED = "[data-test='payment-verified'], .payment-verified"
JOB_CLIENT_COUNTRY = "[data-test='client-country'], .client-location"

# Job detail page
APPLY_BUTTON = "a[href*='/proposals/job/'], a[data-qa='btn-apply'], button[data-qa='btn-apply']"
JOB_DETAIL_TITLE = "h1[data-test='job-title'], h1.job-title, h1"
JOB_DETAIL_DESCRIPTION = "[data-test='job-description'] p, [data-test='description-section'] p"

# Proposal form
COVER_LETTER_TEXTAREA = "textarea[data-qa='cover-letter-input'], [data-cy='cover-letter'], textarea[placeholder*='cover letter' i]"
BID_RATE_INPUT = "input[data-qa='bid-rate'], input[data-test='bid-rate']"
MILESTONE_AMOUNT = "input[data-qa='milestone-amount'], input[name='bid']"
PROPOSAL_SUBMIT_BTN = "button[data-qa='submit-btn'], button[data-test='submit-proposal-btn'], [data-qa='submit-proposal-btn']"
PROPOSAL_BOOST_SKIP = "button[data-qa='skip-btn'], [data-test='skip-boost-btn']"

# My proposals list
PROPOSAL_ROW = "[data-test='proposal-row'], article.proposal-item"
PROPOSAL_JOB_TITLE = "h3 a, .job-title-link"
PROPOSAL_STATUS = "[data-test='proposal-status'], .status-badge"
