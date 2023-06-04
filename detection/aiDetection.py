import os
import torch
from tensorflow.python.keras.backend import argmax
from keras.applications.resnet import preprocess_input
from detection.models import Model

import tensorflow as tf
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from .firebase import storage
import mediafire_dl


def loadModel():
    # version="0.0.0"
    # version = "pap"
    # if not os.path.exists(f"models/{version}.h5"):
    #     print("model not found downloading")
    #     url = f'https://www.mediafire.com/file/mun4ztj629jqllr/{version}.h5/file'
    #     output = f"models/{version}.h5"
    #     mediafire_dl.download(url, output, quiet=False)

    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           'models/SLyoloV5-20230601T110132Z-001/SLyoloV5/yolov5/runs/train/exp/weights/best.pt')
    return model


def manual_preprocess():
    img = load_img('image.jpg', target_size=(224, 224))
    x = img_to_array(img)
    x = preprocess_input(x)
    x = x / 255.0  # rescale the image
    return x.reshape((1, *x.shape))


def runDetection():
    model = loadModel()
    # model = tf.keras.models.load_model(f'models/{version}.h5')
    # img = load_img('image.jpg', target_size=(224, 224, 3))
    # img = manual_preprocess()
    img = load_img('image.jpg', target_size=(224, 224))
    # img_array = img_to_array(img)
    # img_array = np.expand_dims(img_array, 0)
    results = model(img)
    # print(result)
    # return [result, version]
    # Ratio calculation

    detections = results.pandas().xyxy[0]
    num_detections = len(detections)
    detected_classes = detections['name'].tolist()

    normal = 'Negative for intraepithelial lesion'
    normal_count = 0
    for i in detected_classes:
        if i == normal:
            normal_count += 1

    ratio = normal_count / num_detections
    rounded_ratio = round(ratio, 4)
    percentage = rounded_ratio * 100
    abnormal_count = num_detections-normal_count

    print(f"Number of normal cells: {normal_count}")
    print(f"Ratio of normal to abnormal cells: {rounded_ratio}")
    print(f"Percentage: {percentage}")
    results.print()
    results.show()
    return [normal_count, rounded_ratio, abnormal_count]
