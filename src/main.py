from fastapi import FastAPI

from src.models import Base
from src.database import SessionLocal, engine
from src.routers import posts, user, repository, auth


# this will create the tables is they not exist, otherwise it will use them
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(repository.router)
