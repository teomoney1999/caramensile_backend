from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (String, BigInteger, Integer, SmallInteger, ForeignKey, Numeric, DECIMAL)

class Delivery(CommonModel): 
    __tablename__ = "deliveries" 
    destination = db.Column(String()) 
    distance = db.Column(DECIMAL) 
    # RESPONSE TIME
    # stared_at = db.Column(BigInteger()) 
    started_at = db.Column(BigInteger()) 
    ended_at = db.Column(BigInteger()) 
    
    # FEES
    fee_customer_paid = db.Column(DECIMAL)
    fee_company_paid = db.Column(DECIMAL) 
    total_fee = db.Column(DECIMAL)
    
    order = db.relationship("Order", back_populates="delivery") 
    order_id = db.Column(UUID(as_uuid=True), ForeignKey("orders.id"), index=True)
    
    
class Order(CommonModel): 
    __tablename__ = "orders"
    no = db.Column(Integer(), autoincrement=True, index=True) 
    # STATUS
    payment_status = db.Column(SmallInteger(), index=True, default=0)   # 0: no paid, 1: paid
    delivery_status = db.Column(SmallInteger(), index=True, default=0)  # 0: received order, 1: ready for delivery 2: on the road, 3: shipped
    status = db.Column(SmallInteger(), index=True, default=0)  # 0: received, 1: ready, 2: shipping, 3: successful, 4: failed
    
    # WHEN FINISHED ORDER
    completed_at = db.Column(BigInteger()) 
    paid_at = db.Column(BigInteger()) 
    shipped_at = db.Column(BigInteger()) 
    
    # DELIVERY
    delivery_fee = db.Column(DECIMAL)
    delivery_attempt = db.Column(SmallInteger(), default=0)
    
    # PAYMENT
    payment_method = db.Column(SmallInteger(), default=0)   # 0: cash payment, 1: bank payment
    order_amount = db.Column(DECIMAL) 
    total_amount = db.Column(DECIMAL) 
    
    customer_id = db.Column(UUID(as_uuid=True), ForeignKey("customers.id"), index=True)
    customer = db.relationship("Customer", back_populates="order")
    
    order_detail = db.relationship("OrderDetail", back_populates="order")
    
    delivery = db.relationship("Delivery", back_populates="order")
    

class OrderDetail(CommonModel): 
    __tablename__ = "order_details"
    quantity = db.Column(SmallInteger(), default=0) 
    product_name = db.Column(String()) 
    price = db.Column(DECIMAL, default=0)  
    
    # TODO calculate "amount" if not calculate from FE (Event) 
    amount = db.Column(DECIMAL, default=0)
    
    order = db.relationship("Order", back_populates="order_detail") 
    order_id = db.Column(UUID(as_uuid=True), ForeignKey("orders.id"), index=True)
    
    product_id = db.Column(UUID(as_uuid=True), ForeignKey("products.id"))
    product = db.relationship("Product")
    

    
    
    
    
     
        
    
    
    
    
    
    
    
    