from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.database_main import get_db
from schemas.users_schema import User, UserResponse
from schemas.accounts_schema import CreateTag
from middlewares.auth import AuthMiddleware
from models import users_model, accounts_model
import bcrypt


router = APIRouter(
    prefix="/leverage",
    tags=["Users"]
)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user: User, db: Session=Depends(get_db)):
    user_exists = db.query(users_model.User).filter((users_model.User.email == user.email) | (user.phone == users_model.User.phone)).first()
    if user_exists:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "email or phone already exists"
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

    return new_user


@router.post("/tags/users", status_code=status.HTTP_201_CREATED)
def create_leverage_tag(tag: CreateTag, current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    if current_user.verification.value != "verified":
         raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User is not verified!"
            )
    get_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not get_account:
        new_account = accounts_model.Account(
            user_id = current_user.id,
            leverage_tag = tag.leverage_tag.lower()
            )

        db.add(new_account)
        db.commit()
        db.refresh(new_account)

        return new_account

    if get_account:
        get_account.leverage_tag = tag.leverage_tag.lower()

        db.add(get_account)
        db.commit()
        db.refresh(get_account)

        return get_account


@router.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    db.delete(current_user)
    db.commit()