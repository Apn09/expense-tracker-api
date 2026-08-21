from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

from app.core.enums import ExpenseCategory


class ExpenseCreate(BaseModel):

    amount: Decimal= Field(gt=0)
    category: ExpenseCategory
    description: str | None = None
    expense_date: datetime

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value):

        if isinstance(value, str):
            value = value.strip().lower()

            for category in ExpenseCategory:
                if category.value.lower() == value:
                    return category

        raise ValueError(
            "Invalid expense category"
        )


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
