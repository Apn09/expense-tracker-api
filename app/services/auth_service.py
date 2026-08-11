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

    # Check email already exists
    if user_crud.get_by_email(db, user.email):
        raise Exception("Email already registered")

    # Check username already exists
    if user_crud.get_by_username(db, user.username):
        raise Exception("Username already exists")

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    return user_crud.create(db, new_user)


def login_user(db: Session, email: str, password: str):

    # Find user
    user = user_crud.get_by_email(db, email)

    if not user:
        raise Exception("Invalid email or password")

    # Verify password
    if not verify_password(password, user.hashed_password):
        raise Exception("Invalid email or password")

    # Generate JWT
    access_token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
