""" App entry point """

from flask import Flask 
from flask_restful import Resource, Api
from .config.dev_config import Config

from .database import init_database
from .controllers import init_controllers
from .extensions import init_extensions

app = Flask(__name__) 
api = Api(app) 

app.config.from_object(Config)

# import application.models.authentication
# import application.models.customer
# import application.models.store
# import application.models.warehouse


init_database(app) 
init_extensions(app)
init_controllers(app)

