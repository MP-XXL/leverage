from pydantic import BaseModel, Field, validator, EmailStr
from fastapi import HTTPException, status
import re


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)
   
    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str
    user_id: int