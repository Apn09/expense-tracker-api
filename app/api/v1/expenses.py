from datetime import date, datetime, time, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=201,
)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = Expense(
        user_id=user.id,
        amount=data.amount,
        category=data.category,
        description=data.description,
        expense_date=data.expense_date,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get(
    "",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(Expense)
        .filter(
            Expense.user_id == user.id
        )
        .order_by(
            Expense.expense_date.desc()
        )
        .all()
    )


@router.get("/summary")
def summarize_expenses(
    start_date: date | None = None,
    end_date: date | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()

    # No dates provided → current month
    if start_date is None and end_date is None:
        start_date = today.replace(day=1)
        end_date = today

    # Validate date range
    if (
        start_date
        and end_date
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )

    # Get only the logged-in user's expenses
    query = (
        db.query(Expense)
        .filter(
            Expense.user_id == user.id
        )
    )

    # Start of requested date
    if start_date:
        start_datetime = datetime.combine(
            start_date,
            time.min,
        )

        query = query.filter(
            Expense.expense_date >= start_datetime
        )

    # Include the complete end date
    if end_date:
        next_day = end_date + timedelta(days=1)

        end_datetime = datetime.combine(
            next_day,
            time.min,
        )

        query = query.filter(
            Expense.expense_date < end_datetime
        )

    # Optional category filter
    if category:
        query = query.filter(
            Expense.category == category
        )

    # Get matching expenses
    expenses = query.all()

    # Calculate total expense
    total = sum(
        (
            expense.amount
            for expense in expenses
        ),
        Decimal("0.00"),
    )

    # Calculate category-wise totals
    category_summary = {}

    for expense in expenses:

        category_summary[expense.category] = (
            category_summary.get(
                expense.category,
                Decimal("0.00"),
            )
            + expense.amount
        )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_expense": total,
        "expense_count": len(expenses),
        "category_summary": category_summary,
    }


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id,
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id,
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    for field, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            expense,
            field,
            value,
        )

    db.commit()
    db.refresh(expense)

    return expense


@router.delete(
    "/{expense_id}",
    status_code=204,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id,
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    db.delete(expense)
    db.commit()
