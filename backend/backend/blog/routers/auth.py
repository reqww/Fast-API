from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ...core.database import get_db
from .. import models
from ..service import Hash
from ..token import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.name == request.username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": user.name})

    return {"access_token": access_token, "token_type": "bearer"}
