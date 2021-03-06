import tensorflow as tf
import os
import time
from api import logger, application
from api.common.constants import MODELS

# IMAGE_SIZE = MODEL_IMAGE_SIZE


def preprocess_imagefile(filename, city):
    IMAGE_SIZE = MODELS[city]['MODEL_IMAGE_SIZE']
    try:
        # read file as byte
        image_string = tf.io.read_file(filename)
        # decode as string
        image_decoded = tf.image.decode_jpeg(image_string, channels=3)
        # image_decoded = tf.image.decode_gif(image_string)
        ## P.S tf.image.decode_image return shapeless tensor.
        # image_decoded = tf.image.decode_image(image_string)

        # resize to given image size
        image_resized = tf.image.resize(image_decoded, (IMAGE_SIZE, IMAGE_SIZE))
        # normalization
        image_normalized = (tf.cast(image_resized, tf.float32 ) /127.5) - 1

        return image_normalized

    except Exception as e:
        logger.error(e)
        logger.debug(filename)


def load_model(city_models=MODELS):
    global garbage_cls
    start_time = time.time()
    garbage_cls = {}
    for city, model in city_models.items():
        _cls = tf.keras.models.load_model(model['MODEL_PATH'])
        garbage_cls[city] = _cls
    # garbage_cls = tf.keras.models.load_model(model_path)
    logger.info("--- Model loaded in %s seconds ---" % (time.time() - start_time))


def get_predition(image, city='general'):
    if "garbage_cls" not in globals():
        load_model()
    image_X = preprocess_imagefile(image, city)
    image_X = tf.expand_dims(image_X, axis=0)
    pred_Y =  garbage_cls[city].predict(image_X)
    return MODELS[city]['MODEL_LABELS_DICT'][pred_Y.argmax()]