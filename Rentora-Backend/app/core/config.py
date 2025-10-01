from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    DATABASE_URL: str = config("DATABASE_URL")
    APP_NAME: str = "Rentora"
    API_VERSION: str = "1.0.0"
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()