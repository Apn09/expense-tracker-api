from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.core.enums import ExpenseCategory


class ExpenseCreate(BaseModel):

    amount: Decimal = Field(gt=0)

    category: ExpenseCategory

    description: str | None = None

    expense_date: datetime


class ExpenseUpdate(BaseModel):

    amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    category: ExpenseCategory | None = None

    description: str | None = None

    expense_date: datetime | None = None


class ExpenseResponse(BaseModel):

    id: int
    user_id: int
    amount: Decimal
    category: ExpenseCategory
    description: str | None
    expense_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
