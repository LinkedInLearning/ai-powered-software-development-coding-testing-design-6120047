from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..db.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    category = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    date = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="expenses")


Index("ix_expenses_user_date", Expense.user_id, Expense.date)
