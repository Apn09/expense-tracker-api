from datetime import datetime

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str | None = None
    expense_date: datetime


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    description: str | None
    expense_date: datetime

    class Config:
        from_attributes = True
