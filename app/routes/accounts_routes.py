from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.database_main import get_db
# from schemas.users_schema import User, UserResponse
from schemas.accounts_schema import UserTransaction, UserTransactionResponse
from middlewares.auth import AuthMiddleware
from models import users_model, accounts_model, transactions_model
from enums import TransactionType
from datetime import datetime

class UserNotVerfiedError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass
class UserAccountStatusError(Exception):
    pass
class ReceiverNotFoundError(Exception):
    pass



router = APIRouter(
    prefix="/leverage",
    tags=["Accounts"]
)


@router.post("/accounts", status_code=status.HTTP_200_OK)
def leverage_tag_transfers(transaction: UserTransaction, current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):

    try:
        if current_user.verification.value != "verified":
            raise UserNotVerfiedError
        user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
        if user_account.acc_status.value != "active":
            raise UserAccountStatusError
        if user_account.acc_balance < transaction.amount:
            raise InsufficientFundsError
        
        receiver_account = db.query(accounts_model.Account).filter(accounts_model.Account.leverage_tag == transaction.leverage_tag.lower()).first()
        if not receiver_account:
            raise ReceiverNotFoundError

        user_account.acc_balance -= transaction.amount
        receiver_account.acc_balance += transaction.amount
        db.add(user_account)
        db.add(receiver_account)
        db.commit()

        sender_transaction = transactions_model.Transaction(
            sender_acc_id = user_account.id,
            amount = transaction.amount,
            receiver_acc_id = receiver_account.id,
            transaction_type = TransactionType.debit,
            description = transaction.description
        )

        # receiver_transaction = transactions_model.Transaction(
        #     sender_acc_id = user_account.id,
        #     amount = transaction.amount,
        #     receiver_acc_id = receiver_account.id,
        #     transaction_type = TransactionType.credit,
        #     description = transaction.description
        # )

        db.add(sender_transaction)
        # db.add(receiver_transaction)
        db.commit()

        return {
            "success": True,
            "amount": transaction.amount,
            "receiver": transaction.leverage_tag,
            "message": "Funds transfered successfully!"
        }

    except ReceiverNotFoundError:
        return f"The leverage tag \'{transaction.leverage_tag}\' does not exist!"
    except UserAccountStatusError:
        return f"Dear, {current_user.first_name}, can not perform transaction. Your account has been blocked due to suspicious acitvity or inactivity"
    except UserNotVerfiedError:
        return f"Dear {current_user.first_name}, your account is yet to be verified"
    except InsufficientFundsError:
        return "Your account balance is lower than sending amount"
    except Exception as e:
        return f"Oops! something went wrong {e}"

@router.get("/history", status_code=status.HTTP_200_OK)
def get_account_history(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not user_account:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User account not found. Create a leverage tag or request for account number"
        )
    transaction_history = db.query(transactions_model.Transaction).filter(
        (transactions_model.Transaction.receiver_acc_id == user_account.id) | (transactions_model.Transaction.sender_acc_id == user_account.id)
        ).all()
    return transaction_history
