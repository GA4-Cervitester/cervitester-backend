import os

from tensorflow.python.keras.backend import argmax
from detection.models import Model

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from .firebase import storage
import mediafire_dl

def loadModel():
    version="0.0.0"
    if not os.path.exists(f"models/{version}.h5"):
        print("model not found downloading")
        url = f'https://www.mediafire.com/file/mun4ztj629jqllr/{version}.h5/file'
        output = f"models/{version}.h5"
        mediafire_dl.download(url, output, quiet=False)
    return version


    
def runDetection():
    version = loadModel()
    model = tf.keras.models.load_model(f'models/{version}.h5')
    img = load_img('image.jpg', target_size=(200, 200, 3))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, 0)
    result = model.predict(img_array)[0]
    return [np.argmax(result),version]
