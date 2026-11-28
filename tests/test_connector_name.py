"""Offline tests for the CONNECTOR_NAME constant in order_tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import order_tracking  # noqa: E402
from order_tracking import CONNECTOR_NAME  # noqa: E402


def test_connector_name_value():
    assert CONNECTOR_NAME == "cdk"


def test_connector_name_is_str():
    assert isinstance(CONNECTOR_NAME, str)


def test_connector_name_is_exported():
    assert "CONNECTOR_NAME" in order_tracking.__all__
