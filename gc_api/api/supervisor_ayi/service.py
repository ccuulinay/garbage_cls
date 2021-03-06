import os
import uuid
import base64
from flask import abort
from api import logger, application
from api.garbage_classifier.service import get_predition


class SupervisorAyiService(object):

    def preprocess(self, uploaded_image):
        if isinstance(uploaded_image, str):
            image_str = uploaded_image
            image_file = base64.b64decode(image_str)
            # logger.debug(image_file)
            ext = "jpeg"
            save_filename = str(uuid.uuid4()) + "." + ext
            destination = application.config['UPLOAD_FOLDER']
            if not os.path.exists(destination):
                os.makedirs(destination)
            with open(os.path.join(destination, save_filename), "wb") as f:
                f.write(image_file)
        else:
            logger.debug(uploaded_image)
            filename = uploaded_image.filename
            ext = filename.rsplit('.', 1)[1].lower()
            save_filename = str(uuid.uuid4()) + "." + ext
            destination = application.config['UPLOAD_FOLDER']
            if not os.path.exists(destination):
                os.makedirs(destination)
            uploaded_image.save(os.path.join(destination, save_filename))
        return os.path.join(application.config['UPLOAD_FOLDER'], save_filename)

    def predict(self, image_file, city):
        return get_predition(image_file, city)

    def ayi_comment(self, uploaded_image, city):
        image_to_comment = self.preprocess(uploaded_image)
        comment = self.predict(image_to_comment, city)
        logger.debug(comment)
        return image_to_comment, {"comment": comment}

    
    
