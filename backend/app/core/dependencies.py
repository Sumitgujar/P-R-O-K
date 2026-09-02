from collections.abc import Callable
from typing import Any

import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.db.mongodb import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().api_v1_prefix}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), database: AsyncDatabase = Depends(get_database)
) -> dict[str, Any]:
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decode_access_token(token)
        user_id, token_id = payload.get("sub"), payload.get("jti")
        if not isinstance(user_id, str) or not isinstance(token_id, str) or not ObjectId.is_valid(user_id):
            raise credentials_error
    except (jwt.PyJWTError, ValueError):
        raise credentials_error from None
    if await database["revoked_tokens"].find_one({"jti": token_id}) is not None:
        raise credentials_error
    user = await database["users"].find_one({"_id": ObjectId(user_id), "active": True})
    if user is None:
        raise credentials_error
    return user


def require_roles(*allowed_roles: str) -> Callable[..., Any]:
    async def role_guard(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role permissions")
        return current_user
    return role_guard
