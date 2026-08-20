from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.expense import Expense
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
)
from app.core.security import get_current_user
from app.crud.crud_expense import create_expense


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post(
    "/",
    response_model=ExpenseResponse
)
def register_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_expense = Expense(
        user_id=current_user.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        expense_date=expense.expense_date,
    )

    return create_expense(
        db,
        new_expense
    )
