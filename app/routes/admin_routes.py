from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.database_main import get_db
# from schemas.users_schema import User, UserResponse
from schemas.accounts_schema import CreateTag
from middlewares.auth import AuthMiddleware
from models import users_model, accounts_model, transactions_model
from datetime import datetime


router = APIRouter(
    prefix="/leverage",
    tags=["Users"]
)


@router.get("/users/admin", status_code=status.HTTP_200_OK)
def get_all_users(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    try:
        if current_user.role != "admin":
            admin_access_error()
        return db.query(users_model.User).all()
    except Exception as e:
        return f"Oops! Something went wrong!: {e}"

@router.patch("/users/{user_id}/admin")
def block_user(user_id: int, current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    try:
        if current_user.role != "admin":
            admin_access_error()
        user_exists = db.query(users_model.User).filter(users_model.User.id == user_id).first()
        if not user_exists:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "User not found!"
            )

        user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == user_id).first()
        if not user_account:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "User account not found!"
            )
        
        user_account.acc_status = "blocked"
        db.add(user_account)
        db.commit()
        return {
            "message": "Account successfully blocked!",
            "account name": f"{user_exists.first_name} {user_exists.last_name}",
            "user ID": user_id
        }
        
    except Exception as e:
        return f"Oops! Something went wrong!: {e}"


@router.patch("/accounts/users/{user_id}/admin")
def unblock_user(user_id: int, current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    try:
        if current_user.role != "admin":
            admin_access_error()
        user_exists = db.query(users_model.User).filter(users_model.User.id == user_id).first()
        if not user_exists:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "User not found!"
            )

        user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == user_id).first()
        if not user_account:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "User account not found!"
            )
        
        user_account.acc_status = "active"
        db.add(user_account)
        db.commit()
        return {
            "message": "Account successfully unblocked!",
            "account name": f"{user_exists.first_name} {user_exists.last_name}",
            "user ID": user_id
        }

    except Exception as e:
        return f"Oops! Something went wrong!: {e}"
    


@router.get("/transactions/admin", status_code=status.HTTP_200_OK)
def get_all_users(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    try:
        if current_user.role != "admin":
            admin_access_error()
        return db.query(transactions_model.Transaction).all()
    except Exception as e:
        return f"Oops! Something went wrong!: {e}"

@router.get("/accounts/admin", status_code=status.HTTP_200_OK)
def get_all_users(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    try:
        if current_user.role != "admin":
            admin_access_error()
        return db.query(accounts_model.Account).all()
    except Exception as e:
        return f"Oops! Something went wrong!: {e}"


def admin_access_error(status_code=status.HTTP_403_FORBIDDEN):
        raise HTTPException(
        status_code = status_code,
        detail = {
            "message": f"Admin access required!",
            "timestamp": f"{datetime.now()}"
            }
        )