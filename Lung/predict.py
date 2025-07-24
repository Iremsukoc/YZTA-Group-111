import os
from tensorflow.keras.models import load_model
from utils import predict_uploaded_image

# --- Dosya yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "lung_cancer_cnn.h5")


#IMAGE_PATH = os.path.join(BASE_DIR, "test_split_lung", "Normal cases", "colorjitter (37).jpg")
#IMAGE_PATH = os.path.join(BASE_DIR, "test_split_lung", "Malignant cases", "auto_contrast (9).jpg")
IMAGE_PATH = os.path.join(BASE_DIR, "test_split_lung", "Benign cases", "auto_contrast (11).jpg")

# --- Etiket sözlüğü ---
LABEL_MAP = {
    0: 'Benign cases',
    1: 'Malignant cases',
    2: 'Normal cases'
}

def main():
    # Görsel mevcut mu?
    if not os.path.exists(IMAGE_PATH):
        print("HATA: Görsel dosyası bulunamadı!\nYol:", IMAGE_PATH)
        return

    # Modeli yükle
    print("[INFO] Model yükleniyor...")
    model = load_model(MODEL_PATH)

    # Tahmin yap
    print("[INFO] Tahmin yapılıyor...")
    prediction_result = predict_uploaded_image(
        image_path=IMAGE_PATH,
        model=model,
        label_map=LABEL_MAP,
        target_size=(128, 128),
        color_mode='grayscale'
    )

    # Sonuç
    print("\n========== Tahmin Sonucu ==========")
    print("Tahmin edilen sınıf:", prediction_result)
    print("===================================\n")

if __name__ == "__main__":
    main()
