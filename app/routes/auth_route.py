from sqlalchemy.orm import Session
from database.database_main import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from models.users_model import User
from auth.jwt import create_access_token
from schemas.auth import LoginRequest, LoginResponse
from datetime import datetime
import bcrypt


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session=Depends(get_db)):

    user_exists = db.query(User).filter(login_request.email == User.email).first()

    if not user_exists:
        raiseHTTPException("email does not exists!")

    password_match = verify_password(login_request.password, user_exists.password)

    if not password_match:
        raiseHTTPException("Invalid password")

    claims = {
        "sub": str(user_exists.id),
        "email": user_exists.email,
        "user_id": str(user_exists.id)
    }

    access_token = create_access_token(claims)

    return LoginResponse(
        access_token = access_token,
        token_type = "Bearer",
        email = user_exists.email,
        user_id = user_exists.id
    )


def verify_password(plain_text_password: str, hashed_password: str)-> bool:
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))


def raiseHTTPException(e, status=status.HTTP_401_UNAUTHORIZED):
    raise HTTPException(
        status_code = status,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )