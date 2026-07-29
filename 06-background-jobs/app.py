"""
Background jobs — email digest queue + worker.

Stack:
  API harness (app.py)
    ↓
  Worker (worker.py) — reserve → handle → ack / retry / DLQ
    ↓
  JobQueue (queue.py)     Handler (handler.py)

Run: python3 test_jobs.py
Stuck? Open PR solution/06-background-jobs → Files changed.
"""

from __future__ import annotations

from typing import Any

from handler import Handler
from queue import JobQueue
from worker import Worker

_queue: JobQueue | None = None
_handler: Handler | None = None
_worker: Worker | None = None
_max_attempts: int = 3


def reset(*, max_attempts: int = 3) -> None:
    global _queue, _handler, _worker, _max_attempts
    _max_attempts = max_attempts
    _queue = JobQueue()
    _handler = Handler()
    _worker = Worker(_queue, _handler, max_attempts=max_attempts)


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Scripted action runner used by tests.

    Actions:
      reset      — clear queue / sent log and set max_attempts
      enqueue    — put a digest job on the ready lane
      tick       — worker processes at most one job
      stats      — ready / inflight / done / dlq counts
      sent       — emails the handler actually sent
      dlq        — poison messages
      ready      — jobs waiting
      inflight   — jobs reserved but not acked
    """
    global _queue, _handler, _worker

    action = payload.get("action")

    if action == "reset":
        reset(max_attempts=int(payload.get("max_attempts", 3)))
        return {"ok": True, "action": "reset", "max_attempts": _max_attempts}

    if _queue is None or _handler is None or _worker is None:
        return {"ok": False, "error": "app_not_initialized — call reset first"}

    if action == "enqueue":
        job = _queue.enqueue(
            {
                "job_id": payload["job_id"],
                "user_id": payload["user_id"],
                "type": payload.get("type", "digest"),
                "outcomes": payload.get("outcomes", ["ok"]),
            }
        )
        return {"ok": True, "job": job, "stats": _queue.stats()}

    if action == "tick":
        result = _worker.tick()
        result["sent_count"] = len(_handler.sent())
        return result

    if action == "stats":
        return {"ok": True, **_queue.stats()}

    if action == "sent":
        return {"ok": True, "sent": _handler.sent(), "sent_count": len(_handler.sent())}

    if action == "dlq":
        return {"ok": True, "dlq": _queue.dlq(), "dlq_count": len(_queue.dlq())}

    if action == "ready":
        return {"ok": True, "ready": _queue.ready()}

    if action == "inflight":
        return {"ok": True, "inflight": _queue.inflight()}

    return {"ok": False, "error": f"unknown_action:{action}"}
