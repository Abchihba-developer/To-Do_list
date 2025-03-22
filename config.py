from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):

    host: str = "127.0.0.1"
    port: int = 8080


class DatabaseConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    echo: bool = True
    pool_size: int = 5
    max_overflow: int = 10

    autocommit: bool = False
    autoflush: bool = False
    expire_on_commit: bool = False

    @property
    def DB_URL_ASYNCPG(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


class Settings(RunConfig):
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
