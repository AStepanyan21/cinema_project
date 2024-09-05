import os
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_NAME: str = os.environ.get("DB_NAME", "your_database")
    DB_USER: str = os.environ.get("DB_USER", "your_user")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "your_password")
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: str = os.environ.get("DB_PORT", "5432")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_url_sync(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AppSettings(BaseSettings):
    HOST: str = os.environ.get("HOST", "127.0.0.1")
    PORT: int = int(os.environ.get("PORT", "8000"))
    RELOAD: bool = bool(os.environ.get("RELOAD_SERVER", "1"))
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "your_secret_key")
    DOMAIN: str = os.environ.get("DOMAIN", "127.0.0.1:8000")


class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    app_settings: AppSettings = AppSettings()


settings = Settings()
