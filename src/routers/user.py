from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from src.schemas import UserResponse, UserCreate
from src.models import User
from src.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Users

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash the password
    user.password = hash(user.password)
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user