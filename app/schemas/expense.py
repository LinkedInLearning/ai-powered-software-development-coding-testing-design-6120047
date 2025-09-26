from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float = Field(gt=0)
    currency: str = "USD"
    category: str
    description: Optional[str] = None
    date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0)
    currency: str | None = None
    category: str | None = None
    description: str | None = None
    date: date | None = None


class ExpenseOut(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
