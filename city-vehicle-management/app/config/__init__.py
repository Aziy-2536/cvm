# app/config/__init__.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "cWmCy5W-kvddV-U5VOipNmKGnt-bIZ8EyRgDNLI8UXo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    mysql_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()