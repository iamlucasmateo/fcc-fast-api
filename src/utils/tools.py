from passlib.context import CryptContext

# hashing algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_context.hash(password)