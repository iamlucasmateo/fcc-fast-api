from datetime import datetime, timedelta
from secrets import token_bytes

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import TokenData
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 1. SECRET KEY
# 2. Token Algorithm
# 3. Expiration time

# to get something like these, on the command line: openssl rand -hex 32
SECRET_KEY = "7282b4f00bcefcc7b56272997412fc5fcc89d015bff7c851ea5e957236fbe277"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration": expires.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # this will raise an error if token is invalid
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    
    user = db.query(User).filter(User.id == token.id).first()

    return user  
