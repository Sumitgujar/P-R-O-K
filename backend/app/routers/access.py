"""Temporary authorization boundaries until role-specific product routers are added."""

from typing import Any

from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles

router = APIRouter(tags=["authorization"])


@router.get("/student/access-check")
async def student_access_check(current: dict[str, Any] = Depends(require_roles("student"))) -> dict[str, str]:
    return {"status": "ok", "role": current["role"]}


@router.get("/teacher/access-check")
async def teacher_access_check(current: dict[str, Any] = Depends(require_roles("teacher"))) -> dict[str, str]:
    return {"status": "ok", "role": current["role"]}


@router.get("/admin/access-check")
async def admin_access_check(current: dict[str, Any] = Depends(require_roles("admin"))) -> dict[str, str]:
    return {"status": "ok", "role": current["role"]}
