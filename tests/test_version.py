"""Offline tests for the package VERSION constant."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from order_tracking import VERSION  # noqa: E402


def test_version_is_non_empty_string():
    assert isinstance(VERSION, str)
    assert VERSION != ""


def test_version_has_three_numeric_dot_separated_parts():
    parts = VERSION.split(".")
    assert len(parts) == 3
    assert all(part.isascii() and part.isdigit() for part in parts)
