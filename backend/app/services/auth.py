from datetime import UTC, datetime, timedelta
from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password


async def register_student(database: AsyncDatabase, values: dict[str, str]) -> dict[str, Any]:
    user = {
        "email": values["email"].strip().lower(), "display_name": values["display_name"].strip(), "role": "student", "active": True,
        "password_hash": hash_password(values["password"]), "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC),
    }
    result = await database["users"].insert_one(user)
    student = {
        "user_id": result.inserted_id, "student_number": values["student_number"].strip(),
        "program": {"code": values["program_code"].strip(), "name": values["program_name"].strip()},
        "year_level": None, "academic_status": "active", "interests": [], "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC),
    }
    try:
        await database["students"].insert_one(student)
    except Exception:
        await database["users"].delete_one({"_id": result.inserted_id})
        raise
    return {**user, "_id": result.inserted_id}


async def authenticate(database: AsyncDatabase, email: str, password: str) -> dict[str, Any] | None:
    user = await database["users"].find_one({"email": email.strip().lower(), "active": True})
    if user is None or not verify_password(password, user.get("password_hash", "")):
        return None
    return user


def token_response(user: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return {"access_token": create_access_token(str(user["_id"]), user["role"]), "expires_in": settings.access_token_expire_minutes * 60}


def token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(minutes=get_settings().access_token_expire_minutes)
