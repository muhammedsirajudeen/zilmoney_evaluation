from models.hello import Expense
from schemas.expense import ExpenseCreate
from sqlalchemy.orm import Session


def create_expense_db(db: Session, expense: ExpenseCreate):
    db_expense = Expense(
        user_id=expense.user_id,
        name=expense.name,
        amount=expense.amount,
        category=expense.category
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense