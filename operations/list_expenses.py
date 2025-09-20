
from datetime import datetime
from typing import Optional

from sqlalchemy import extract
from models.hello import Expense
from sqlalchemy.orm import Session


def list_expenses(
    db: Session,
    user_id: int,
    day: Optional[str] = None,      # format YYYY-MM-DD
    week: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    category: Optional[str] = None
):
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if day:
        date_obj = datetime.strptime(day, "%Y-%m-%d")
        query = query.filter(
            extract("year", Expense.created_at) == date_obj.year,
            extract("month", Expense.created_at) == date_obj.month,
            extract("day", Expense.created_at) == date_obj.day
        )

    if week and year:
        query = query.filter(
            extract("isodow", Expense.created_at) >= 1  # optional, ensure ISO week
        )
        query = query.filter(
            extract("week", Expense.created_at) == week,
            extract("year", Expense.created_at) == year
        )

    if month and year:
        query = query.filter(
            extract("month", Expense.created_at) == month,
            extract("year", Expense.created_at) == year
        )

    if category:
        query = query.filter(Expense.category == category)

    return query.order_by(Expense.created_at.desc()).all()
