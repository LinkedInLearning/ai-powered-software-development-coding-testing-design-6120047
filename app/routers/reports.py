from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..deps import get_current_user
from ..db.session import get_db
from ..models.expense import Expense as ExpenseModel
from ..models.user import User as UserModel
from ..schemas.report import SummaryReport

router = APIRouter()


@router.get("/summary", response_model=SummaryReport)
def summary(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    total = db.query(func.coalesce(func.sum(ExpenseModel.amount), 0)).filter(ExpenseModel.user_id == current_user.id).scalar()
    rows = (
        db.query(ExpenseModel.category, func.coalesce(func.sum(ExpenseModel.amount), 0))
        .filter(ExpenseModel.user_id == current_user.id)
        .group_by(ExpenseModel.category)
        .all()
    )
    by_category: Dict[str, float] = {name: value for name, value in rows}
    return SummaryReport(total=float(total or 0), by_category=by_category)
