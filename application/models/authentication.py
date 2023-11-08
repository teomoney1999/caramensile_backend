from ..database import db 
from ..database.model import CommonModel 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (String, BigInteger, SmallInteger, ForeignKey)
from .abtracts import BankInfo, Contact

# users_roles = db.Table()
# class UsersRoles(db.Model): 
#     __tablename__ = 'users_roles' 
#     user_id = db.Column(UUID(as_uuid=True), 
#                         ForeignKey('users.id', ondelete="CASCADE"), 
#                         primary_key=True, index=True) 
#     role_id = db.Column(UUID(as_uuid=True), 
#                         ForeignKey('roles.id', ondelete="CASCADE"), 
#                         primary_key=True, index=True)

roles_user = db.Table("roles_user",
                    db.Column("user_id", UUID(as_uuid=True), 
                        ForeignKey('users.id', ondelete="CASCADE"), 
                        primary_key=True, index=True), 
                    db.Column("role_id", UUID(as_uuid=True), 
                        ForeignKey('roles.id', ondelete='CASCADE'), 
                        primary_key=True, index=True))

class User(CommonModel): 
    __tablename__ = 'users'
    email = db.Column(String(), unique=True, nullable=False, index=True) 
    password = db.Column(String(), nullable=False, index=True) 
    salt = db.Column(String(), nullable=False)
    is_login = db.Column(SmallInteger(), default=0) 
    
    # previously one-to-many Parent.children is now
    # one-to-one Parent.child
    personal_information = db.relationship("PersonalInfomation", 
                                           back_populates='user', uselist=False, 
                                           cascade="all, delete", passive_deletes=True)
    role = db.relationship("Role", 
                           secondary=roles_user, 
                           back_populates='user')
    
    # TODO use google oauth to create user and login

class Role(CommonModel): 
    __tablename__ = 'roles' 
    name = db.Column(String(), unique=True, nullable=False, index=True) 
    description = db.Column(String()) 
    user = db.relationship("User", 
                           secondary=roles_user, 
                           back_populates='role')

class PersonalInfomation(CommonModel, BankInfo, Contact): 
    __tablename__ = 'personal_informations'
    first_name = db.Column(String()) 
    last_name = db.Column(String()) 
    date_birth = db.Column(BigInteger())
    gender = db.Column(SmallInteger(), default=0) # 0: male, 1: female 
    
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"))
    # many-to-one side remains, see tip below
    user = db.relationship("User", back_populates='personal_information')
    
    

    
    
