from fastapi import FastAPI
from app.api.v1.expenses import router as expense_router
from app.core.config import settings
from app.db.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.user import User
# from app.models.expense import Expense   # Uncomment when this model exists

from app.api.v1.health import router as health_router
from app.api.v1.database_health import router as database_health_router
from app.api.v1.auth import router as auth_router

print("SECRET_KEY:", settings.SECRET_KEY)
print("ALGORITHM:", settings.ALGORITHM)
print("TOKEN EXPIRE:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

# Automatically create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(health_router)
app.include_router(database_health_router)
app.include_router(auth_router)
app.include_router(expense_router)

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
        "environment": settings.APP_ENV,
    }
