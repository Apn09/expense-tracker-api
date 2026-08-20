from sqlalchemy.orm import Session

from app.models.expense import Expense


def create_expense(
    db: Session,
    expense: Expense
):
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense
