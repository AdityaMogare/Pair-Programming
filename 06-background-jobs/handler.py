"""Digest email handler — scripted outcomes per job for deterministic tests."""

from __future__ import annotations

from typing import Any


class TransientError(Exception):
    """Retryable worker failure (SMTP blip, lock timeout, …)."""


class Handler:
    def __init__(self) -> None:
        self._sent: list[dict[str, Any]] = []
        self._outcome_cursors: dict[str, int] = {}

    def reset(self) -> None:
        self._sent.clear()
        self._outcome_cursors.clear()

    def sent(self) -> list[dict[str, Any]]:
        return [dict(s) for s in self._sent]

    def handle(self, job: dict[str, Any]) -> dict[str, Any]:
        job_id = job["job_id"]
        outcomes = job.get("outcomes") or ["ok"]
        idx = self._outcome_cursors.get(job_id, 0)
        if idx >= len(outcomes):
            outcome = outcomes[-1]
        else:
            outcome = outcomes[idx]
            self._outcome_cursors[job_id] = idx + 1

        if outcome == "fail":
            raise TransientError(f"smtp_unavailable:{job_id}")
        if outcome == "crash":
            raise RuntimeError(f"worker_segfault:{job_id}")

        entry = {
            "job_id": job_id,
            "user_id": job["user_id"],
            "type": job.get("type", "digest"),
        }
        self._sent.append(entry)
        return {"ok": True, "sent": entry}
