from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote

base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
)


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


    model_config = base_config

    @property
    def POSTGRES_URL(self) -> str:
        user = quote(self.POSTGRES_USER,safe="")
        pwd = quote(self.POSTGRES_PASSWORD,safe="")
        return f"postgresql+asyncpg://{user}:{pwd}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = base_config

db_settings = DatabaseSettings()
security_settings = SecuritySettings()
