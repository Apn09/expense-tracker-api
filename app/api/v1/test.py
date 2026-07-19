from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {"users_count": count}
