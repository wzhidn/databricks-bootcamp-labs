"""Business rules shared by pipelines, notebooks and unit tests.

Keeping the rules as plain Python makes them unit-testable in CI (lab 06)
without a Spark cluster. The SQL expectations in src/pipelines mirror them.
"""
from __future__ import annotations

VALID_REGIONS = {"EMEA", "NA", "LATAM", "APAC"}


def normalize_region(region: str | None) -> str | None:
    """Upper-case and trim a region code; unknown values become None."""
    if region is None:
        return None
    value = region.strip().upper()
    return value if value in VALID_REGIONS else None


def is_valid_order(record: dict) -> bool:
    """An order is valid if it has a customer, a positive amount and quantity."""
    return (
        record.get("customer_id") is not None
        and (record.get("amount") or 0) > 0
        and (record.get("quantity") or 0) > 0
    )


def discount_rate(coupon_code: str | None) -> float:
    """Discount implied by a coupon code (used in lab 01 schema-drift exercise)."""
    return {"WELCOME10": 0.10, "SPRING15": 0.15, "VIP20": 0.20}.get((coupon_code or "").upper(), 0.0)
