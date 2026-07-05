"""JWT helpers for authentication."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from .rbac import Role


def create_access_token(user_id: str, role: Role, expires_minutes: int = 60) -> str:
    """Create a signed JWT access token."""

    import jwt

    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def verify_access_token(token: str) -> dict:
    """Decode and verify a signed JWT access token."""

    import jwt

    return jwt.decode(token, _secret(), algorithms=["HS256"])


def _secret() -> str:
    return os.getenv("JWT_SECRET", "change-this-secret")
