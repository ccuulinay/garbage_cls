import os
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from api import application
from api.supervisor_ayi.models import upload_parser as image_upload_parser
from api.supervisor_ayi.service import SupervisorAyiService

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

        if uploaded.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
            return {'Message': "No file selected"}
        if uploaded and self.validate_imagefile(uploaded.filename):
            response = supervisor_ayi_service.ayi_comment(uploaded)
            return response

    @staticmethod
    def validate_imagefile(filename):
        allowed_img_ext = application.config['ALLOWED_EXTENSIONS']
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_img_ext

