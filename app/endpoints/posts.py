from fastapi import HTTPException, status

from app.main import app, repository
from app.repository.posts import PostRepository
from app.models import Post


@app.get('/posts/')
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
    deleted = repository.delete(id)
    if not deleted:
        raise_inexistent(id)


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