from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ENV: str = "staging"
    # Live practice targets so your framework runs out-of-the-box:
    BASE_URL: str = "https://www.saucedemo.com"
    API_BASE_URL: str = "https://jsonplaceholder.typicode.com"
    
    # Credentials (SauceDemo standard user)
    ADMIN_USER: str = "standard_user"
    ADMIN_PASSWORD: str = "secret_sauce"
    API_KEY: str = "reqres-free-v1"
    
    # Timeouts (in milliseconds)
    DEFAULT_TIMEOUT: int = 15000
    NAVIGATION_TIMEOUT: int = 30000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()