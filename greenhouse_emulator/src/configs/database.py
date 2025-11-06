from os import getenv

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str | None = None

    def model_post_init(self, context=None):
        self.DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT"))
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_NAME = getenv("DB_NAME")


database_settings = DatabaseSettings(
    DB_HOST=DB_HOST,
    DB_PORT=DB_PORT,
    DB_USER=DB_USER,
    DB_PASS=DB_PASS,
    DB_NAME=DB_NAME,
)
