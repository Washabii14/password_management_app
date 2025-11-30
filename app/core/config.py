from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    app_port: int = 8000

    # Database
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_user: str = "pw_manager"
    postgres_password: str = "pw_manager_password"
    postgres_db: str = "pw_manager_dev"
    database_url: Optional[str] = None

    # S3 / Object storage
    s3_endpoint_url: str = "http://s3:9000"
    s3_access_key_id: str = "dev-access-key"
    s3_secret_access_key: str = "dev-secret-key"
    s3_region: str = "us-east-1"
    s3_bucket_vault_blobs: str = "pw-manager-vault-blobs-dev"

    # Security
    jwt_secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    log_level: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


