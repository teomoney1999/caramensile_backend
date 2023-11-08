from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (String, ForeignKey, Numeric, Integer, SmallInteger, BigInteger)


class Product(CommonModel):
    __tablename__ = "products" 
    name = db.Column(String()) 
    unit = db.Column(String()) 
    price = db.Column(Integer())
    quantity_threshold = db.Column(SmallInteger(), default=0)
    # 0: inactive, 1: active
    is_active = db.Column(SmallInteger(), default=1)
    inactive_at = db.Column(BigInteger())

class Store(CommonModel): 
    __tablename__ = "stores"
    product_id = db.Column(UUID(as_uuid=True), ForeignKey("products.id"), index=True) 
    product = db.relationship("Product") 
    quantity = db.Column(Integer(), default=0) 