from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True