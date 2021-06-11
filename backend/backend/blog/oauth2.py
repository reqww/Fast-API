from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from . import models
from .token import verify_token
from ..core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user():
    pass


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, credentials_exception)
    user = (
        db.query(models.User)
        .filter(models.User.name == token_data.username)
        .first()
    )

    if not user:
        raise credentials_exception

    return user
