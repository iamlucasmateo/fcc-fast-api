from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.oauth2 import get_current_user
from src.models import UpDownVote
from src.schemas import UserResponse

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
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
        updown = "up" if upvote else "down"
        return {"messsage": f"created {updown}vote"}
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}")
async def delete_like(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    query = db.query(UpDownVote).filter(
        UpDownVote.post_id == id, UpDownVote.user_id == current_user.id
    )
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no vote for this post")
    
    query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Post {id} successfully deleted"}


@router.get("/")
async def get_all_user_votes(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # paginate this
    query = db.query(UpDownVote).filter(UpDownVote.user_id == current_user.id)
    return query.all()


@router.get("/{post_id}")
async def get_all_user_votes(
    post_id: int,
    db: Session = Depends(get_db)
):  
    # alternative: use COUNT
    query = db.query(UpDownVote).filter(UpDownVote.post_id == post_id)
    results = query.all()
    upvotes = len([r for r in results if r.upvote])
    downvotes = len([r for r in results if not r.upvote])
    return {"upvotes": upvotes, "downvotes": downvotes}


