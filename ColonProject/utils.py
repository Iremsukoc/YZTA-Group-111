# utils.py
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image

def transform_image(uploaded_image, target_size=(224, 224)):
    img = Image.open(uploaded_image).convert('RGB')
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(model, img_array, class_names):
    prediction = model.predict(img_array)[0]
    predicted_class = class_names[np.argmax(prediction)]
    confidence = float(np.max(prediction))
    return predicted_class, confidence
