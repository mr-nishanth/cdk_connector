"""Client for the autoSoft order tracking API.

Consumes ``GET /api/v1/orders/{order_id}/tracking`` as published in the
upstream contract (autosoft-connector, sha256 314bf81684b6).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional
from urllib.parse import quote

import httpx

Status = Literal["pending", "shipped", "delivered"]
ALLOWED_STATUSES: tuple[str, ...] = ("pending", "shipped", "delivered")
_CONTRACT_FIELDS = frozenset({"order_id", "status", "updated_at"})


class OrderNotFound(Exception):
    """Raised when the backend reports that an order id is unknown (HTTP 404)."""

    def __init__(self, order_id: str, detail: Optional[str] = None) -> None:
        self.order_id = order_id
        self.detail = detail
        message = f"order not found: {order_id}"
        if detail:
            message = f"{message} ({detail})"
        super().__init__(message)


@dataclass(frozen=True)
class OrderTracking:
    order_id: str
    status: Status
    updated_at: str


def _parse(payload: Any) -> OrderTracking:
    if not isinstance(payload, dict):
        raise ValueError("tracking response must be a JSON object")
    fields = set(payload.keys())
    if fields != _CONTRACT_FIELDS:
        raise ValueError(
            f"tracking response must contain exactly {sorted(_CONTRACT_FIELDS)}, "
            f"got {sorted(fields)}"
        )
    order_id = payload["order_id"]
    status = payload["status"]
    updated_at = payload["updated_at"]
    if not isinstance(order_id, str):
        raise ValueError("order_id must be a string")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"unknown status value: {status!r}")
    if not isinstance(updated_at, str):
        raise ValueError("updated_at must be a string")
    return OrderTracking(order_id=order_id, status=status, updated_at=updated_at)


def get_tracking(
    base_url: str,
    order_id: str,
    *,
    client: Optional[httpx.Client] = None,
    timeout: float = 10.0,
) -> OrderTracking:
    """Fetch tracking information for ``order_id`` from the backend.

    Raises ``OrderNotFound`` on HTTP 404, ``httpx.HTTPStatusError`` for other
    non-2xx responses, and ``ValueError`` if the body does not match the contract.
    """
    url = (
        base_url.rstrip("/")
        + "/api/v1/orders/"
        + quote(order_id, safe="")
        + "/tracking"
    )
    if client is None:
        response = httpx.get(url, timeout=timeout)
    else:
        response = client.get(url)

    if response.status_code == 404:
        detail: Optional[str] = None
        try:
            body = response.json()
            if isinstance(body, dict) and isinstance(body.get("detail"), str):
                detail = body["detail"]
        except ValueError:
            pass
        raise OrderNotFound(order_id, detail)

    response.raise_for_status()
    return _parse(response.json())
