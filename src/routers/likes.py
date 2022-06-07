from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.oauth2 import get_current_user
from src.models import UpDownVote
from src.schemas import UserResponse

router = APIRouter(
    prefix="/likes",
    tags=["Posts"]
)

@router.post("/{id}")
async def like_post(
    id: int,
    upvote: bool = True,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
):  
    vote = UpDownVote(user_id=user.id, post_id=id, upvote=upvote)
    try:
        db.add(vote) # creates row in DB
        db.commit() # commits
        db.refresh(vote) # retrieves results from DB
        return {"messsage": "like created"}
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}")
async def delete_like(
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user)
):
    pass
