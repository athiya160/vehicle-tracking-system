from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    route_id: Optional[int] = None
    vehicle_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    route_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
