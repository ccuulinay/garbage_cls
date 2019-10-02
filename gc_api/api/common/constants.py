from api import application

MODEL_LABELS_DICT = {int(k): v for k,v in application.config['MODEL_PARAM']['label_dict'].items()}
MODEL_IMAGE_SIZE = application.config['MODEL_PARAM']['IMAGE_SIZE']