from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.models.product import *
from backend.app.crud.product import ProductCRUD
from backend.app.database import get_db

router = APIRouter()

@router.post("/{user_id}", response_model=str)
async def create_product(user_id: str, product: ProductCreate, db=Depends(get_db)) -> str:
    print(ProductCreate.dict)
    product_crud = ProductCRUD(db)
    product_id = await product_crud.create_product(user_id, product)
    return product_id

@router.get("/search/{user_id}", response_model=List[Product])
async def search_products(user_id: str, name: str, db=Depends(get_db)) -> List[Product]:
    product_crud = ProductCRUD(db)
    return await product_crud.get_products_by_name(user_id, name)
@router.get("/{user_id}", response_model=Product)
async def get_product(user_id: str, product_id: str, db=Depends(get_db)) -> Product:
    product_crud = ProductCRUD(db)
    print(product_id)
    product = await product_crud.get_product_by_id(user_id, product_id)
    if product is None:
        return None
        #raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{user_id}")
async def update_product(user_id: str, product: ProductUpdate, db=Depends(get_db)):
    product_crud = ProductCRUD(db)
    success = await product_crud.update_product(user_id, product)
    if not success:
        return None
        #raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{user_id}")
async def delete_product(user_id: str, product_id: str, db=Depends(get_db)):
    product_crud = ProductCRUD(db)
    success = await product_crud.delete_product(user_id, product_id)
    if not success:
        return None
        #raise HTTPException(status_code=404, detail="Product not found")
