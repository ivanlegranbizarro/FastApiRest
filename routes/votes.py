from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Post, User, Vote
from db.schemas import VoteSchema
from oauth.oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_exists = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    vote_query = db.query(Vote).filter(
        Vote.post_id == vote.post_id, Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Vote already exists"
            )
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"detail": "Vote created successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
            )
        vote_query.delete()
        db.commit()
        return {"detail": "Vote deleted successfully"}
