from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.enums import ExpenseCategory
from app.db.database import get_db
from app.models.user import User

from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    ExpenseSummaryResponse,
)

from app.services.expense_service import (
    create_expense,
    get_user_expenses,
    update_expense,
    delete_expense,
)

from app.services.expense_summary_service import (
    get_expense_summary,
)


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
    current_user: User = Depends(get_current_user),
):

    return create_expense(
        db=db,
        user_id=current_user.id,
        expense=expense
    )


@router.get(
    "/",
    response_model=list[ExpenseResponse]
)
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_user_expenses(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/summary",
    response_model=ExpenseSummaryResponse
)
def expense_summary(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    category: ExpenseCategory | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    today = datetime.now()

    # Default: current month
    if start_date is None:
        start_date = today.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    # Default: today
    if end_date is None:
        end_date = today

    # Validate date range
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be after end date"
        )

    return get_expense_summary(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        category=category
    )


@router.patch(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense_api(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    expense = update_expense(
        db=db,
        expense_id=expense_id,
        user_id=current_user.id,
        expense_data=expense_data
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense


@router.delete(
    "/{expense_id}"
)
def delete_expense_api(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    deleted = delete_expense(
        db=db,
        expense_id=expense_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted Sucessfully"
    }
