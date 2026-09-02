from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

UserRole = Literal["student", "teacher", "admin"]


class StudentRegistrationRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=12, max_length=128)
    student_number: str = Field(min_length=1, max_length=40)
    program_code: str = Field(min_length=1, max_length=30)
    program_name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class CurrentUserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    role: UserRole


class LogoutResponse(BaseModel):
    status: Literal["logged_out"]
    revoked_until: datetime
