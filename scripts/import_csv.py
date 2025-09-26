import csv
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.expense import Expense


def get_or_create_user(db: Session, username: str, email: Optional[str] = None) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    user = User(username=username, email=email or f"{username}@example.com", password_hash="")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def import_expenses(csv_path: str, username: str) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = get_or_create_user(db, username)
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row.get("amount", 0))
                currency = row.get("currency", "USD")
                category = row.get("category") or "Uncategorized"
                description = row.get("description") or None
                date_str = row.get("date")
                date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.utcnow().date()
                expense = Expense(
                    amount=amount,
                    currency=currency,
                    category=category,
                    description=description,
                    date=date,
                    user_id=user.id,
                )
                db.add(expense)
        db.commit()
        print("Import completed")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import expenses from CSV")
    parser.add_argument("csv_path", help="Path to CSV file with columns: amount,currency,category,description,date")
    parser.add_argument("username", help="Username to assign expenses to")

    args = parser.parse_args()
    import_expenses(args.csv_path, args.username)
