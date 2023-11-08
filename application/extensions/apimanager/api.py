from flask_restful import Resource, Api, reqparse
from flask import Blueprint
from ...database import db
from ...models.authentication import User


class IllegalArgumentError(Exception):
    """This exception is raised when a calling function has provided illegal
    arguments to a function or method.

    """
    pass

COMMON_KEY = ('type', 'nullable', 'default', 'name')
REQUEST_EXCLUDE_FIELDS = ("id", "created_at", "created_by", "updated_at", 
                        "updated_by", "deleted_at", "deleted_by", "deleted")
METHODS = ("GET", "POST", "UPDATE", "DELETE")


class ApiManager(object): 
    APINAME_FORMAT = '{0}api'
    BLUEPRINTNAME_FORMAT = '{0}{1}'
    
    def __init__(self, app=None, *args, **kw): 
        self.app = app
        
        if self.app is not None:   
            self.init_app(self.app, *args, **kw)
        
    def init_app(self, app=None, view_cls=Resource, db=None, *args, **kw): 
        if app is not None: 
            self.app = app
        
        if view_cls is not None: 
            self.view_cls = view_cls 
            self.collection_view_cls = self.view_cls[0] 
            self.instance_view_cls = self.view_cls[1]
        
        if db is not None: 
            self.db = db
    
    @staticmethod
    def _next_blueprint_name(blueprints, basename):
        
        # blueprints is a dict whose keys are the names of the blueprints
        existing = [name for name in blueprints if name.startswith(basename)]
        # if this is the first one...
        if not existing:
            next_number = 0
        else:
            # for brevity
            b = basename
            existing_numbers = [int(n.partition(b)[-1]) for n in existing]
            next_number = max(existing_numbers) + 1
        return ApiManager.BLUEPRINTNAME_FORMAT.format(basename, next_number)
    
    @staticmethod
    def api_name(collection_name):
        """Returns the name of the :class:`API` instance exposing models of the
        specified type of collection.

        `collection_name` must be a string.

        """
        return ApiManager.APINAME_FORMAT.format(collection_name)
        
    def _get_columns_map(self, columns) -> list:
        # RESULT:
        # [{'type': String(), 'nullable': False, 'default': None, 'unique': True, 'name': 'name'}, 
        # {'type': String(), 'nullable': True, 'default': None, 'unique': None, 'name': 'description'}]
        cols = []
        for colname in columns: 
            col = {}
            if colname in REQUEST_EXCLUDE_FIELDS: 
                continue
            for key in COMMON_KEY:
                if not hasattr(columns[colname], key): 
                    continue
                attr = getattr(columns[colname], key)
                if key == "type": 
                    # print("====== python_type", attr.python_type)
                    # Get python type from sqlalchemy
                    # https://stackoverflow.com/questions/4165143/easy-convert-betwen-sqlalchemy-column-types-and-python-data-types
                    col[key] = attr.python_type
                    continue
                col[key] = attr
            # Avoiding add an empty dict into col array
            if not bool(col):
                continue
            cols.append(col)
        return cols
    
    def _parse_args(self, cols: list): 
        parser = reqparse.RequestParser() 
        for col in cols: 
            # print("=====col", col)
            parser.add_argument(col["name"], default=col["default"], required=True,
                                type=col["type"], nullable=col["nullable"])
        return parser.parse_args()
    
        
    def create_api_blueprint(self, model=None, collection_name=None, app=None,
                            url_prefix="/api/v1", *args, **kw):
        if app is None: 
            app = self.app 
        if model is None: 
            raise IllegalArgumentError("model can not be None!") 
        if collection_name is None: 
            raise IllegalArgumentError("collection_name can not be None!") 
        
        # ENDPOINT
        collection_endpoint = '/{0}'.format(collection_name)
        instance_endpoint = '/{0}/<id>'.format(collection_name)
        
        # NAME
        api_name = ApiManager.api_name(collection_name=collection_name)
        blueprint_name = ApiManager._next_blueprint_name(app.blueprints, api_name)
        
        blueprint = Blueprint(name=blueprint_name, import_name=__name__, url_prefix=url_prefix)
        api = Api(blueprint) 

        
        api.add_resource(self.collection_view_cls, \
                         collection_endpoint, resource_class_kwargs=dict(db=self.db,\
                         model=model, collection_name=collection_name)) 
        api.add_resource(self.instance_view_cls, \
                         instance_endpoint, resource_class_kwargs=dict(db=self.db,\
                         model=model, collection_name=collection_name)) 
        return blueprint
        
        
    def create_api(self, *args, **kw):
        # print("Call function create_api")
        if "app" in kw:
            # If an application object was already provided in the constructor,
            # raise an error indicating that the user is being confusing.
            if self.app is not None:
                msg = ('Cannot provide a Gatco application in the APIManager'
                       ' constructor and in create_api(); must choose exactly'
                       ' one')
                raise IllegalArgumentError(msg)
            app = kw.pop('app')
            blueprint = self.create_api_blueprint(*args, **kw) 
            app.register_blueprint(blueprint)
        else:
            # print("Create API")
            if self.app is not None: 
                app = self.app
                blueprint = self.create_api_blueprint(*args, **kw) 
                app.register_blueprint(blueprint)
            else: 
                print(" ===== ERR", "App is not initialized!")
            
        