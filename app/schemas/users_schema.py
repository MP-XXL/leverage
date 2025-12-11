from pydantic import BaseModel, Field, validator, model_validator, EmailStr
from fastapi import HTTPException, status
from datetime import datetime, date
from typing import  Optional
import re


class User(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: EmailStr
    phone: str = Field(min_length=11, pattern=r"\d")
    password: str = Field(min_length=6, max_length=50)
    confirm_password: str = Field(min_length=6, max_length=50)
    date_of_birth: date
    address: str = Field(min_length=10, max_length=150)


    @validator('phone')
    def phone_is_valid_numeric_value(cls, value):
        if value.isdigit() is not True:
            raise ValueError('phone number must be digits')
        return value


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

    
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

    @validator('first_name')
    def check_first_name(cls, value):
        if any(char.isdigit() for char in value):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not contain numbers'
                )
        return value

    @validator('last_name')
    def check_last_name(cls, value):
        if any(char.isdigit() for char in value):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not contain numbers'
                )
        return value
    
    @validator('first_name')
    def first_name(cls, value):
        if value.isspace() is True:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not be blank!'
                )
        return value

    @validator('last_name')
    def validate_last_name(cls, value):
        if value.isspace() is True:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not be blank!'
                )
        return value

    @validator('date_of_birth')
    def validate_name(cls, value):
        if value > date.today():
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Invalid date!'
                )
        return value



class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str 

