import os
from flask import after_this_request
from flask_restplus import Namespace, Resource, marshal
from werkzeug.utils import secure_filename
from api import api, logger, application
from api.supervisor_ayi.models import upload_parser as image_upload_parser
from api.supervisor_ayi.models import camera_capture_parser
from api.supervisor_ayi.service import SupervisorAyiService
from api.common.constants import ALLOWED_CITIES

supervisor_ayi_service = SupervisorAyiService()


supervisor_ayi_ns = Namespace('supervisor_ayi', description="supervisor ayi operations")


@supervisor_ayi_ns.route("/garbage_image")
@supervisor_ayi_ns.expect(image_upload_parser)
class SupervisorAyiOperations(Resource):
    def post(self):
        """
        Upload a image
        :return:
        """
        args = image_upload_parser.parse_args()
        uploaded = args['image_file']
        city = args['city']
        logger.debug(uploaded)
        if uploaded.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
            return {'Message': "No file selected"}
        if not validate_city(city):
            return {'Message': "Input city is not supported so far."}
            # city = str(ALLOWED_CITIES[0]).lower()
        else:
            city = str(city).lower()
        if uploaded and self.validate_imagefile(uploaded.filename):
            temp_image, response = supervisor_ayi_service.ayi_comment(uploaded, city)

            @after_this_request
            def after_request_func(res):
                if application.config['KEEP_UPLOAD_IMAGE']:
                    pass
                else:
                    logger.debug("Remove temp image file.")
                    if os.path.exists(temp_image):
                        os.remove(temp_image)
                return res
            
            return response

    @staticmethod
    def validate_imagefile(filename):
        allowed_img_ext = application.config['ALLOWED_EXTENSIONS']
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_img_ext


@supervisor_ayi_ns.route("/camera_capture")
class SupervisorAyiOperations(Resource):
    @supervisor_ayi_ns.expect(camera_capture_parser)
    def post(self):
        args = camera_capture_parser.parse_args()
        uploaded_image_string = args['image_string']
        city = args['city']
        # Validate city param, if not in allowed list, set as default, Shanghai.
        if not validate_city(city):
            city = str(list(ALLOWED_CITIES)[0]).lower()
        else:
            city = str(city).lower()
        temp_image, response = supervisor_ayi_service.ayi_comment(uploaded_image_string, city)

        @after_this_request
        def after_request_func(res):
            if application.config['KEEP_UPLOAD_IMAGE']:
                pass
            else:
                logger.debug("Remove temp image file.")
                if os.path.exists(temp_image):
                    os.remove(temp_image)
            return res

        return response


def validate_city(city):
    allowed_cities = ALLOWED_CITIES
    return str(city).lower() in allowed_cities
