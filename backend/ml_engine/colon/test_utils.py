import numpy as np
from tensorflow.keras.models import load_model
from model_transform import transform_image, predict_image
import os

# --- Dosya yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model_cnn.h5")

# Test edilecek görselin yolu (görsel dosyası .jpg, .png olabilir)
# İkisinden birini kullanabilirsiniz:


image_path = os.path.join(BASE_DIR, "test_split_colon", "Colon_adenocarcinoma", "colonca158.jpeg")  # <-- burada kendi görsel adını gir
#image_path = os.path.join(BASE_DIR, "test_split_colon", "Colon_benign_tissue", "colonn44.jpeg")


# --- Sınıf etiketleri ---
class_names = ['Colon_adenocarcinoma', 'Colon_benign_tissue']

# --- Modeli yükle ---
print("[INFO] Model yükleniyor...")
model = load_model(model_path)

# --- Görüntüyü işleyip tahmin yap ---
print("[INFO] Görüntü işleniyor...")
img_array = transform_image(image_path)

print("[INFO] Tahmin yapılıyor...")
predicted_label, confidence = predict_image(model, img_array, class_names)

# --- Sonucu yazdır ---
print("\n========== Tahmin Sonucu ==========")
print(f"Tahmin Edilen Sınıf : {predicted_label}")
print("===================================\n")
