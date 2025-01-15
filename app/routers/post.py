from .. import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import oauth2

from typing import List

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts  # Return the fetched data


@router.get("/{id}", response_model=schemas.PostResponse)
def getdatabyID(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id : {id} Data was not found"
        )
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def createPost(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user.email)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pst with id: {id} does not exist",
        )
    post.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def UpdateById(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()
    if post_updated == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} is not found ",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
