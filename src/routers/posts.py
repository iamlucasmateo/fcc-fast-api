from typing import List, Optional

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from src.schemas import PostCreate, PostResponse
from src.models import PostModel
from src.database import get_db
from src.oauth2 import get_current_user 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def read_all(
    db: Session = Depends(get_db), 
    current_user: int = Depends(get_current_user), 
    limit: int = 10, 
    skip: int = 0,
    search: Optional[str] = ""

): # using Depends makes testing easier (it's not necessary)
    # db.query returns a query
    # posts = db.query(PostModel).all() , all posts
    posts = db.query(PostModel).filter(PostModel.content.contains(search), PostModel.user_id == current_user.id).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}', response_model=PostResponse)
def read_one(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(PostModel).filter(
        PostModel.id == id, PostModel.user_id == current_user.id
    ).first()
    return post


@router.post("/", response_model=PostResponse)
def create(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # new_post = PostModel(title=post.title, content=post.content, published=post.published)
    post_data = post.dict()
    post_data.update({"user_id": current_user.id})
    new_post = PostModel(**post_data) # unpacking for shorter code
    db.add(new_post) # creates row in DB
    db.commit() # commits
    db.refresh(new_post) # retrieves results from DB
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    query = db.query(PostModel).filter(
        PostModel.id == id, PostModel.user_id == current_user.id
    )
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}", response_model=PostResponse)
def update(id: int, payload: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(PostModel).filter(
        PostModel.id == id, PostModel.user_id == current_user.id
    )
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")
    
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    post = db.refresh(post_query.first())

    return post