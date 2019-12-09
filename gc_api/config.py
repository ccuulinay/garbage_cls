import os
import logging
import json
from datetime import timedelta


class Config(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'ccuulinay')
    UPLOAD_FOLDER = os.path.join(APP_ROOT, "images")
    MODEL_FOLDER = os.path.join(APP_ROOT, "..", "models")
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    # Load model and it's params in config file which from saving from training.
    MODEL_CONF_FILE = os.path.join(MODEL_FOLDER, "model_label_dict.json")
    with open(MODEL_CONF_FILE, 'r') as f:
        _models_params = json.loads(f.read())
    # MODEL_BASENAME = "_inceptionV3_epoch_30_without_dropout_level0"
    MODEL_BASENAME = "_mobilenetV2_epoch_30_without_dropout_level0"
    MODEL_PARAM = _models_params[MODEL_BASENAME]
    MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_PARAM['model_name'])
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    KEEP_UPLOAD_IMAGE = False
    

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


