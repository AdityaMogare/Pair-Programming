"""Queue worker — reserve → handle → ack / retry / DLQ."""

from __future__ import annotations

from typing import Any

from handler import Handler, TransientError
from queue import JobQueue


class Worker:
    def __init__(self, queue: JobQueue, handler: Handler, *, max_attempts: int = 3) -> None:
        self._queue = queue
        self._handler = handler
        self._max_attempts = max_attempts
        self._ticks = 0

    def tick(self) -> dict[str, Any]:
        """Process at most one job. Returns a small status payload for tests."""
        self._ticks += 1

        # Visibility timeout: anything left inflight from a prior crash/missed ack
        # becomes ready again (this is how missing acks create duplicate sends).
        redelivered = self._queue.requeue_stale_inflight()

        job = self._queue.reserve()
        if job is None:
            return {
                "ok": True,
                "processed": False,
                "redelivered": redelivered,
                "stats": self._queue.stats(),
            }

        job_id = job["job_id"]
        try:
            result = self._handler.handle(job)
        except TransientError as exc:
            next_attempts = int(job.get("attempts", 0)) + 1
            if next_attempts >= self._max_attempts:
                self._queue.dead_letter(job_id)
                action = "dlq"
            else:
                self._queue.nack(job_id)
                action = "nack"
            return {
                "ok": False,
                "processed": True,
                "job_id": job_id,
                "error": str(exc),
                "attempts": next_attempts,
                "action": action,
                "redelivered": redelivered,
                "stats": self._queue.stats(),
            }
        except Exception as exc:  # noqa: BLE001
            # Unexpected crash — dead-letter so the job does not stick inflight.
            self._queue.dead_letter(job_id)
            return {
                "ok": False,
                "processed": True,
                "job_id": job_id,
                "error": str(exc),
                "action": "dlq",
                "redelivered": redelivered,
                "stats": self._queue.stats(),
            }

        self._queue.ack(job_id)
        return {
            "ok": True,
            "processed": True,
            "job_id": job_id,
            "action": "ack",
            "result": result,
            "redelivered": redelivered,
            "stats": self._queue.stats(),
        }
