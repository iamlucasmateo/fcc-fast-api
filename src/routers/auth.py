from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import UserLogin
from src.models import User
from src.utils.tools import verify
from src import oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login/")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),  
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm returns a username and password, but it can be matched
    # to whatever you need in the database
    # The OAuth2 Depdendency ensures the data is sent as form-data (not request body) 
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    # Verify user against DB (hashed password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or password incorrect")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or password incorrect")

    # Create token; it can have whatever data the app needs
    token_data = { "user_id": user.id }
    access_token = oauth2.create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
