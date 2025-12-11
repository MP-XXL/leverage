from fastapi import Depends, Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.database_main import get_db
from datetime import datetime
from models.users_model import User
from jose import jwt, JWTError
from auth.jwt import SECRET_KEY, ALGORITHM


security = HTTPBearer()

class JWTBearer(HTTPBearer):   #The  bearer class handles decoding by base64

    def __init__(self, auto_error: bool=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session=Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                self.raiseHTTPException("Invalid authorization scheme. expected \'Bearer\'")
            return self.verify_jwt(credentials.credentials, db)
        else:
            raiseHTTPException("message: Invalid or expired token!")
    
    def verify_jwt(self, token: str, db: Session):
        try:
            payload = self.verify_access_token(token)
            user_id = payload.get("sub")
            if user_id is None:
                return False
            
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raiseHTTPException("User does not exist!")

            return user
        except Exception as e:
            self.raiseHTTPException(f"JWT verification failed. Login session expired: {e}")
    
    def verify_access_token(self, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, ALGORITHM)
        except JWTError as e:
           raise

    def raiseHTTPException(self, e, status=status.HTTP_403_FORBIDDEN):
        raise HTTPException(
                    status_code = status,
                    detail = {
                        "message": e,
                        "timestamp": f"{datetime.now()}"
                    }
                )
    
AuthMiddleware = JWTBearer()
