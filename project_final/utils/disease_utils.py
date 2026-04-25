import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = "models/03_disease_detection/plant_disease_model.h5"

_model = None

def load_model_once():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model


CLASS_NAMES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___healthy',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus'
    # 'Tomato___healthy'
]


def process_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_disease(image_file):
    model = load_model_once()
    image = Image.open(image_file)

    processed_img = process_image(image)
    predictions = model.predict(processed_img)

    predicted_idx = np.argmax(predictions)
    predicted_class = CLASS_NAMES[predicted_idx]
    confidence = float(np.max(predictions)) * 100

    return predicted_class, confidence