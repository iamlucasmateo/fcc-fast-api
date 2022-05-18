from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.config import ConfigParser

conn_data = ConfigParser().get_data(["DATABASE", "DEV", "CONNECTION"])

SQLALCHEMY_DATABASE_URL = f"postgresql://{conn_data['user']}:{conn_data['password']}@{conn_data['host']}/{conn_data['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base model
Base = declarative_base()