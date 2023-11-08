from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (String, BigInteger, SmallInteger, ForeignKey, Numeric)
from application.models.abtracts import Contact, BankInfo

    

class Brand(CommonModel, Contact): 
    __tablename__ = "brands"
    name = db.Column(String(), nullable=False, index=True) 
    owner_name = db.Column(String())
    # 0: Cửa hàng chè, ăn vặt, 1: Nhà hàng Buffet, 2: Nhà hàng truyền thống
    business_type = db.Column(SmallInteger(), default=0) 
    
class Customer(CommonModel, Contact, BankInfo): 
    __tablename__ = "customers"
    name = db.Column(String(), nullable=False) 
    address = db.Column(String()) 
    last_buy_date = db.Column(BigInteger())
    
    brand = db.relationship("Brand")
    brand_id = db.Column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=True)
    
    order = db.relationship("Order", back_populates="customer")

    
     
        
    
    
    
    
    
    
    
    