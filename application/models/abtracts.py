from ..database import db 
from ..database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (String, BigInteger, SmallInteger, ForeignKey, Numeric)

class Contact(db.Model): 
    __abstract__ = True
    phone = db.Column(String(), index=True) 
    zalo = db.Column(String(), index=True) 
    facebook = db.Column(String()) 
    facebook_name = db.Column(String(), index=True)

class BankInfo(db.Model): 
    __abstract__ = True
    bank_name = db.Column(String()) 
    bank_number = db.Column(String(), index=True)
    bank_qr_code = db.Column(String()) # qr code link 
    