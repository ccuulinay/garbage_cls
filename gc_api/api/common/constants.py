from api import application
import os

MODEL_PARAM = application.config['MODELS_PARAM']
CITIES_AND_MODEL_NAME = list(filter(None, application.config['CITIES_AND_MODEL_NAME'].split(";")))

MODELS = {}
ALLOWED_CITIES = set()
for c_n_mn in CITIES_AND_MODEL_NAME:
    city, model_basename = c_n_mn.split(",")
    city, model_basename = city.strip(), model_basename.strip()

    MODEL_PATH = os.path.join(application.config['MODEL_FOLDER'], MODEL_PARAM[city][model_basename]['model_name'])
    MODEL_LABELS_DICT = {int(k): v for k, v in MODEL_PARAM[city][model_basename]['label_dict'].items()}
    MODEL_IMAGE_SIZE = MODEL_PARAM[city][model_basename]['IMAGE_SIZE']
    MODELS[city] = {
        "MODEL_PATH": MODEL_PATH,
        "MODEL_LABELS_DICT": MODEL_LABELS_DICT,
        "MODEL_IMAGE_SIZE": MODEL_IMAGE_SIZE,
    }
    ALLOWED_CITIES.add(str(city).lower())



# MODEL_LABELS_DICT = {int(k): v for k,v in MODEL_PARAM['label_dict'].items()}
# MODEL_IMAGE_SIZE = MODEL_PARAM['IMAGE_SIZE']
