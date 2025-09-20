from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.hello import CategoryEnum
class ExpenseBase(BaseModel):
    user_id: int
    name: str = Field(..., example="Lunch")
    amount: float = Field(..., gt=0, example=250.50)
    category: CategoryEnum

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseRead(ExpenseBase):
    expense_id: int
    created_at: datetime

    class Config:
        orm_mode = True
