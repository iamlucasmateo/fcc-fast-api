from pydantic import BaseSettings

# this will be overriden by env variables
class Settings(BaseSettings):
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str


    class Config:
        env_file = ".env"



SETTINGS = Settings()

def get_settings():
    return SETTINGS