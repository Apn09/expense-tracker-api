from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.password_reset import PasswordResetToken

from app.core.security import (
    generate_password_reset_token,
    hash_password,
)

from app.core.config import settings


def create_password_reset_token(
    db: Session,
    email: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    token = generate_password_reset_token()

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )
    )

    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
        used=False,
    )

    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)

    return reset_token


def reset_password(
    db: Session,
    token: str,
    new_password: str
):

    reset_token = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == token
        )
        .first()
    )

    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    if reset_token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token already used"
        )

    now = datetime.now(timezone.utc)

    if reset_token.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token expired"
        )

    user = (
        db.query(User)
        .filter(
            User.id == reset_token.user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    user.hashed_password = hash_password(
        new_password
    )

    reset_token.used = True

    db.commit()

    return user
