from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_expire_minutes: int
    jwt_algorithm: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )


settings = Settings()  # type: ignore
