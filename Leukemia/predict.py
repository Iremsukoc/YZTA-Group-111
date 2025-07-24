import os
from utils import load_saved_model, prepare_image, predict_image

# --- Dosya yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "test_split_leukemia", "Pre", "WBC-Malignant-Pre-005.jpg")

def main():
    # Modeli yükle
    print("[INFO] Model yükleniyor...")
    model, class_names = load_saved_model()

    # Görseli hazırla
    print("[INFO] Görüntü işleniyor...")
    image_array = prepare_image(IMAGE_PATH)

    # Tahmin yap
    print("[INFO] Tahmin yapılıyor...")
    label = predict_image(image_array, model, class_names)

    # Sonuç
    print("\n========== Tahmin Sonucu ==========")
    print(f"Tahmin edilen sınıf: {label}")
    print("===================================\n")

if __name__ == "__main__":
    main()
