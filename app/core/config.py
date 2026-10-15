from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SERVICE_NAME: str = "Inventory"
    ENV: str = "local"
    AUTH_TYPE: str = "jwt_rbac"  # none | api_key | jwt_rbac
    CACHE_ENABLED: bool = True
    QUEUE_ENABLED: bool = True
    DATABASE: str = "postgresql"  # none | postgresql | mongodb
    JWT_SECRET: str = "5a1da2b620c99ce9b990b69a9c353ca5bf7bc4771e01e3678a3e129e31993365"
    JWT_ALGORITHM: str = "HS256"
    # مقدار پیش‌فرض برای توسعهٔ لوکال؛ در .env (که در .gitignore است) override کنید.
    DATABASE_URL: str = "postgresql+asyncpg://forge:change-me@localhost:5432/inventory_backendd"


settings = Settings()
