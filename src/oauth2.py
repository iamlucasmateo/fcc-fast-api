from jose import JWTError, jwt
from datetime import datetime, timedelta

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