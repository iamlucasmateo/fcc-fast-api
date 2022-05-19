from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import UserLogin
from src.models import User
from src.utils.tools import verify


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login/")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or password incorrect")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or password incorrect")
    
    return {"token": "example token"}
