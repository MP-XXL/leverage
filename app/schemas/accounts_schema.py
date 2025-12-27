from pydantic import BaseModel, Field, validator, model_validator, EmailStr
from fastapi import HTTPException, status
from datetime import datetime, date
from typing import  Optional
import re



class CreateTag(BaseModel):
    leverage_tag: str = Field(min_length=5, max_length=20)

    @validator('leverage_tag')
    def leverage_tag(cls, value):
        if value.isspace() is True:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Leverage_tag can not be blank!'
                )
        return value

    @validator('leverage_tag')
    def leverage_tag_space(cls, value):
        for character in value:
            if character == " ":
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = 'Spaces are not allowed in tag names'
                    )
        return value
 
