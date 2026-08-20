from sqlalchemy.orm import Session

from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_user(db: Session, user: UserCreate):

    existing_user = user_crud.get_by_email(
        db,
        user.email
    )

    if existing_user:
        raise Exception("Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    db: Session,
    email: str,
    password: str
):

    user = user_crud.get_by_email(
        db,
        email
    )

    if not user:
        raise Exception(
            "Invalid email or password"
        )

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise Exception(
            "Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
