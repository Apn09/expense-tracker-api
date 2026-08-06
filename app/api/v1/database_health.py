from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import SessionLocal

router = APIRouter(
    prefix="/health/database",
    tags=["Database Health"],
)


@router.get("/")
def database_health():

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))

        return {
            "database": "UP",
            "message": "Database connection successful"
        }

    except Exception as e:
        return {
            "database": "DOWN",
            "message": str(e)
        }

    finally:
        db.close()
