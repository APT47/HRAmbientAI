import base64
from typing import Any

import requests

from hr_ambient_ai.config import settings


class HiBobClient:
    """Thin client for the HiBob REST API v1."""

    def __init__(self) -> None:
        token = base64.b64encode(
            f"{settings.hibob_service_user_id}:{settings.hibob_token}".encode()
        ).decode()
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._base = settings.hibob_base_url

    def _url(self, path: str) -> str:
        return f"{self._base}/{path.lstrip('/')}"

    def get_employee(self, employee_id: str) -> dict[str, Any]:
        resp = requests.get(self._url(f"/people/{employee_id}"), headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    def search_employees(self, email: str | None = None) -> list[dict[str, Any]]:
        params = {"email": email} if email else {}
        resp = requests.get(self._url("/people"), headers=self._headers, params=params)
        resp.raise_for_status()
        return resp.json().get("employees", [])

    def update_field(self, employee_id: str, field_path: str, value: Any) -> dict[str, Any]:
        """Update a single field on an employee record.

        Args:
            employee_id: HiBob internal employee ID.
            field_path:  Dot-separated HiBob field path, e.g. 'work.title'.
            value:       New value to set.
        """
        url = self._url(f"/people/{employee_id}/fields/{field_path}")
        resp = requests.put(url, json={"value": value}, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    def list_fields(self) -> list[dict[str, Any]]:
        """Return all available people fields (useful for discovering field paths)."""
        resp = requests.get(self._url("/company/people/fields"), headers=self._headers)
        resp.raise_for_status()
        return resp.json().get("fields", [])
