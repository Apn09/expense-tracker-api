from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.expense import Expense


class CRUDExpense(CRUDBase):

    def __init__(self):
        super().__init__(Expense)

    def get_by_user(self, db: Session, user_id: int):
        return db.query(Expense).filter(
            Expense.user_id == user_id
        ).all()


expense_crud = CRUDExpense()
