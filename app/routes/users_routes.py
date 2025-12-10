from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.database_main import get_db
from schema.users_schema import User, UserResponse
from models import users_model
import bcrypt


router = APIRouter(
    prefix="/leverage",
    tags=["Users"]
)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user: User, db: Session=Depends(get_db)):
    user_exists = db.query(users_model.User).filter(users_model.User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "email already exists"
            )

    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user.password.encode("utf8"), salts)
    
    new_user = users_model.User(
        **user.dict(exclude={"password", "confirm_password"}),
        password = hashed_password.decode()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration Sucessful!",
        "data": new_user
    }