from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String

from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Expense details
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    # Date when the expense occurred
    expense_date = Column(Date, nullable=False)

    # Record creation timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
