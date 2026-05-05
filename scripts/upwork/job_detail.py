"""Upwork job detail page scraper."""

from __future__ import annotations

import json
import logging
import re

from .bridge import BridgePage
from .human import sleep_random
from .types import JobDetail
from .urls import BASE

logger = logging.getLogger(__name__)

_EXTRACT_DETAIL_JS = """
(() => {
    const getText = (sel) => {
        const el = document.querySelector(sel);
        return el ? el.textContent.trim() : '';
    };
    const getAll = (sel) => Array.from(document.querySelectorAll(sel))
        .map(e => e.textContent.trim()).filter(Boolean);

    // Title
    const title = getText('h1[data-test="job-title"], h1.job-title, h1') || document.title;

    // Full description
    const descEl = document.querySelector(
        '[data-test="job-description"] [data-test="description"], ' +
        '[data-test="description-section"], ' +
        'section[data-test="description"]'
    );
    const fullDesc = descEl ? descEl.innerText.trim() : getText('[data-test="description"]');

    // Budget
    const budget = getText(
        '[data-test="budget"], [data-test="job-budget"], strong[data-test="budget"]'
    );

    // Skills
    const skills = getAll('[data-test="skills-list"] a, [data-test="attr-item"]');

    // Metadata
    const experienceLevel = getText('[data-test="experience-level"], [data-test="contractor-tier"]');
    const projectDuration = getText('[data-test="duration-label"], [data-test="project-duration"]');
    const weeklyHours = getText('[data-test="hours-per-week"]');
    const jobType = getText('[data-test="job-type-label"]') ||
        (budget.includes('/hr') ? 'hourly' : 'fixed');

    // Client info
    const clientRating = getText('[data-test="client-rating"], .air3-rating-value-text');
    const clientTotalSpent = getText('[data-test="client-spendings"], [data-test="total-spent"]');
    const clientCountry = getText('[data-test="client-location"], .client-location');
    const paymentVerified = !!document.querySelector(
        '[data-test="payment-verified"], .payment-verified'
    );

    // Posted date
    const postedDate = getText('[data-test="posted-date"], time[datetime]') ||
        (document.querySelector('time[datetime]')?.getAttribute('datetime') || '');

    // Apply URL — look for proposal link
    const applyLink = document.querySelector(
        'a[href*="/proposals/job/"], a[data-qa="btn-apply"]'
    );
    const applyUrl = applyLink ? applyLink.href : '';

    // Current page URL
    const pageUrl = window.location.href.split('?')[0];
    const uidMatch = pageUrl.match(/jobs\\/([^/]+)\\/?$/);
    const uid = uidMatch ? uidMatch[1] : '';

    return JSON.stringify({
        title, fullDesc, budget, jobType, skills,
        experienceLevel, projectDuration, weeklyHours,
        clientRating, clientTotalSpent, clientCountry,
        paymentVerified, postedDate, applyUrl, pageUrl, uid
    });
})()
"""


def get_job_detail(page: BridgePage, url: str) -> JobDetail:
    logger.info("Getting job detail: %s", url)
    page.navigate(url)
    page.wait_for_load()
    sleep_random(1200, 2000)
    page.wait_dom_stable(timeout=8.0)

    raw = page.evaluate(_EXTRACT_DETAIL_JS)
    try:
        d = json.loads(raw or "{}")
    except (json.JSONDecodeError, TypeError):
        d = {}

    return JobDetail(
        title=d.get("title", ""),
        url=d.get("pageUrl", url),
        uid=d.get("uid", ""),
        posted_date=d.get("postedDate", ""),
        budget=d.get("budget", ""),
        job_type=d.get("jobType", ""),
        description=d.get("fullDesc", "")[:500],
        full_description=d.get("fullDesc", ""),
        skills=d.get("skills", []),
        payment_verified=d.get("paymentVerified", False),
        client_country=d.get("clientCountry", ""),
        experience_level=d.get("experienceLevel", ""),
        project_duration=d.get("projectDuration", ""),
        weekly_hours=d.get("weeklyHours", ""),
        client_rating=d.get("clientRating", ""),
        client_total_spent=d.get("clientTotalSpent", ""),
        apply_url=d.get("applyUrl", ""),
    )
