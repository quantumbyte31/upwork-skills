"""Upwork job search."""

from __future__ import annotations

import json
import logging
import time

from .bridge import BridgePage
from .human import sleep_random
from .types import JobListing
from .urls import make_job_search_url

logger = logging.getLogger(__name__)

_EXTRACT_JOBS_JS = """
(() => {
    const jobs = [];
    const seen = new Set();

    // Try multiple tile selectors — Upwork DOM changes
    const tiles = Array.from(document.querySelectorAll(
        'article.job-tile, [data-test="job-tile"], section[class*="job-tile"]'
    ));

    for (const tile of tiles) {
        // Title + URL
        const titleEl = tile.querySelector(
            'h2.h5.job-tile-title a, a.job-title-link, [data-test="job-title"] a, h2 a'
        );
        if (!titleEl) continue;
        const title = titleEl.textContent.trim();
        const url = titleEl.href ? titleEl.href.split('?')[0] : '';
        if (!title || !url || seen.has(url)) continue;
        seen.add(url);

        // Extract UID from URL
        const uidMatch = url.match(/jobs\/([^/]+)\/?$/);
        const uid = uidMatch ? uidMatch[1] : '';

        // Budget / type
        const budgetEl = tile.querySelector(
            '[data-test="budget"], strong[data-test="budget"]'
        );
        const typeEl = tile.querySelector('[data-test="job-type-label"]');
        const budget = budgetEl ? budgetEl.textContent.trim() : '';
        const jobType = typeEl ? typeEl.textContent.trim().toLowerCase() : '';

        // Description snippet
        const descEl = tile.querySelector(
            '[data-test="job-description-text"] p, [data-test="job-description-text"] span, .break span'
        );
        const description = descEl ? descEl.textContent.trim().substring(0, 300) : '';

        // Skills
        const skillEls = Array.from(tile.querySelectorAll(
            '[data-test="skills-list"] a, [data-test="attr-item"], span.air3-badge-tagline'
        ));
        const skills = skillEls.map(s => s.textContent.trim()).filter(Boolean);

        // Posted date
        const dateEl = tile.querySelector('[data-test="job-pubilshed-date"], [data-test="posted-date"]');
        const postedDate = dateEl ? dateEl.textContent.trim() : '';

        // Payment verified
        const pvEl = tile.querySelector('[data-test="payment-verified"], .payment-verified');
        const paymentVerified = pvEl ? pvEl.textContent.toLowerCase().includes('verified') : false;

        // Client country
        const countryEl = tile.querySelector('[data-test="client-country"], .client-location');
        const clientCountry = countryEl ? countryEl.textContent.trim() : '';

        // Proposals count
        const propEl = tile.querySelector('[data-test="proposals"]');
        const proposalsCount = propEl ? propEl.textContent.trim() : '';

        jobs.push({
            title, url, uid, postedDate, budget,
            jobType: jobType || (budget.includes('/hr') ? 'hourly' : 'fixed'),
            description, skills, paymentVerified, clientCountry, proposalsCount
        });
    }
    return JSON.stringify(jobs);
})()
"""


def search_jobs(
    page: BridgePage,
    query: str,
    limit: int = 20,
    sort: str = "recency",
    job_type: str = "",
    min_budget: int = 0,
) -> list[JobListing]:
    url = make_job_search_url(query, sort=sort, job_type=job_type, min_budget=min_budget)
    logger.info("Searching Upwork: %s", url)
    page.navigate(url)
    page.wait_for_load()
    sleep_random(1500, 2500)
    page.wait_dom_stable(timeout=8.0)

    raw = page.evaluate(_EXTRACT_JOBS_JS)
    try:
        items = json.loads(raw or "[]")
    except (json.JSONDecodeError, TypeError):
        logger.warning("Failed to parse job list JSON")
        items = []

    results = []
    for item in items[:limit]:
        results.append(JobListing(
            title=item.get("title", ""),
            url=item.get("url", ""),
            uid=item.get("uid", ""),
            posted_date=item.get("postedDate", ""),
            budget=item.get("budget", ""),
            job_type=item.get("jobType", ""),
            description=item.get("description", ""),
            skills=item.get("skills", []),
            payment_verified=item.get("paymentVerified", False),
            client_country=item.get("clientCountry", ""),
            proposals_count=item.get("proposalsCount", ""),
        ))

    logger.info("Found %d jobs for query: %s", len(results), query)
    return results
