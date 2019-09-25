import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

# Initiate application
application = Flask(__name__)

# Load configuration from config object which default to Development
application.config.from_object(os.getenv('FLASK_ENVIRONMENT', 'config.Development'))

# CORS handling
CORS(application)

logger = application.config['LOGGER']

# Create api object for flask restplus
api = Api(application, title='Garbage Classifier',
          description='Garbage Classifier API', version=0.1)


@api.errorhandler(Exception)
def handle_error(e):
    code = e.code
    message = e.__str__
    return {"status": code, "message": message}, code

