from flask_sqlalchemy import SQLAlchemy
# from .model import CommonModel
# from .test import Customer

db = SQLAlchemy()

def init_database(app): 
    db.init_app(app)