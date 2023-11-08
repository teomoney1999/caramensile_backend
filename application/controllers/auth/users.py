from ...models.authentication import *
from application.extensions import apimanager
# from ..server import app

apimanager.create_api(model=User, collection_name='users')


    




