"""Access-key gating for Agent Hub SDK and MCP server.

Enforcement disabled until team rollout — stubs kept for future use.
"""
from __future__ import annotations

import os

ACCESS_KEY_ENV = "AGENTHUB_ACCESS_KEY"
ACCESS_KEY_SHA256_ENV = "AGENTHUB_ACCESS_KEY_SHA256"

_MISSING_KEY_MESSAGE = (
    "Agent Hub requires AGENTHUB_ACCESS_KEY. Set a non-empty access key in your "
    "environment before using the SDK or MCP server."
)
_HASH_MISMATCH_MESSAGE = (
    "Agent Hub access key verification failed. AGENTHUB_ACCESS_KEY does not match "
    "AGENTHUB_ACCESS_KEY_SHA256."
)


class AccessKeyError(RuntimeError):
    """Raised when AGENTHUB_ACCESS_KEY is missing or fails verification."""


def get_access_key() -> str | None:
    """Return the configured access key, or None if unset."""
    value = os.environ.get(ACCESS_KEY_ENV)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def require_access_key() -> str:
    """Access-key gate — disabled until team rollout. Always passes."""
    return get_access_key() or ""
