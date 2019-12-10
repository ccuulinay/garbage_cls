import werkzeug.datastructures
from flask_restplus import fields, reqparse
from api import api

upload_parser = api.parser()
upload_parser.add_argument('image_file', location='files'
                           , type=werkzeug.datastructures.FileStorage
                           , required=True
                           , help="Image file")
upload_parser.add_argument(
    'city', type=str
    , required=True
    , help="Which city you are in?"
)

camera_capture_parser = api.parser()
camera_capture_parser.add_argument(
    'image_string', type=str
    , required=True
    , help="Camera capture image screen"
)
camera_capture_parser.add_argument(
    'city', type=str
    , required=True
    , help="Which city you are in?"
)


camera_capture = api.model('camera_capture', {
    "image_string": fields.String(required=True, description="Camera capture base64 image string.")
})
