from fastapi import FastAPI, Response, status, HTTPException

from data import data
from app.models import Post

app = FastAPI()

@app.get('/posts')
async def get_all_posts():
    return data

@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    post = data.get(id, None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"{id} not found"}
    return post

@app.post('/posts', status_code=201)
async def create_post(post: Post):
    new_index = max(data.keys()) + 1
    data.update({new_index: post})
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    deleted = data.pop(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    if id not in data.keys():
        return None
    setattr(post, "edited", True)
    data.update({id: post})
    return post.dict()

