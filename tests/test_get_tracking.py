"""Offline tests for order_tracking.get_tracking using httpx.MockTransport."""

import json
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from order_tracking import (  # noqa: E402
    OrderNotFound,
    OrderTracking,
    get_tracking,
    is_final_status,
)

BASE = "https://backend.example"
OK_BODY = {
    "order_id": "ORD-1001",
    "status": "shipped",
    "updated_at": "2024-05-01T10:00:00+00:00",
}


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_200_parses_into_order_tracking():
    client = _client(lambda req: httpx.Response(200, json=OK_BODY))
    result = get_tracking(BASE, "ORD-1001", client=client)
    assert result == OrderTracking(
        order_id="ORD-1001",
        status="shipped",
        updated_at="2024-05-01T10:00:00+00:00",
    )


def test_request_is_get_to_contract_path_without_body():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["body"] = request.content
        return httpx.Response(200, json=OK_BODY)

    get_tracking(BASE, "ORD-1001", client=_client(handler))
    assert seen["method"] == "GET"
    assert seen["path"] == "/api/v1/orders/ORD-1001/tracking"
    assert seen["body"] == b""


def test_trailing_slash_in_base_url_is_handled():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        return httpx.Response(200, json=OK_BODY)

    get_tracking(BASE + "/", "ORD-1001", client=_client(handler))
    assert seen["path"] == "/api/v1/orders/ORD-1001/tracking"


def test_order_id_with_reserved_characters_is_percent_encoded():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["raw_path"] = request.url.raw_path.decode()
        return httpx.Response(
            404, json={"detail": "not found"}
        )

    with pytest.raises(OrderNotFound):
        get_tracking(BASE, "ORD/1 ?x#y", client=_client(handler))
    assert seen["raw_path"] == "/api/v1/orders/ORD%2F1%20%3Fx%23y/tracking"


def test_404_with_detail_raises_order_not_found_with_order_id():
    client = _client(lambda req: httpx.Response(404, json={"detail": "no such order"}))
    with pytest.raises(OrderNotFound) as exc_info:
        get_tracking(BASE, "ORD-9999", client=client)
    assert "ORD-9999" in str(exc_info.value)
    assert "no such order" in str(exc_info.value)
    assert exc_info.value.order_id == "ORD-9999"


def test_404_without_json_body_still_raises_order_not_found():
    client = _client(lambda req: httpx.Response(404, content=b"<html>nope</html>"))
    with pytest.raises(OrderNotFound) as exc_info:
        get_tracking(BASE, "ORD-9999", client=client)
    assert "ORD-9999" in str(exc_info.value)


def test_500_raises_http_status_error():
    client = _client(lambda req: httpx.Response(500, json={"detail": "boom"}))
    with pytest.raises(httpx.HTTPStatusError):
        get_tracking(BASE, "ORD-1001", client=client)


def test_unknown_status_value_is_rejected():
    body = dict(OK_BODY, status="lost")
    client = _client(lambda req: httpx.Response(200, json=body))
    with pytest.raises(ValueError):
        get_tracking(BASE, "ORD-1001", client=client)


def test_updated_at_is_returned_as_contract_string():
    client = _client(lambda req: httpx.Response(200, json=OK_BODY))
    result = get_tracking(BASE, "ORD-1001", client=client)
    assert isinstance(result.updated_at, str)
    assert result.updated_at == "2024-05-01T10:00:00+00:00"


def test_unexpected_extra_field_is_rejected():
    body = dict(OK_BODY, extra="x")
    client = _client(lambda req: httpx.Response(200, json=body))
    with pytest.raises(ValueError):
        get_tracking(BASE, "ORD-1001", client=client)


def test_is_final_status_delivered_is_true():
    assert is_final_status("delivered") is True


def test_is_final_status_pending_is_false():
    assert is_final_status("pending") is False


def test_is_final_status_shipped_is_false():
    assert is_final_status("shipped") is False


@pytest.mark.parametrize("value", ["lost", "", "Delivered"])
def test_is_final_status_unknown_value_raises_value_error(value):
    with pytest.raises(ValueError):
        is_final_status(value)
