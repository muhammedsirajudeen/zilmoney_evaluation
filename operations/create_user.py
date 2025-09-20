from sqlalchemy.orm import Session
from models.hello import Expense, User
from schemas.schemas import UserCreate
def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, salary=user.salary)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
