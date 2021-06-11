from fastapi import APIRouter, Depends, status, Response, HTTPException

from sqlalchemy.orm import Session

from typing import List

from .. import schemas, models
from ..oauth2 import get_current_user
from ...core.database import get_db


router = APIRouter(prefix="/api/blog", tags=["blogs"])


@router.get("/", response_model=List[schemas.BlogShow])
async def blogs(
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(get_current_user),
):
    blogs = db.query(models.Blog).all()
    print(blogs)
    return blogs


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BlogShow,
)
async def create(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    data = request.dict()
    data["user_id"] = user.id
    new_blog = models.Blog(**data)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}", response_model=schemas.BlogShow)
async def retrieve(
    id,
    response: Response,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"blog with id {id} not found."}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found.",
        )
    return blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found.",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update(
    id,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found.",
        )
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return blog.first()
