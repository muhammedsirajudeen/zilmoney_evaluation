from pydantic import BaseModel
from typing import Dict

class BudgetSummary(BaseModel):
    total_expense: float
    total_salary: float
    remaining_amount: float
    category_breakdown: Dict[str, float]
