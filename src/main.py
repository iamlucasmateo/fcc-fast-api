from email.policy import HTTP
from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from sqlalchemy.orm import Session

from src.utils.config import ConfigParser
from src.repository.posts import (
    InMemoryPostRepository, PostgreSQLPostRepository, PostgresPostSQLQueries
)
from src.schemas import PostBase, PostCreate, PostResponse, UserCreate, UserResponse
from src.models import Base, PostModel, User
from src.database import SessionLocal, engine
from src.utils.tools import hash


# this will create the tables is they not exist, otherwise it will use them
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# environment
config = ConfigParser()
env = config.get_env()
selected_repository = config.get_data(paths=["REPOSITORY"])


# select repository
if selected_repository == 'POSTGRES':
    connection_data = config.get_data(paths=["DATABASE", env, "CONNECTION"])
    repository = PostgreSQLPostRepository(
        connection_data=connection_data,
        connection_handler=psycopg2,
        queries=PostgresPostSQLQueries()
    )
else:
    repository = InMemoryPostRepository()


@app.get('/posts/', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def read_all(db: Session = Depends(get_db)): # using Depends makes testing easier (it's not necessary)
    # db.query returns a query
    posts = db.query(PostModel).all()
    return posts


@app.get('/posts/{id}', response_model=PostResponse)
def read_one(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    return post


@app.post('/posts/', response_model=PostResponse)
def create(post: PostCreate, db: Session = Depends(get_db)):
    # new_post = PostModel(title=post.title, content=post.content, published=post.published)
    new_post = PostModel(**post.dict()) # unpacking for shorted code
    db.add(new_post) # creates row in DB
    db.commit() # commits
    db.refresh(new_post) # retrieves results from DB
    return new_post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    query = db.query(PostModel).filter(PostModel.id == id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    query.delete(synchronize_session=False)
    db.commit()

@app.put('/posts/{id}', response_model=PostResponse)
def update(id: int, payload: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(PostModel).filter(PostModel.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")
    
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    post = db.refresh(post_query.first())

    return post

# Users

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash the password
    user.password = hash(user.password)
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




# Using repository
@app.get('/repository/posts/', status_code=status.HTTP_200_OK)
def read_all():
    data = repository.read_all()
    return data


@app.get('/repository/posts/{id}')
def read_one(id: int):
    data = repository.read_one(id)
    if not data:
        raise_inexistent(id)
    return data


@app.post('/repository/posts/')
def create(payload: PostCreate):
    repository.create(payload)
    return payload


@app.delete('/repository/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    repository.delete(id)


@app.put('/repository/posts/{id}')
def update(id: int, payload: PostCreate):
    try:
        repository.update(id, payload)
        return payload
    except KeyError as e:
        raise_inexistent(id)

def raise_inexistent(id: int, status_code: int = status.HTTP_404_NOT_FOUND):
    raise HTTPException(
        status_code=status_code,
        detail=f"id {id} does not exist for posts"
    )