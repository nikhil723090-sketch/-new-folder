"""FastAPI helpers for role-based access control."""

from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth import verify_access_token
from .rbac import Role, has_permission


security = HTTPBearer()


def require_permission(permission: str):
    """FastAPI dependency factory for permission checks."""

    def dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        payload = verify_access_token(credentials.credentials)
        role = Role(payload["role"])
        if not has_permission(role, permission):
            raise HTTPException(status_code=403, detail="Permission denied")
        return payload

    return dependency
