from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.core.config import settings
from app.core.security import (
    generate_password_reset_token,
    hash_reset_token,
    hash_password,
)
from app.services.email_service import send_password_reset_email


def create_password_reset_token(db: Session, email: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return

    token = generate_password_reset_token()
    token_hash = hash_reset_token(token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )

    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False,
    )

    db.add(reset_token)
    db.commit()

    reset_link = f"{settings.FRONTEND_RESET_URL}?token={token}"

    send_password_reset_email(user.email, reset_link)


def reset_password(db: Session, token: str, new_password: str):

    token_hash = hash_reset_token(token)

    reset_token = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == token_hash)
        .first()
    )

    if not reset_token:
        return False, "Invalid reset token"

    if reset_token.used:
        return False, "Token already used"

    if reset_token.expires_at < datetime.now(timezone.utc):
        return False, "Token expired"

    user = db.query(User).filter(
        User.id == reset_token.user_id
    ).first()

    if not user:
        return False, "User not found"

    user.hashed_password = hash_password(new_password)
    reset_token.used = True

    db.commit()

    return True, "Password reset successful"
