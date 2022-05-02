from fastapi import FastAPI, Response, status, HTTPException
import psycopg2

from src.utils.config import ConfigParser
from src.repository.posts import (
    InMemoryPostRepository, PostgreSQLPostRepository, PostgresPostSQLQueries
)

from src.models import Post


app = FastAPI()

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


@app.get('/posts/', status_code=status.HTTP_201_CREATED)
def read_all():
    data = repository.read_all()
    return data


@app.get('/posts/{id}')
def read_one(id: int):
    data = repository.read_one(id)
    if not data:
        raise_inexistent(id)
    return data


@app.post('/posts/')
def create(payload: Post):
    repository.create(payload)
    return payload


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    repository.delete(id)


@app.put('/posts/{id}')
def update(id: int, payload: Post):
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