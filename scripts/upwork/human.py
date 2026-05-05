"""Human behavior simulation — delays, rate limiting, action logging."""

from __future__ import annotations

import json
import logging
import random
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def sleep_random(min_ms: int, max_ms: int) -> None:
    delay = random.randint(max(min_ms, 1), max(max_ms, min_ms + 1)) / 1000.0
    time.sleep(delay)


def sleep_gaussian(mean_ms: int, std_ms: int) -> None:
    delay = max(100, random.gauss(mean_ms, std_ms)) / 1000.0
    time.sleep(delay)


BAN_KEYWORDS = [
    "your account has been suspended",
    "restricted",
    "unusual activity",
    "verify your identity",
    "too many requests",
    "rate limit",
    "captcha",
    "prove you are human",
]


class RateLimiter:
    """Session-level rate limiter for Upwork safety thresholds."""

    DEFAULT_LIMITS: dict[str, int] = {
        "search": 60,
        "job_view": 80,
        "proposal": 10,     # Upwork limits proposals; stay conservative
        "message": 20,
        "general": 100,
    }

    def __init__(self, limits: dict[str, int] | None = None) -> None:
        self._limits = {**self.DEFAULT_LIMITS, **(limits or {})}
        self._actions: dict[str, list[float]] = {}

    def _prune(self, action_type: str) -> None:
        cutoff = time.time() - 3600
        self._actions[action_type] = [t for t in self._actions.get(action_type, []) if t > cutoff]

    def can_act(self, action_type: str = "general") -> bool:
        self._prune(action_type)
        limit = self._limits.get(action_type, self._limits["general"])
        return len(self._actions.get(action_type, [])) < limit

    def record(self, action_type: str = "general") -> None:
        self._actions.setdefault(action_type, []).append(time.time())

    def remaining(self, action_type: str = "general") -> int:
        self._prune(action_type)
        limit = self._limits.get(action_type, self._limits["general"])
        return max(0, limit - len(self._actions.get(action_type, [])))


class ActionLogger:
    """Append-only JSONL log for all Upwork actions."""

    def __init__(self, log_path: str | None = None) -> None:
        self._path = Path(log_path or Path.home() / ".upwork-skills" / "actions.jsonl")
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, action: str, target_url: str, target_name: str = "",
            success: bool = True, details: dict | None = None) -> None:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "action": action,
            "target_url": target_url,
            "target_name": target_name,
            "success": success,
        }
        if details:
            entry["details"] = details
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def recent(self, n: int = 20) -> list[dict]:
        if not self._path.exists():
            return []
        with open(self._path, encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(line) for line in lines[-n:]]
