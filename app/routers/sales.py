from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.post("/", response_model=schemas.SaleOut)
def create_sale(sale_in: schemas.SaleCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    total = 0.0
    items = []
    for it in sale_in.items:
        product = db.query(models.Product).get(it.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {it.product_id} não encontrado")
        if product.stock < it.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {product.name}")
        unit_price = product.price
        total += unit_price * it.quantity
        items.append({"product": product, "quantity": it.quantity, "unit_price": unit_price})
    sale = models.Sale(customer_id=sale_in.customer_id, total=total)
    db.add(sale)
    db.flush()
    for it in items:
        si = models.SaleItem(sale_id=sale.id, product_id=it["product"].id, quantity=it["quantity"], unit_price=it["unit_price"])
        db.add(si)
        it["product"].stock -= it["quantity"]
        db.add(it["product"])
    db.commit()
    db.refresh(sale)
    return sale

@router.get("/", response_model=List[schemas.SaleOut])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(models.Sale).offset(skip).limit(limit).all()

@router.get("/{sale_id}", response_model=schemas.SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    s = db.query(models.Sale).get(sale_id)
    if not s:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return s
