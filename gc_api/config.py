import os
import logging
from datetime import timedelta


class Config(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'ccuulinay')
    UPLOAD_FOLDER = os.path.join(APP_ROOT, "images")
    MODEL_FOLDER = os.path.join(APP_ROOT, "..", "models")
    MODEL_PATH = os.path.join(MODEL_FOLDER, "epoch_40_adam_without_drop_out.h5")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    

class Development(Config):
    DEBUG = True

    # Create Logger object
    FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
    logging.basicConfig(filename="app.log"
                        , level=logging.DEBUG
                        , format=FORMAT
                        , filemode='w')
    LOGGER = logging.getLogger()
    
    
class Production(Config):
    DEBUG = False

    # Create Logger object
    FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
    logging.basicConfig(filename="app.log"
                        , level=logging.INFO
                        , format=FORMAT
                        , filemode='w')
    LOGGER = logging.getLogger()


