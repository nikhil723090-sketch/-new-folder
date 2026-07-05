"""Role and permission definitions."""

from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    INVESTIGATOR = "investigator"
    SUPERVISOR = "supervisor"


PERMISSIONS = {
    Role.ADMIN: {"*"},
    Role.INVESTIGATOR: {"cases:view_assigned", "chat:ask", "reports:download"},
    Role.ANALYST: {"analytics:run", "hotspots:run", "predictions:run", "chat:ask"},
    Role.SUPERVISOR: {"reports:approve", "reports:view", "audit:view"},
}


def has_permission(role: Role, permission: str) -> bool:
    allowed = PERMISSIONS.get(role, set())
    return "*" in allowed or permission in allowed
