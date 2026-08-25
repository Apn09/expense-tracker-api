from sqlalchemy.orm import Session

from app.crud.crud_expense import expense_crud
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense


def create_expense(
    db: Session,
    user_id: int,
    expense: ExpenseCreate
):

    new_expense = Expense(
        user_id=user_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        expense_date=expense.expense_date,
    )

    return expense_crud.create(
        db,
        new_expense
    )


def get_user_expenses(
    db: Session,
    user_id: int
):

    return expense_crud.get_user_expenses(
        db,
        user_id
    )


def update_expense(
    db: Session,
    expense_id: int,
    user_id: int,
    expense_data: ExpenseUpdate
):

    expense = expense_crud.get_user_expense(
        db,
        expense_id,
        user_id
    )

    if expense is None:
        return None

    update_data = expense_data.model_dump(
        exclude_unset=True
    )

    return expense_crud.update_expense(
        db,
        expense,
        update_data
    )


def delete_expense(
    db: Session,
    expense_id: int,
    user_id: int
):

    expense = expense_crud.get_user_expense(
        db,
        expense_id,
        user_id
    )

    if expense is None:
        return False

    expense_crud.delete_expense(
        db,
        expense
    )

    return True
