from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.database_main import get_db
# from schemas.users_schema import User, UserResponse
from schemas.accounts_schema import UserTransaction, UserTransactionResponse, FundUser
from middlewares.auth import AuthMiddleware
from models import users_model, accounts_model, transactions_model, ledger_model
from enums import TransactionType, Type
from datetime import datetime

class UserNotVerfiedError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass
class UserAccountStatusError(Exception):
    pass
class ReceiverNotFoundError(Exception):
    pass
class ImproperFlowError(Exception):
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
        if receiver_account.leverage_tag == user_account.leverage_tag:
            raise ImproperFlowError

        user_account.acc_balance -= transaction.amount
        receiver_account.acc_balance += transaction.amount
        db.add(user_account)
        db.add(receiver_account)
        db.commit()

        user_transaction = transactions_model.Transaction(
            sender_acc_id = user_account.id,
            amount = transaction.amount,
            receiver_acc_id = receiver_account.id,
            transaction_type = TransactionType.transfer,
            description = transaction.description
        )

        sender_transaction = ledger_model.Ledger(
            user_account = user_account.id,
            amount = transaction.amount,
            ledger_type = Type.debit,
        )

        receiver_transaction = ledger_model.Ledger(
            user_account = receiver_account.id,
            amount = transaction.amount,
            ledger_type = Type.credit,
        )

        db.add(user_transaction)
        db.add(sender_transaction)
        db.add(receiver_transaction)
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
    except ImproperFlowError :
        return "Can not send money to self! Try deposit"
    except InsufficientFundsError:
        return "Your account balance is lower than sending amount"
    except Exception as e:
        return f"Oops! something went wrong {e}"

@router.post("/fund", status_code=status.HTTP_200_OK)
def fund_account(transaction: FundUser, current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    account_exists = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not account_exists:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User account not found. Create new account or leverage tag"
        )
    
    account_exists.acc_balance += transaction.amount

    db.add(account_exists)
    db.commit()

    return {
        "message": "Account funded successfully!",
        "amount": transaction.amount
    }

@router.get("/history", status_code=status.HTTP_200_OK)
def get_account_history(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    current_user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not current_user_account:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User account not found. Create a leverage tag or request for account number"
        )
    transactions_history = db.query(ledger_model.Ledger).filter(ledger_model.Ledger.user_account == current_user_account.id).all()
    return transactions_history


@router.get("/debit/history", status_code=status.HTTP_200_OK)
def get_debit_account_history(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    current_user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not current_user_account:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User account not found. Create a leverage tag or request for account number"
        )
    history = db.query(ledger_model.Ledger).filter(ledger_model.Ledger.user_account == current_user_account.id).all()
    debit_history = []
    for transaction in history:
        if transaction.ledger_type.value == "debit":
            debit_history.append(transaction)
    if len(debit_history) <= 0:
        return f"No debit history!"
    return debit_history

@router.get("/credit/history", status_code=status.HTTP_200_OK)
def get_debit_account_history(current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    current_user_account = db.query(accounts_model.Account).filter(accounts_model.Account.user_id == current_user.id).first()
    if not current_user_account:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User account not found. Create a leverage tag or request for account number"
        )
    history = db.query(ledger_model.Ledger).filter(ledger_model.Ledger.user_account == current_user_account.id).all()
    credit_history = []
    for transaction in history:
        if transaction.ledger_type.value == "credit":
            credit_history.append(transaction)
    if len(credit_history) <= 0:
        return f"No credit history!"
    return credit_history
