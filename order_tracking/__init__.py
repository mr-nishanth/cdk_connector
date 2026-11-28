"""Order tracking client package."""

from order_tracking.client import (
    ALLOWED_STATUSES,
    OrderNotFound,
    OrderTracking,
    Status,
    get_tracking,
)

CONNECTOR_NAME = "cdk"

__all__ = [
    "ALLOWED_STATUSES",
    "CONNECTOR_NAME",
    "OrderNotFound",
    "OrderTracking",
    "Status",
    "get_tracking",
]
