from datetime import date

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.core.enums import ExpenseCategory


def get_expense_summary(
    db: Session,
    user_id: int,
    start_date: date,
    end_date: date,
    category: ExpenseCategory | None = None
):
    # First, get only this user's expenses
    query = db.query(Expense).filter(
        Expense.user_id == user_id
    )

    # Apply the date filter
    query = query.filter(
        Expense.expense_date >= start_date,
        Expense.expense_date <= end_date
    )

    # If category was provided, apply category filter
    if category:
        query = query.filter(
            Expense.category == category
        )

    expenses = query.all()

    # Calculate total amount
    total_expense = sum(
        expense.amount for expense in expenses
    )

    # Count number of expenses
    expense_count = len(expenses)

    # Calculate category-wise amount
    category_summary = {}

    for expense in expenses:

        category_name = expense.category.value

        if category_name not in category_summary:
            category_summary[category_name] = Decimal("0")

        category_summary[category_name] += expense.amount

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_expense": total_expense,
        "expense_count": expense_count,
        "category_summary": category_summary
    }
