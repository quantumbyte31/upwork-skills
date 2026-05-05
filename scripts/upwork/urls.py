"""Upwork URL constants and builders."""

from __future__ import annotations

from urllib.parse import quote_plus

BASE = "https://www.upwork.com"
HOME_URL = BASE
LOGIN_URL = f"{BASE}/ab/account-security/login"
JOBS_SEARCH_URL = f"{BASE}/nx/search/jobs/"
MY_PROPOSALS_URL = f"{BASE}/nx/proposals/"
MY_PROFILE_URL = f"{BASE}/freelancers/settings/contactInfo"
FIND_WORK_URL = f"{BASE}/nx/find-work/"


def make_job_search_url(
    query: str,
    sort: str = "recency",
    job_type: str = "",       # "hourly" | "fixed"
    min_budget: int = 0,
    payment_verified: bool = True,
) -> str:
    url = f"{JOBS_SEARCH_URL}?q={quote_plus(query)}&sort={sort}"
    if payment_verified:
        url += "&payment_verified=1"
    if job_type in ("hourly", "fixed"):
        url += f"&job_type={job_type}"
    if min_budget > 0:
        url += f"&budget={min_budget}"
    return url
