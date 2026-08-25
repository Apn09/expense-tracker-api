from app.schemas.user import UserCreate, UserLogin, UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import register_user, login_user
from app.core.security import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return register_user(db, user)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        return login_user(
            db,
            user.email,
            user.password
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.get("/me")
def read_current_user(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
