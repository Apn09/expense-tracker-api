from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
)

from app.db.database import Base


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    expense_date = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
