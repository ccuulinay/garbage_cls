import os
import uuid
import base64
from flask import abort
from api import logger, application
from api.common.constants import MODEL_LABELS_DICT
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

    def predict(self, image_file):
        return get_predition(image_file)

    def ayi_comment(self, uploaded_image):
        image_to_comment = self.preprocess(uploaded_image)
        comment = self.predict(image_to_comment)
        return image_to_comment, {"comment": comment}

    def ayi_comment_capture(self, args):
        image_str = args['image_string']
        image_file = base64.b64decode(image_str)
        # logger.debug(image_file)
        ext = "jpeg"
        
        save_filename = str(uuid.uuid4()) + "." + ext
        destination = application.config['UPLOAD_FOLDER']
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(os.path.join(destination, save_filename), "wb") as f:
            f.write(image_file)
        
        image_to_comment = os.path.join(application.config['UPLOAD_FOLDER'], save_filename)

        comment = self.predict(image_to_comment)
        return image_to_comment, {"comment": comment}
    
