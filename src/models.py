from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text

from src.database import Base


class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # server_default is enforced on the DB if SQLAlchemy builds the DB