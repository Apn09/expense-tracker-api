
from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.database_health import router as database_health_router

print("SECRET_KEY:", settings.SECRET_KEY)
print("ALGORITHM:", settings.ALGORITHM)
print("TOKEN EXPIRE:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
from fastapi import FastAPI
from app.core.config import settings
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)
app.include_router(health_router)
app.include_router(database_health_router)

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
