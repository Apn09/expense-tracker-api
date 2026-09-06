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

# Password reset settings
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15
    FRONTEND_RESET_URL: str = "http://localhost:3000/reset-password"

    # Email settings
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    class Config:
        env_file = ".env"
        extra = "ignore"
   
settings = Settings()
