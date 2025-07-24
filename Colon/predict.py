import numpy as np
from tensorflow.keras.models import load_model
from utils import transform_image, predict_image
import os

# --- Dosya yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_cnn.h5")

# Görsel yolu
IMAGE_PATH = os.path.join(BASE_DIR, "test_split_colon", "Colon_adenocarcinoma", "colonca336.jpeg")
#IMAGE_PATH = os.path.join(BASE_DIR, "test_split_colon", "Colon_benign_tissue", "colonn16.jpeg")

# --- Sınıf etiketleri ---
class_names = ['Colon_adenocarcinoma', 'Colon_benign_tissue']

def main():
    print("[INFO] Model yükleniyor...")
    model = load_model(MODEL_PATH)

    print("[INFO] Görüntü işleniyor...")
    img_array = transform_image(IMAGE_PATH)

    print("[INFO] Tahmin yapılıyor...")
    predicted_label, confidence = predict_image(model, img_array, class_names)

    print("\n========== Tahmin Sonucu ==========")
    print(f"Tahmin Edilen Sınıf : {predicted_label}")
    print(f"Güven Oranı         : {confidence:.2f}")
    print("===================================\n")

if __name__ == "__main__":
    main()
