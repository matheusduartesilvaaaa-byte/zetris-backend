from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(customer_in: schemas.CustomerCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    c = models.Customer(**customer_in.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/", response_model=List[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(models.Customer).offset(skip).limit(limit).all()

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    c = db.query(models.Customer).get(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return c

@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, customer_in: schemas.CustomerCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    c = db.query(models.Customer).get(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for k, v in customer_in.dict().items():
        setattr(c, k, v)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    c = db.query(models.Customer).get(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(c)
    db.commit()
    return {"ok": True}
