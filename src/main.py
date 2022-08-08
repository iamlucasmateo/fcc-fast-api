from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import Base
from src.database import SessionLocal, engine
from src.routers import posts, user, repository, auth, likes


# this will create the tables is they not exist, otherwise it will use them
# Base.metadata.create_all(bind=engine)

# with Alembic it's not needed anymore

app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)
app.include_router(repository.router)

@app.get("/status")
def get_status():
    return {"message": "server running"}

@app.get("/")
def hello_world():
    return {"hello": "world"}

# explicit origins declarations
origins = [
    "http://localhost",
    "https://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)