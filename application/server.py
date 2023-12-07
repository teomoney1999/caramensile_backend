""" App entry point """

from flask import Flask 
from flask_restful import Resource, Api
from flask_cors import CORS
from .config.dev_config import Config
import logging

from .database import init_database
from .controllers import init_controllers
from .extensions import init_extensions

app = Flask(__name__) 
api = Api(app) 

app.config.from_object(Config)
CORS(app)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
# import application.models.authentication
# import application.models.customer
# import application.models.store
# import application.models.warehouse


init_database(app) 
init_extensions(app)
init_controllers(app)

