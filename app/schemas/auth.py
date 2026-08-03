from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    LOAN_OFFICER = "Loan Officer"
    CUSTOMER = "Customer"


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@gmail.com",
                "password": "Admin@123",
                "role": "Admin"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "Admin@123"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"