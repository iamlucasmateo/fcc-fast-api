from fastapi import status, HTTPException, APIRouter
import psycopg2

from src.utils.config import ConfigParser
from src.repository.posts import (
    InMemoryPostRepository, PostgreSQLPostRepository, PostgresPostSQLQueries
)
from src.schemas import PostCreate

# This was done before the Foreign Key restriction on the Post table

router = APIRouter(
    prefix="/repository/posts",
    tags=["Repository"]
)

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


# Using repository
@router.get("/", status_code=status.HTTP_200_OK)
def read_all():
    data = repository.read_all()
    return data


@router.get("/{id}")
def read_one(id: int):
    data = repository.read_one(id)
    if not data:
        raise_inexistent(id)
    return data


@router.post("/")
def create(payload: PostCreate):
    repository.create(payload)
    return payload


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    repository.delete(id)


@router.put("/{id}")
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