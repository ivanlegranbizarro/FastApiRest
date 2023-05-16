from typing import Optional

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi.routing import APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import get_db
from db.models import Post, Vote
from db.schemas import PostCreate, PostResponse
from oauth.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), search: Optional[str] = ""):
    posts = db.query(Post).filter(Post.title.ilike(f"%{search}%")).all()
    count_voutes_per_post = (
        db.query(Vote.post_id, func.count(Vote.post_id)).group_by(Vote.post_id).all()
    )


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: EmailStr = Depends(get_current_user),
):
    new_post = Post(**post.dict(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put(
    "/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse
)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: EmailStr = Depends(get_current_user),
):
    post_query = db.query(Post).filter(Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    if post_query.first().author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.email} is not the author of this post",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: EmailStr = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    if post.first().author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.email} is not the author of this post",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
