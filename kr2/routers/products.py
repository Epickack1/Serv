from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from data import sample_products

router = APIRouter(tags=["Задание 3.2"])

@router.get("/products/search")
async def search_products(
    keyword: str = Query(..., description="Ключевое слово для поиска"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    limit: int = Query(10, ge=1, description="Максимум товаров в ответе"),
):
    keyword_lower = keyword.lower()
    result = [
        p for p in sample_products
        if keyword_lower in p["name"].lower()
        and (category is None or p["category"] == category)
    ]
    return result[:limit]


@router.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
