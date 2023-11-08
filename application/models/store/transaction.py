from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (Integer, ForeignKey, Numeric)


class StoreImported(CommonModel): 
    __tablename__ = "storeimporteds"
    no = db.Column(Integer(), autoincrement=True, index=True) 
    storeimpored_detail = db.relationship("StoreImportedDetail", back_populates="storeimported")
    
class StoreImportedDetail(CommonModel): 
    __tablename__ = "storeimpored_details"
    quantity = db.Column(Integer(), default=0)
    
    product_id = db.Column(UUID(as_uuid=True), ForeignKey("products.id"))
    product = db.relationship("Product")
    
    storeimported_id = db.Column(UUID(as_uuid=True), ForeignKey("storeimporteds.id", ondelete='CASCADE'), index=True)
    storeimported = db.relationship("StoreImported", back_populates="storeimpored_detail")
    
    
    

    