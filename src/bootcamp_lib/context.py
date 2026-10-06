"""Resolve the catalog and schema a participant works in.

In `mode: development` the bundle prefixes resource names with
`dev_<short_name>_`, where short_name is the user part of the e-mail with
non-alphanumeric characters replaced by underscores. Notebooks use this
helper so every participant lands in their own schema automatically.
"""
from __future__ import annotations

import re


def short_name(user_email: str) -> str:
    local = user_email.split("@", 1)[0].lower()
    return re.sub(r"[^a-z0-9]", "_", local)


def dev_schema(user_email: str, base: str = "sales") -> str:
    return f"dev_{short_name(user_email)}_{base}"


def resolve(catalog: str, schema: str, user_email: str) -> tuple[str, str]:
    """Return (catalog, schema); an empty schema means 'my dev schema'."""
    return catalog or "bootcamp_dev", schema or dev_schema(user_email)
