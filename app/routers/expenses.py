from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..deps import get_current_user
from ..db.session import get_db
from ..models.expense import Expense as ExpenseModel
from ..models.user import User as UserModel
from ..schemas.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate

router = APIRouter()


@router.get("/", response_model=List[ExpenseOut])
def list_expenses(
    category: Optional[str] = Query(default=None),
    from_date: Optional[date] = Query(default=None, alias="from"),
    to_date: Optional[date] = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    q = db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id)
    if category is not None:
        q = q.filter(ExpenseModel.category == category)
    if from_date is not None:
        q = q.filter(ExpenseModel.date >= from_date)
    if to_date is not None:
        q = q.filter(ExpenseModel.date <= to_date)
    return q.order_by(ExpenseModel.date.desc(), ExpenseModel.id.desc()).all()


@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    expense = ExpenseModel(**payload.model_dump(), user_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, payload: ExpenseUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(expense, k, v)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return None
