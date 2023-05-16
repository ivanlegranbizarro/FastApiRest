from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from db.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = datetime.utcnow() + timedelta(
        minutes=int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": access_token_expires})
    encoded_jwt = jwt.encode(
        to_encode, config("JWT_SECRET"), algorithm=config("ALGORITHM")
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, config("JWT_SECRET"), algorithms=[config("ALGORITHM")]
        )
        user_email = payload.get("user_email")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(user_email=user_email)
    except jwt.JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.email == token.user_email).first()

    return user
