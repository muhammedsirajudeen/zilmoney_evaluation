from sqlalchemy import func
from sqlalchemy.orm import Session

from models.hello import Expense, User

def get_budget_summary(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None

    # Total expense
    total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0.0))\
                      .filter(Expense.user_id == user_id).scalar()

    # Category-wise breakdown
    category_data = db.query(Expense.category, func.coalesce(func.sum(Expense.amount), 0.0))\
                      .filter(Expense.user_id == user_id)\
                      .group_by(Expense.category).all()
    
    category_breakdown = {category.value: total for category, total in category_data}

    return {
        "total_expense": float(total_expense),
        "total_salary": float(user.salary),
        "remaining_amount": float(user.salary - total_expense),
        "category_breakdown": category_breakdown
    }
