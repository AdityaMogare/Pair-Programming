"""HTTP-shaped API handlers over the profile service."""

from __future__ import annotations

from typing import Any

from service import ProfileService


class ProfileAPI:
    def __init__(self, service: ProfileService) -> None:
        self._service = service

    def get(self, user_id: str) -> dict[str, Any]:
        profile = self._service.get_profile(user_id)
        if profile is None:
            return {"ok": False, "status": 404, "error": "not_found"}
        body = {k: v for k, v in profile.items() if not k.startswith("_")}
        return {
            "ok": True,
            "status": 200,
            "source": profile.get("_source"),
            "profile": body,
        }

    def patch(self, user_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        profile = self._service.update_profile(user_id, fields)
        if profile is None:
            return {"ok": False, "status": 404, "error": "not_found"}
        body = {k: v for k, v in profile.items() if not k.startswith("_")}
        return {
            "ok": True,
            "status": 200,
            "source": profile.get("_source"),
            "profile": body,
        }
