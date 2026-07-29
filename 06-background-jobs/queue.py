"""In-memory job queue with ready / inflight / DLQ lanes."""

from __future__ import annotations

from typing import Any


class JobQueue:
    def __init__(self) -> None:
        self._ready: list[dict[str, Any]] = []
        self._inflight: dict[str, dict[str, Any]] = {}
        self._done: dict[str, dict[str, Any]] = {}
        self._dlq: list[dict[str, Any]] = []

    def enqueue(self, job: dict[str, Any]) -> dict[str, Any]:
        row = {
            "job_id": job["job_id"],
            "type": job.get("type", "digest"),
            "user_id": job["user_id"],
            "attempts": int(job.get("attempts", 0)),
            "outcomes": list(job.get("outcomes", ["ok"])),
        }
        self._ready.append(row)
        return dict(row)

    def requeue_stale_inflight(self) -> list[str]:
        """Return unacked inflight jobs to the ready lane (visibility timeout)."""
        returned: list[str] = []
        for job_id, job in list(self._inflight.items()):
            returned.append(job_id)
            self._ready.append(dict(job))
            del self._inflight[job_id]
        return returned

    def reserve(self) -> dict[str, Any] | None:
        if not self._ready:
            return None
        job = self._ready.pop(0)
        self._inflight[job["job_id"]] = dict(job)
        return dict(job)

    def ack(self, job_id: str) -> bool:
        job = self._inflight.pop(job_id, None)
        if job is None:
            return False
        self._done[job_id] = dict(job)
        return True

    def nack(self, job_id: str) -> bool:
        """Requeue after a transient failure; bump attempts."""
        job = self._inflight.pop(job_id, None)
        if job is None:
            return False
        job = dict(job)
        job["attempts"] = int(job.get("attempts", 0)) + 1
        self._ready.append(job)
        return True

    def dead_letter(self, job_id: str) -> bool:
        job = self._inflight.pop(job_id, None)
        if job is None:
            return False
        job = dict(job)
        job["attempts"] = int(job.get("attempts", 0)) + 1
        self._dlq.append(job)
        return True

    def ready(self) -> list[dict[str, Any]]:
        return [dict(j) for j in self._ready]

    def inflight(self) -> list[dict[str, Any]]:
        return [dict(j) for j in self._inflight.values()]

    def done(self) -> list[dict[str, Any]]:
        return [dict(j) for j in self._done.values()]

    def dlq(self) -> list[dict[str, Any]]:
        return [dict(j) for j in self._dlq]

    def stats(self) -> dict[str, int]:
        return {
            "ready": len(self._ready),
            "inflight": len(self._inflight),
            "done": len(self._done),
            "dlq": len(self._dlq),
        }
