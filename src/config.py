from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # app
    APP_NAME: str = "Awesome API"
    DEBUG: bool = True

    # redis
    REDIS_URL: str = "redis://localhost/0"

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "69208e7f89038df97ff9af4eb3e894e0e0f5515206b86fb58268f0b6b434d5d8"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


@lru_cache()
def get_settings():
    return Settings()