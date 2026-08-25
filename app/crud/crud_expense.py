from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.expense import Expense


class CRUDExpense(CRUDBase):

    def __init__(self):
        super().__init__(Expense)

    def get_user_expenses(
        self,
        db: Session,
        user_id: int
    ):
        return (
            db.query(Expense)
            .filter(
                Expense.user_id == user_id
            )
            .all()
        )

    def get_user_expense(
        self,
        db: Session,
        expense_id: int,
        user_id: int
    ):
        return (
            db.query(Expense)
            .filter(
                Expense.id == expense_id,
                Expense.user_id == user_id
            )
            .first()
        )

    def update_expense(
        self,
        db: Session,
        expense: Expense,
        update_data: dict
    ):
        for field, value in update_data.items():
            setattr(expense, field, value)

        db.commit()
        db.refresh(expense)

        return expense

    def delete_expense(
        self,
        db: Session,
        expense: Expense
    ):
        db.delete(expense)
        db.commit()


expense_crud = CRUDExpense()
