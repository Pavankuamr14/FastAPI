from .. import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from .. import oauth2
from typing import Optional

from typing import List

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    posts = [
        {
            **schemas.PostResponse.from_orm(
                post
            ).dict(),  # Convert to Pydantic model first
            "votes": votes,
            "owner": post.owner,
        }
        for post, votes in results
    ]
    return posts


# @router.get("/", response_model=List[schemas.PostOut])
# def get_posts(
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
#     limit: int = 10,
#     skip: int = 0,
#     search: Optional[str] = "",
# ):
#     posts = (
#         db.query(models.Post)
#         .filter(models.Post.title.contains(search))
#         .limit(limit)
#         .offset(skip)
#         .all()
#     )  # this is for getting all post
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     # BY this your can only see your own post that you have created rather than others post. It's just like Note taking application.
#     result = (
#             db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
#             .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
#             .group_by(models.Post.id)
#             .all()
#         )
#     return result


# return posts  # Return the fetched data


@router.get("/{id}", response_model=schemas.PostOut)
def getdatabyID(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    results = (  # renamed for consistency with get_posts
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not results:  # check if results is None or empty
        raise HTTPException(
            status_code=404, detail=f"post with id : {id} Data was not found"
        )

    post, votes = results  # unpack the tuple
    post_dict = schemas.PostResponse.from_orm(
        post
    ).dict()  # convert to postResponse object first
    post_dict["votes"] = votes  # manually add votes
    return post_dict  # (post_dict)


# @router.get("/{id}", response_model=schemas.PostOut)
# def getdatabyID(
#     id: int,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     # post = db.query(models.Post).filter(models.Post.id == id).first()
#     post = (
#         db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
#         .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
#         .group_by(models.Post.id)
#         .filter(models.Post.id == id)
#         .first()
#     )
#     if not post:
#         raise HTTPException(
#             status_code=404, detail=f"post with id : {id} Data was not found"
#         )
#     return post
# if post.owner_id != current_user.id:
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="not authorized to perform requested action",
#     )
# BY this your can only see your own post that you have created rather than others post. It's just like Note taking application.


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def createPost(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())

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

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pst with id: {id} does not exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def UpdateById(
    id: int,
    updated_post_data: schemas.PostCreate,  # Renamed for clarity
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()  # Renamed for clarity
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} is not found ",
        )
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    post_query.update(
        updated_post_data.dict(), synchronize_session=False
    )  # Use updated_post_data here
    db.commit()
    return post_query.first()


# @router.put("/{id}", response_model=schemas.PostResponse)
# def UpdateById(
#     id: int,
#     post: schemas.PostCreate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with {id} is not found ",
#         )
#     if post.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to perform request action",
#         )
#     post_query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()
