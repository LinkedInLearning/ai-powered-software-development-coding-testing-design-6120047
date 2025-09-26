from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_current_user
from ..db.session import get_db
from ..models.user import User as UserModel
from ..schemas.user import UserOut, UserUpdate
from ..core.security import hash_password

router = APIRouter()


@router.get("/me", response_model=UserOut)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    updated = False
    if payload.email is not None:
        # Check uniqueness for email
        exists = db.query(UserModel).filter(UserModel.email == payload.email, UserModel.id != current_user.id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = payload.email
        updated = True
    if payload.password is not None:
        current_user.password_hash = hash_password(payload.password)
        updated = True

    if updated:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    return current_user
