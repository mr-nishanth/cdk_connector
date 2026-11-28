"""Order tracking client package."""

from order_tracking.client import (
    ALLOWED_STATUSES,
    OrderNotFound,
    OrderTracking,
    Status,
    get_tracking,
)

VERSION = "0.1.0"

__all__ = [
    "ALLOWED_STATUSES",
    "OrderNotFound",
    "OrderTracking",
    "Status",
    "VERSION",
    "get_tracking",
]
