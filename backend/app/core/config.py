from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Dog-Eared"
    ENV: str = "dev"

    SECRET_KEY: str = "change-me-in-prod"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    ADMIN_EMAIL: str = "you@example.com"
    ADMIN_PASSWORD: str = "change-me"
    ADMIN_DISPLAY_NAME: str = "Admin"

    FRONTEND_ORIGIN: str = "http://localhost:5173"

    DATABASE_URL: str = "sqlite:///./dogeared.db"

    # Feature flags
    ALLOW_OPEN_REGISTRATION: bool = False  # future switch


settings = Settings()
