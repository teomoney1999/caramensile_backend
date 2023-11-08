# from flask import jsonify, Blueprint, Response
# from flask_restful import Resource, Api, reqparse
# from ..database import db
# from ..helpers import to_dict, add_info_into_obj, resp, count, get_columns, get_field_type, test
# from ..models.authentication import *
# from ..extensions.api import REQUEST_EXCLUDE_FIELDS, COMMON_KEY
    


# url_prefix = '/api/v1/'
# collection_name = "roles"
# model = Role
# columns = get_columns(model) 

# cols = []
# for colname in columns: 
#     col = {}
#     if colname in REQUEST_EXCLUDE_FIELDS: 
#         continue
#     for key in COMMON_KEY:
#         if not hasattr(columns[colname], key): 
#             continue
#         attr = getattr(columns[colname], key)
#         if key == "type": 
#             # Get python type from sqlalchemy
#             # https://stackoverflow.com/questions/4165143/easy-convert-betwen-sqlalchemy-column-types-and-python-data-types
#             col[key] = attr.python_type
#             continue
#         col[key] = attr
#     # Avoiding add an empty dict into col array
#     if not bool(col):
#         continue
#     cols.append(col)

        
# def args_parsing(cols: list): 
#     # print("COLS",cols)
#     parser = reqparse.RequestParser() 
#     for col in cols: 
#         # print("=====col", col)
#         parser.add_argument(col["name"], default=col["default"], required=True,
#                             type=col["type"], nullable=col["nullable"])
#     return parser.parse_args()


# bp = Blueprint(name='roles', import_name=__name__, url_prefix=url_prefix)
# api = Api(bp)

# class CollectionApi(Resource): 
#     def put(self, id): 
#         existed_obj = db.session.query(model).get(id) 
#         if not existed_obj: 
#             return jsonify({"error_code": "PARAM_ERROR", "error_message": f"Role with id {id} does not exist in the database!"}, status=409)
        
#         args = args_parsing(cols)
#         existed_obj = add_info_into_obj(existed_obj, args)
#         db.session.commit()
   
#         return resp(to_dict(existed_obj))

#     def get(self, id): 
#         obj = db.session.query(model).get(id) 
#         return resp(to_dict(obj))
    
#     def delete(self, id): 
#         # check duplicate obj
#         obj = db.session.query(model).get(id)
#         db.session.delete(obj)
#         db.session.commit()
#         return jsonify({})

# class InstanceApi(Resource): 
#     def get(self): 
#         objs = db.session.query(model).all()
#         return resp([to_dict(obj) for obj in objs])
    
#     def post(self): 
#         args = args_parsing(cols)
        
#         # check duplicate obj
        
#         obj = model() 
#         obj = add_info_into_obj(obj, args)
        
#         db.session.add(obj) 
#         db.session.commit()
        
#         return resp(to_dict(obj))
    
# view = CollectionApi.as_view()
    
# api.add_resource(CollectionApi, '/roles')
# api.add_resource(InstanceApi, '/roles/<id>')

