from fastapi import APIRouter, Depends, status, Response, HTTPException

from sqlalchemy.orm import Session

from typing import List

from ..oauth2 import get_current_user
from .. import schemas, models
from ...core.database import get_db
from ..service import Hash


router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    request.password = Hash.bcrypt(request.password)
    new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserShow])
async def user_list(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserShow)
async def retrieve_user(
    id,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found.",
        )
    return user
