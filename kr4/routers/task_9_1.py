"""
Задание 9.1. Эндпоинты для Product, чтобы было удобно проверить миграции.
Сами миграции — в alembic/versions/, инициализация — в alembic.ini + alembic/env.py.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_models import Product, get_db
from models import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Задание 9.1 — Product (Alembic)"])


@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
