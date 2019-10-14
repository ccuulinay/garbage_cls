import os
from flask import Flask, redirect
from flask_cors import CORS
from flask_restplus import Api

# Initiate application
application = Flask(__name__, template_folder="../static", static_folder="../static/static")

# Load configuration from config object which default to Development
# application.config.from_object(os.getenv('FLASK_ENVIRONMENT', 'config.Development'))
application.config.from_object(os.getenv('FLASK_ENVIRONMENT', 'config.Production'))

# CORS handling
CORS(application)


@application.errorhandler(404)
def page_not_found(e):
    return redirect('/')


logger = application.config['LOGGER']


# Create api object for flask restplus
api = Api(None, title='Garbage Classifier',
            doc='/docs/',
            description='Garbage Classifier API', version=0.1)


@api.errorhandler(Exception)
def handle_error(e):
    code = e.code
    message = e.__str__
    return {"status": code, "message": message}, code


