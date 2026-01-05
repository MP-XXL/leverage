from pydantic import BaseModel, Field, validator, model_validator, EmailStr
from fastapi import HTTPException, status
from decimal import Decimal
from datetime import datetime, date
from typing import  Optional
import re



class CreateTag(BaseModel):
    leverage_tag: str = Field(min_length=5, max_length=20)

    @validator("leverage_tag")
    def leverage_tag(cls, value):
        if value.isspace() is True:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Leverage_tag can not be blank!"
                )
        return value

    @validator("leverage_tag")
    def leverage_tag_space(cls, value):
        for character in value:
            if character == " ":
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail = "Spaces are not allowed in tag names"
                    )
        return value


class UserTransaction(BaseModel):
    amount: Decimal = Field(ge=1, max_digits=10, decimal_places=2)
    leverage_tag: str = Field(min_length=5, max_length=20)
    description: str = Field(max_length=200)

    @validator("amount")
    def check_amount(cls, value):
        if value < 1:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Amount can not be less than 1"
            )
        return value

class UserTransactionResponse(BaseModel):
    amount: float = Field(ge=1)
    leverage_tag: str = Field(min_length=5, max_length=20)
    description: str = Field(max_length=200)
 
