from ...database import db 
from ...database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (Integer, String, ForeignKey, Numeric, SmallInteger)
from ..abtracts import Contact


class Warehouse(CommonModel): 
    __tablename__ = "warehouses" 
    ingredient_id = db.Column(UUID(as_uuid=True), ForeignKey("ingredients.id")) 
    ingredient = db.relationship("Ingredient")
    
    quantity = db.Column(SmallInteger(), default=0)

class Ingredient(CommonModel): 
    __tablename__ = "ingredients" 
    name = db.Column(String())
    unit = db.Column(String())
    
class Supplier(CommonModel, Contact): 
    __tablename__ = "suppliers" 
    name = db.Column(String())
    address = db.Column(String()) 

