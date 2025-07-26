import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
import os

# --- Sınıf etiketleri ---
CLASS_NAMES = ["Benign", "Early", "Pre", "Pro"]

# --- Model yolu ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "resnet50.h5")

def load_saved_model():
    """
    Klasör içindeki modeli yükler ve sınıf etiketleriyle birlikte döndürür.
    """
    model = load_model(MODEL_PATH)
    return model, CLASS_NAMES

def prepare_image(image_path, target_size=(224, 224)):
    """
    Verilen görseli modele uygun hale getirir:
    - Yükler
    - Yeniden boyutlandırır
    - NumPy array'e çevirir
    - ResNet50'ye uygun normalize eder
    - Batch boyutu ekler
    """
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)
    return img_array

def predict_image(image_array, model, class_names):
    """
    İşlenmiş görüntü array'i üzerinden tahmin yapar.
    """
    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions[0])
    predicted_label = class_names[predicted_index]
    return predicted_label
