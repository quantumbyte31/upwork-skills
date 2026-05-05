"""BridgePage — Page-compatible API via Upwork browser extension bridge.

CLI commands are sent via WebSocket to bridge_server.py,
which forwards them to the browser extension for execution.
Each call is a short-lived connection (send one command, receive one reply).
"""

from __future__ import annotations

import json
import time
from typing import Any

import websockets.sync.client as ws_client

from .errors import BridgeError, ElementNotFoundError

BRIDGE_URL = "ws://localhost:9337"


class BridgePage:
    def __init__(self, bridge_url: str = BRIDGE_URL, timeout: float = 90.0) -> None:
        self._url = bridge_url
        self._timeout = timeout

    def _send(self, method: str, params: dict | None = None) -> Any:
        msg = {"role": "cli", "method": method, "params": params or {}}
        try:
            with ws_client.connect(self._url, open_timeout=10) as ws:
                ws.send(json.dumps(msg))
                raw = ws.recv(timeout=self._timeout)
        except OSError as e:
            raise BridgeError(f"Cannot connect to bridge at {self._url}: {e}") from e
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise BridgeError(f"Invalid JSON from bridge: {e}") from e
        if "error" in data:
            raise BridgeError(data["error"])
        return data.get("result")

    # ── Server health ──────────────────────────────────────────────

    def is_server_running(self) -> bool:
        try:
            self._send("ping_server")
            return True
        except BridgeError:
            return False
        except OSError:
            return False

    def is_extension_connected(self) -> bool:
        try:
            result = self._send("ping_server")
            return bool(result and result.get("extension_connected"))
        except Exception:
            return False

    # ── Navigation ────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        self._send("navigate", {"url": url})

    def get_url(self) -> str:
        return self._send("get_url") or ""

    def wait_for_load(self, timeout: float = 30.0) -> None:
        self._send("wait_for_load", {"timeout": int(timeout * 1000)})

    def wait_dom_stable(self, timeout: float = 10.0) -> None:
        self._send("wait_dom_stable", {"timeout": int(timeout * 1000), "interval": 500})

    # ── DOM queries ───────────────────────────────────────────────

    def evaluate(self, js: str) -> Any:
        return self._send("evaluate", {"expression": js})

    def has_element(self, selector: str) -> bool:
        return bool(self._send("has_element", {"selector": selector}))

    def get_element_text(self, selector: str) -> str:
        return self._send("get_element_text", {"selector": selector}) or ""

    def get_attribute(self, selector: str, attr: str) -> str:
        return self._send("get_element_attribute", {"selector": selector, "attr": attr}) or ""

    def get_elements_count(self, selector: str) -> int:
        return int(self._send("get_elements_count", {"selector": selector}) or 0)

    def wait_for_selector(self, selector: str, timeout: float = 30.0) -> bool:
        result = self._send("wait_for_selector", {"selector": selector, "timeout": int(timeout * 1000)})
        return bool(result)

    # ── DOM actions ───────────────────────────────────────────────

    def click_element(self, selector: str) -> None:
        result = self._send("click_element", {"selector": selector})
        if isinstance(result, dict) and "__error" in result:
            raise ElementNotFoundError(selector)

    def fill_input(self, selector: str, text: str) -> None:
        result = self._send("fill_input", {"selector": selector, "text": text})
        if isinstance(result, dict) and "__error" in result:
            raise ElementNotFoundError(selector)

    def fill_textarea(self, selector: str, text: str) -> None:
        result = self._send("fill_textarea", {"selector": selector, "text": text})
        if isinstance(result, dict) and "__error" in result:
            raise ElementNotFoundError(selector)

    def scroll_to_bottom(self, step: int = 600, delay_ms: int = 700) -> None:
        self._send("scroll_to_bottom", {"step": step, "delay": delay_ms})

    def scroll_down(self, amount: int = 600) -> None:
        self._send("scroll_down", {"amount": amount})

    def get_cookies(self) -> list[dict]:
        return self._send("get_cookies", {"domain": "upwork.com"}) or []
