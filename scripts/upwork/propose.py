"""Upwork proposal submission."""

from __future__ import annotations

import logging
import time

from .bridge import BridgePage
from .errors import ProposalError, NotLoggedInError
from .human import sleep_random, ActionLogger
from .login import check_login_status
from .selectors import (
    APPLY_BUTTON,
    COVER_LETTER_TEXTAREA,
    BID_RATE_INPUT,
    MILESTONE_AMOUNT,
    PROPOSAL_SUBMIT_BTN,
    PROPOSAL_BOOST_SKIP,
)
from .types import ProposalResult
from .job_detail import get_job_detail

logger = logging.getLogger(__name__)
_alog = ActionLogger()


def submit_proposal(
    page: BridgePage,
    job_url: str,
    cover_letter: str,
    bid_rate: str = "",
) -> ProposalResult:
    """Navigate to a job, open the proposal form, fill it, and submit.

    Args:
        page: BridgePage instance
        job_url: Upwork job URL
        cover_letter: Proposal cover letter text
        bid_rate: Hourly rate or fixed bid amount (e.g. "45" or "500")
    """
    if not check_login_status(page):
        raise NotLoggedInError()

    # Get job details first for logging
    detail = get_job_detail(page, job_url)
    job_title = detail.title
    apply_url = detail.apply_url

    logger.info("Applying to: %s", job_title)

    # Navigate to apply URL or click apply button
    if apply_url:
        page.navigate(apply_url)
    else:
        page.navigate(job_url)
        page.wait_for_load()
        sleep_random(1000, 2000)
        try:
            page.click_element(APPLY_BUTTON)
        except Exception as e:
            raise ProposalError(f"Could not find Apply button: {e}") from e

    page.wait_for_load()
    sleep_random(1500, 2500)
    page.wait_dom_stable(timeout=10.0)

    current_url = page.get_url()
    if "login" in current_url or "account-security" in current_url:
        raise NotLoggedInError()

    # Fill cover letter
    if not page.wait_for_selector(COVER_LETTER_TEXTAREA.split(",")[0].strip(), timeout=20.0):
        raise ProposalError("Cover letter textarea not found — proposal form may have changed")

    page.fill_textarea(COVER_LETTER_TEXTAREA.split(",")[0].strip(), cover_letter)
    sleep_random(800, 1500)

    # Fill bid rate if provided
    if bid_rate:
        for rate_sel in [BID_RATE_INPUT, MILESTONE_AMOUNT]:
            for sel in rate_sel.split(","):
                sel = sel.strip()
                if page.has_element(sel):
                    # Clear existing value then type
                    page.evaluate(
                        f"document.querySelector('{sel}').value = ''; "
                        f"document.querySelector('{sel}').dispatchEvent(new Event('input', {{bubbles:true}}));"
                    )
                    sleep_random(300, 600)
                    page.fill_input(sel, bid_rate)
                    sleep_random(500, 900)
                    break

    # Skip optional boost screen if it appears
    sleep_random(500, 800)
    for skip_sel in PROPOSAL_BOOST_SKIP.split(","):
        if page.has_element(skip_sel.strip()):
            try:
                page.click_element(skip_sel.strip())
                sleep_random(800, 1200)
            except Exception:
                pass
            break

    # Submit
    submitted = False
    for submit_sel in PROPOSAL_SUBMIT_BTN.split(","):
        submit_sel = submit_sel.strip()
        if page.has_element(submit_sel):
            page.click_element(submit_sel)
            submitted = True
            sleep_random(2000, 3500)
            break

    if not submitted:
        raise ProposalError("Submit button not found — proposal form may have changed")

    # Verify submission
    final_url = page.get_url()
    success = "submitted" in final_url or "thank" in (page.evaluate("document.title") or "").lower()

    result = ProposalResult(
        job_url=job_url,
        job_title=job_title,
        success=success,
        message="Proposal submitted successfully" if success else "Submission status unclear — please verify in My Proposals",
        proposal_url=final_url,
    )

    _alog.log(
        action="submit_proposal",
        target_url=job_url,
        target_name=job_title,
        success=success,
        details={"bid": bid_rate, "cover_letter_len": len(cover_letter)},
    )

    return result


def list_my_proposals(page: BridgePage, limit: int = 20) -> list[dict]:
    """Scrape the My Proposals page and return a list of proposal dicts."""
    from .urls import MY_PROPOSALS_URL
    page.navigate(MY_PROPOSALS_URL)
    page.wait_for_load()
    sleep_random(1500, 2000)
    page.wait_dom_stable(timeout=8.0)

    import json
    raw = page.evaluate(
        """
        (() => {
            const rows = [];
            const tiles = document.querySelectorAll('[data-test="proposal-row"], article.proposal-item, li[class*="proposal"]');
            for (const tile of tiles) {
                const titleEl = tile.querySelector('h3 a, .job-title-link, a[href*="/jobs/"]');
                const statusEl = tile.querySelector('[data-test="proposal-status"], .status-badge, [class*="status"]');
                const dateEl = tile.querySelector('time, [data-test="submitted-date"]');
                const bidEl = tile.querySelector('[data-test="bid-amount"], .bid-amount');
                rows.push({
                    jobTitle: titleEl ? titleEl.textContent.trim() : '',
                    jobUrl: titleEl ? titleEl.href?.split('?')[0] : '',
                    status: statusEl ? statusEl.textContent.trim() : '',
                    submittedDate: dateEl ? (dateEl.getAttribute('datetime') || dateEl.textContent.trim()) : '',
                    bid: bidEl ? bidEl.textContent.trim() : ''
                });
            }
            return JSON.stringify(rows);
        })()
        """
    )
    try:
        return json.loads(raw or "[]")[:limit]
    except Exception:
        return []
