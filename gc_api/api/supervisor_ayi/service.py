import os
import uuid
from flask import abort
from api import logger, application
from api.common.constants import level0_label_encoding_dict
from api.garbage_classifier.service import get_predition


class SupervisorAyiService(object):

    def preprocess(self, uploaded_image):
        filename = uploaded_image.filename
        ext = filename.rsplit('.', 1)[1].lower()
        save_filename = str(uuid.uuid4()) + "." + ext
        destination = application.config['UPLOAD_FOLDER']
        if not os.path.exists(destination):
            os.makedirs(destination)
        uploaded_image.save(os.path.join(destination, save_filename))
        return os.path.join(application.config['UPLOAD_FOLDER'], save_filename)

    def predict(self, image_file):
        return get_predition(image_file)

    def ayi_comment(self, uploaded_image):
        image_to_comment = self.preprocess(uploaded_image)
        comment = self.predict(image_to_comment)
        return {"comment": comment}
