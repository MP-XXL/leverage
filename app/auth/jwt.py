import os
from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta, datetime


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ACCESS_TOKEN_EXPIRATION_IN_MINUTES = int(os.getenv('JWT_EXPIRATION_TIME'))
ALGORITHM = os.getenv('JWT_ALGORITHM')

def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None)-> str:
    try:
        if expires_delta:
            expiration_time = datetime.now() + expires_delta
        else:
            expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_IN_MINUTES)
        
        claims.update({"exp": expiration_time})

        return jwt.encode(claims, SECRET_KEY, ALGORITHM)

    except JWTError as e:
        raise e

