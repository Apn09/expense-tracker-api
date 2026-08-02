from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.redis import redis_client

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():

    db_status = "UP"
    redis_status = "UP"

    # Database Health Check
    try:
        db: Session = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "DOWN"
    finally:
        db.close()

    # Redis Health Check
    try:
        redis_client.ping()
    except Exception:
        redis_status = "DOWN"

    return {
        "application": "Expense Tracker API",
        "status": "UP",
        "database": db_status,
        "redis": redis_status
    }
