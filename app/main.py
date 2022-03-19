from multiprocessing.dummy import connection
from fastapi import FastAPI
import psycopg2

from app.utils.config import ConfigParser
from app.repository.posts import (
    InMemoryPostRepository, PostgreSQLPostRepository, PostgresPostSQLQueries
)


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