from app.core.config import settings

print("SECRET_KEY:", settings.SECRET_KEY)
print("ALGORITHM:", settings.ALGORITHM)
print("TOKEN EXPIRE:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
from fastapi import FastAPI
from app.core.config import settings
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Expense Tracker API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/config")
def config():
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV
    }
