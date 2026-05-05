"""Unified CLI entry point — Upwork Extension Bridge version.

Connects to the user's browser via the Upwork Bridge extension.
Start bridge_server.py first, install the Upwork Bridge extension in Chrome, then run this CLI.

Output: JSON (ensure_ascii=False)
Exit codes: 0=success, 1=not logged in, 2=error
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("upwork-cli")


def _output(data: dict, exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


class _DummyBrowser:
    def close(self) -> None:
        pass


def _ensure_bridge_ready(bridge_url: str) -> None:
    import subprocess
    import time
    from pathlib import Path
    from upwork.bridge import BridgePage

    page = BridgePage(bridge_url)
    if not page.is_server_running():
        logger.info("Bridge server not running, starting...")
        scripts_dir = Path(__file__).parent
        kwargs: dict = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        subprocess.Popen([sys.executable, str(scripts_dir / "bridge_server.py")], **kwargs)
        for _ in range(10):
            time.sleep(1)
            if page.is_server_running():
                logger.info("Bridge server started")
                break
        else:
            logger.warning("Bridge server start timeout. Please run bridge_server.py manually.")
            return

    if page.is_extension_connected():
        return

    logger.info("Browser extension not connected, opening Chrome...")
    _open_chrome()
    for _ in range(20):
        time.sleep(1)
        if page.is_extension_connected():
            logger.info("Browser extension connected")
            return
    logger.warning(
        "Extension connection timeout. "
        "Please ensure Chrome has the Upwork Bridge extension installed and enabled."
    )


def _open_chrome() -> None:
    import subprocess
    for cmd in [["open", "-a", "Google Chrome"], ["google-chrome"], ["chromium-browser"]]:
        try:
            subprocess.Popen(cmd)
            return
        except FileNotFoundError:
            continue
    logger.warning("Chrome not found. Please open your browser manually.")


def _connect(args: argparse.Namespace):
    from upwork.bridge import BridgePage
    bridge_url = getattr(args, "bridge_url", "ws://localhost:9337")
    _ensure_bridge_ready(bridge_url)
    return _DummyBrowser(), BridgePage(bridge_url)


# ── Subcommand implementations ────────────────────────────────────────────────

def cmd_check_login(args: argparse.Namespace) -> None:
    from upwork.login import check_login_status, get_current_username
    browser, page = _connect(args)
    try:
        logged_in = check_login_status(page)
        if logged_in:
            username = get_current_username(page)
            _output({"logged_in": True, "username": username})
        else:
            _output({"logged_in": False, "hint": "Not logged in. Please log in to Upwork in your browser."}, exit_code=1)
    finally:
        browser.close()


def cmd_delete_cookies(args: argparse.Namespace) -> None:
    from upwork.login import logout
    browser, page = _connect(args)
    try:
        logged_out = logout(page)
        _output({"success": True, "message": "Logged out" if logged_out else "Was not logged in"})
    finally:
        browser.close()


def cmd_search_jobs(args: argparse.Namespace) -> None:
    from upwork.search import search_jobs
    browser, page = _connect(args)
    try:
        results = search_jobs(
            page,
            query=args.query,
            limit=args.limit,
            sort=args.sort,
            job_type=args.job_type or "",
            min_budget=args.min_budget or 0,
        )
        _output({"jobs": [j.to_dict() for j in results], "count": len(results)})
    finally:
        browser.close()


def cmd_get_job_detail(args: argparse.Namespace) -> None:
    from upwork.job_detail import get_job_detail
    browser, page = _connect(args)
    try:
        detail = get_job_detail(page, args.url)
        _output(detail.to_dict())
    finally:
        browser.close()


def cmd_submit_proposal(args: argparse.Namespace) -> None:
    from upwork.propose import submit_proposal

    with open(args.cover_letter_file, encoding="utf-8") as f:
        cover_letter = f.read().strip()

    browser, page = _connect(args)
    try:
        result = submit_proposal(
            page,
            job_url=args.url,
            cover_letter=cover_letter,
            bid_rate=args.bid or "",
        )
        _output(result.to_dict())
    finally:
        browser.close()


def cmd_list_proposals(args: argparse.Namespace) -> None:
    from upwork.propose import list_my_proposals
    browser, page = _connect(args)
    try:
        proposals = list_my_proposals(page, limit=args.limit)
        _output({"proposals": proposals, "count": len(proposals)})
    finally:
        browser.close()


def cmd_my_profile(args: argparse.Namespace) -> None:
    from upwork.profile import get_my_profile
    browser, page = _connect(args)
    try:
        profile = get_my_profile(page)
        _output(profile)
    finally:
        browser.close()


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="upwork-cli",
        description="Upwork automation via browser extension bridge",
    )
    parser.add_argument("--bridge-url", default="ws://localhost:9337", dest="bridge_url")
    sub = parser.add_subparsers(dest="command", required=True)

    # Auth
    sub.add_parser("check-login", help="Check Upwork login status")
    sub.add_parser("delete-cookies", help="Log out of Upwork")

    # Search
    p = sub.add_parser("search-jobs", help="Search Upwork job listings")
    p.add_argument("--query", required=True, help="Search keywords")
    p.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    p.add_argument("--sort", default="recency", choices=["recency", "relevance"], help="Sort order")
    p.add_argument("--job-type", default="", choices=["", "hourly", "fixed"], dest="job_type", help="Filter by job type")
    p.add_argument("--min-budget", type=int, default=0, dest="min_budget", help="Minimum budget ($)")

    # Job detail
    p = sub.add_parser("get-job-detail", help="Get full details of a job posting")
    p.add_argument("--url", required=True, help="Upwork job URL")

    # Proposal
    p = sub.add_parser("submit-proposal", help="Submit a proposal to a job")
    p.add_argument("--url", required=True, help="Upwork job URL")
    p.add_argument(
        "--cover-letter-file",
        required=True,
        dest="cover_letter_file",
        help="Absolute path to text file containing the cover letter",
    )
    p.add_argument("--bid", default="", help="Bid amount (e.g. '45' for $45/hr or '$500' fixed)")

    # My proposals
    p = sub.add_parser("list-proposals", help="List my sent proposals")
    p.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")

    # Profile
    sub.add_parser("my-profile", help="Get my freelancer profile info")

    return parser


def main() -> None:
    # Add scripts/ dir to sys.path so `upwork` package is importable
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    parser = build_parser()
    args = parser.parse_args()
    cmd_map = {
        "check-login": cmd_check_login,
        "delete-cookies": cmd_delete_cookies,
        "search-jobs": cmd_search_jobs,
        "get-job-detail": cmd_get_job_detail,
        "submit-proposal": cmd_submit_proposal,
        "list-proposals": cmd_list_proposals,
        "my-profile": cmd_my_profile,
    }
    handler = cmd_map.get(args.command)
    if handler:
        try:
            handler(args)
        except Exception as e:
            _output({"error": str(e), "type": type(e).__name__}, exit_code=2)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
