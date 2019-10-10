import os
from flask import Blueprint, render_template
from flask_cors import CORS
from api import application

static_pages = Blueprint('main', __name__
                         , template_folder=application.config['STATIC_FOLDER']
                         # , static_folder=os.path.join(application.config['STATIC_FOLDER'], "static")
                         )

# CORS handling
CORS(static_pages)


@static_pages.route('/')
def hello():
    return render_template("index.html")