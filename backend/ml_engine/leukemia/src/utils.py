import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
import os
from config import MODEL_PATH

# Sınıf etiketleri (manuel olarak verildi)
CLASS_NAMES = ["Benign", "Early", "Pre", "Pro"]

def load_saved_model():
    model = load_model(MODEL_PATH)
    return model, CLASS_NAMES

def prepare_image(image_path, target_size=(224, 224)):
    """ Görseli yükle ve modele uygun hale getir """
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)
    return img_array

def predict_image(image_array, model, class_names):
    """ Tahmin yap """
    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions[0])
    predicted_label = class_names[predicted_index]
    return predicted_label

"""
ÖRNEK KULLANIM:

from utils import load_saved_model, prepare_image, predict_image

model, class_names = load_saved_model()
image_array = prepare_image("C:\\Users\\Ali İhsan Sancar\\Desktop\\leukemia-classifier\\test_split_leukemia\\Benign\\WBC-Benign-002.jpg")
label = predict_image(image_array, model, class_names)

print("Tahmin:", label)
"""
