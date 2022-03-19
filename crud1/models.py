from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    edited: bool = False
    share: Optional[bool] = True