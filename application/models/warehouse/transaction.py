from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (Integer, String, ForeignKey, Numeric, SmallInteger, DECIMAL)


class GoodReceipt(CommonModel): 
    __tablename__ = "goodreceipts"
    no = db.Column(Integer(), autoincrement=True, index=True) 
    total_amount = db.Column(DECIMAL, default=0)
    payment_status = db.Column(SmallInteger(), default=0)   # 0: not paid, 1: paid
    
    supplier_id = db.Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), index=True)
    supplier = db.relationship("Supplier")
    
    goodreceipt_detail = db.relationship("GoodReceiptDetail", back_populates="goodreceipt")

class GoodReceiptDetail(CommonModel): 
    __tablename__ = "goodreceipt_details" 
    quantity = db.Column(SmallInteger(), default=0)
    
    ingredient_id = db.Column(UUID(as_uuid=True), ForeignKey("ingredients.id"), index=True)
    ingredient = db.relationship("Ingredient")
    
    goodreceipt_id = db.Column(UUID(as_uuid=True), ForeignKey("goodreceipts.id", ondelete="CASCADE"), index=True)
    goodreceipt = db.relationship("GoodReceipt", back_populates="goodreceipt_detail")

class GoodIssued(CommonModel): 
    __tablename__ = "goodissueds"
    no = db.Column(Integer(), autoincrement=True, index=True) 
    
    goodissued_detail = db.relationship("GoodIssuedDetail", back_populates="goodissued")
    
     
class GoodIssuedDetail(CommonModel): 
    __tablename__ = "goodissued_details" 
    
    ingredient_id = db.Column(UUID(as_uuid=True), ForeignKey("ingredients.id"), index=True)
    ingredient = db.relationship("Ingredient")
    
    quantity = db.Column(SmallInteger(), default=0)
    
    goodissued_id = db.Column(UUID(as_uuid=True), ForeignKey("goodissueds.id", ondelete="CASCADE"), index=True)
    goodissued = db.relationship("GoodIssued", back_populates="goodissued_detail")