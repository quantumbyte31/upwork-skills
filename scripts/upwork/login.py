"""Upwork login state management."""

from __future__ import annotations

import logging
import time

from .bridge import BridgePage
from .human import sleep_random
from .selectors import LOGGED_IN, NOT_LOGGED_IN
from .urls import HOME_URL, LOGIN_URL, FIND_WORK_URL

logger = logging.getLogger(__name__)


def check_login_status(page: BridgePage) -> bool:
    current_url = page.get_url()
    if "upwork.com" not in current_url:
        page.navigate(FIND_WORK_URL)
        page.wait_for_load()
    page.wait_dom_stable(timeout=5.0)

    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline:
        if page.has_element(LOGGED_IN):
            return True
        if page.has_element(NOT_LOGGED_IN):
            return False
        # Also check if URL redirected to login page
        url = page.get_url()
        if "login" in url or "account-security" in url:
            return False
        time.sleep(0.3)

    return page.has_element(LOGGED_IN)


def get_current_username(page: BridgePage) -> str:
    try:
        if not check_login_status(page):
            return ""
        username = page.evaluate(
            """
            (() => {
                // Try data attribute on avatar
                const avatar = document.querySelector('img.up-avatar[alt]');
                if (avatar) return avatar.alt.trim();
                // Try profile link href
                const links = document.querySelectorAll('a[href*="/freelancers/~"]');
                for (const a of links) {
                    const m = a.href.match(/\/freelancers\/(~[^/?#]+)/);
                    if (m) return m[1];
                }
                // Try header name span
                const nameEl = document.querySelector('[data-qa="header-desktop-user-name"], .nav-user-name');
                if (nameEl) return nameEl.textContent.trim();
                return '';
            })()
            """
        )
        return username or ""
    except Exception:
        logger.warning("Failed to get Upwork username")
        return ""


def logout(page: BridgePage) -> bool:
    page.navigate(HOME_URL)
    page.wait_for_load()
    sleep_random(800, 1500)
    if not check_login_status(page):
        logger.info("Already not logged in")
        return False
    try:
        # Click user menu
        page.click_element("[data-qa='header-desktop-user-avatar'], img.up-avatar")
        sleep_random(600, 1000)
        page.click_element("a[href*='/logout'], button[data-test='logout']")
        sleep_random(1000, 2000)
        logger.info("Logged out via UI")
        return True
    except Exception as e:
        logger.warning("UI logout failed: %s", e)
        return False
