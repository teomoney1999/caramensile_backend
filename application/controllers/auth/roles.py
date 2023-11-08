from flask import jsonify
from ...database import db
# from ...helpers import to_dict, get_columns, add_info_into_obj, resp
from ...models.authentication import *
from application.extensions import apimanager

apimanager.create_api(model=Role, collection_name='roles')
