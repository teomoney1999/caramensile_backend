from .apimanager.api import ApiManager
from ..database import db
from .apimanager.sqlalchemy.view import CollectionApiView, InstanceApiView
apimanager = ApiManager()

def init_extensions(app):
    apimanager.init_app(app=app, db=db, view_cls=(CollectionApiView, InstanceApiView))