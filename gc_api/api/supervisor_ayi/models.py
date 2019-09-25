import werkzeug.datastructures
from flask_restplus import fields, reqparse
from api import api

upload_parser = api.parser()
upload_parser.add_argument('image_file', location='files'
                           , type=werkzeug.datastructures.FileStorage
                           , required=True
                           , help="Image file")


