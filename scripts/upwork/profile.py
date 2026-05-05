"""Upwork freelancer profile operations."""

from __future__ import annotations

import json
import logging

from .bridge import BridgePage
from .human import sleep_random
from .urls import MY_PROFILE_URL

logger = logging.getLogger(__name__)


def get_my_profile(page: BridgePage) -> dict:
    page.navigate(MY_PROFILE_URL)
    page.wait_for_load()
    sleep_random(1200, 2000)
    page.wait_dom_stable(timeout=8.0)

    raw = page.evaluate(
        """
        (() => {
            const getText = (sel) => {
                const el = document.querySelector(sel);
                return el ? el.textContent.trim() : '';
            };
            return JSON.stringify({
                name: getText('[data-test="name"], h1, .profile-name'),
                title: getText('[data-test="title"], .profile-title, h2'),
                hourlyRate: getText('[data-test="hourly-rate"], .hourly-rate'),
                availability: getText('[data-test="availability"]'),
                connects: getText('[data-test="connects-balance"], .connects-balance'),
                profileUrl: window.location.href
            });
        })()
        """
    )
    try:
        return json.loads(raw or "{}")
    except Exception:
        return {}
