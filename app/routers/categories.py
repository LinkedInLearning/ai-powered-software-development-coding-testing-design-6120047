from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_current_user
from ..db.session import get_db
from ..models.category import Category as CategoryModel
from ..models.user import User as UserModel
from ..schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter()

# Default categories could be seeded via migrations; here we just expose CRUD for user categories


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return (
        db.query(CategoryModel)
        .filter((CategoryModel.user_id == None) | (CategoryModel.user_id == current_user.id))  # noqa: E711
        .order_by(CategoryModel.name.asc())
        .all()
    )


@router.post("/", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    exists = (
        db.query(CategoryModel)
        .filter(CategoryModel.name == payload.name, CategoryModel.user_id == current_user.id)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = CategoryModel(name=payload.name, user_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    data = payload.name
    if data is not None:
        dup = (
            db.query(CategoryModel)
            .filter(CategoryModel.name == data, CategoryModel.user_id == current_user.id, CategoryModel.id != category.id)
            .first()
        )
        if dup:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        category.name = data
        db.add(category)
        db.commit()
        db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return None
