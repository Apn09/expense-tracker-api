from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Expense Tracker API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str
    REDIS_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
