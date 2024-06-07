import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights='imagenet')

def getTop3(predictions):
    parsedResults = ["", "", ""]
    for i in range(3):
        parsedResults[i] = predictions[i][1].replace("_", " ")
    return parsedResults

def getPrediction(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    return getTop3(decode_predictions(predictions, top=3)[0])
