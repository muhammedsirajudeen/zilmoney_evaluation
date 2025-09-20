from fastapi import APIRouter,Query, Request
from fastapi.responses import JSONResponse

from models.hello import Expense, User
from operations.budget_summary import get_budget_summary
from operations.list_expenses import list_expenses
from operations.create_expense import create_expense_db
from operations.create_user import create_user
from schemas.budget import BudgetSummary
from schemas.expense import ExpenseCreate, ExpenseRead
from utils.extract_token import get_token_from_header
from utils.jwt import create_access_token, decode_access_token
router = APIRouter(prefix="/api", tags=["Hello"])
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException
from schemas.schemas import UserCreate, UserRead
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Optional
from datetime import datetime
from typing import List, Optional
from sqlalchemy import func


@router.get("/")
def say_hello(name: str = "World"):
    return JSONResponse({"message": f"Hello, {name}!"},status_code=200)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/")
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    # Optional: check if username already exists
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return JSONResponse(content={"message":"user already exists"},status_code=400)
    user=create_user(db, user)
    token=create_access_token({"username":user.username,"user_id":user.user_id})
    print("the token  is ",token)
    #hacky solution
    return JSONResponse(content={"message":"user created successfully","user":{"username":user.username,
                                                                               "user_id":user.user_id,
                                                                               "salary":user.salary},
                                                                               "token":token
                                                                               },
                                                                               status_code=201)



@router.post("/expenses/", response_model=ExpenseRead)
def create_expense(request:Request,expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Optional: validate that user exists
    # decode_access_token()
    #try to incorporate everywhere if additional time
    token=get_token_from_header(request)
    print("the token is",token)
    payload=decode_access_token(token)
    print("payload is",payload)
    user_id=payload["user_id"]
    if user_id!=expense.user_id:
        return JSONResponse({"message":"unauthorized"},status_code=401)
    user = db.query(User).filter(User.user_id == expense.user_id).first()
    if not user:
        return JSONResponse(content={"message":"user not found"},status_code=404)

    return create_expense_db(db, expense)




@router.get("/expenses/{user_id}", response_model=List[ExpenseRead])
def get_user_expenses(
    user_id: int,
    day: Optional[str] = Query(None, description="YYYY-MM-DD"),
    week: Optional[int] = Query(None, ge=1, le=53),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    #TODO: convert to check to enum values
    if category not in ["Food","Transport"]:
        return JSONResponse({"message":"category not found"},status_code=400)
    # Check user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expenses = list_expenses(db, user_id, day=day, week=week, month=month, year=year, category=category)
    return expenses



@router.get("/totals/{user_id}", response_model=BudgetSummary)
def budget_summary(user_id: int, db: Session = Depends(get_db)):
    summary = get_budget_summary(db, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="User not found")
    return summary