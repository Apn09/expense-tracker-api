from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)

from app.db.database import Base


class PasswordResetToken(Base):

    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    token = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    used = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
