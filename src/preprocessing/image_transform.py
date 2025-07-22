import numpy as np
import cv2
from PIL import Image

def preprocess_single_image(image_path, target_size=(128, 128), color_mode='grayscale'):
    """
    Verilen tek bir görseli PIL kullanarak modele uygun hale getirir.
    """

    try:
        img = Image.open(image_path)
    except Exception as e:
        raise FileNotFoundError(f"Görsel açılamadı: {image_path}\nHata: {e}")

    # Renk moduna göre dönüştür
    if color_mode == 'grayscale':
        img = img.convert("L")
    else:
        img = img.convert("RGB")

    # Yeniden boyutlandır
    img = img.resize(target_size)

    # NumPy dizisine çevir + normalize
    img_array = np.array(img).astype('float32') / 255.0

    # Kanal boyutu ekle (grayscale: (128,128) → (128,128,1))
    if color_mode == 'grayscale':
        img_array = np.expand_dims(img_array, axis=-1)

    # Batch boyutu ekle
    img_array = np.expand_dims(img_array, axis=0)

    return img_array



def predict_uploaded_image(image_path, model, label_map=None, target_size=(128, 128), color_mode='grayscale'):
    """
    preprocess_single_image() fonksiyonunu kullanarak tahmin yapan sade fonksiyon.

    Args:
        image_path (str): Görselin yolu
        model: Eğitilmiş model
        label_map (dict): Sınıf indexlerini etiket ismine çeviren sözlük
        target_size (tuple): Yeniden boyutlandırma hedefi
        color_mode (str): 'grayscale' veya 'rgb'

    Returns:
        str veya int: Tahmin edilen sınıf etiketi
    """
    # Ön işleme
    processed_image = preprocess_single_image(image_path, target_size=target_size, color_mode=color_mode)

    # Tahmin yap
    prediction = model.predict(processed_image)
    predicted_index = int(np.argmax(prediction))

    # Etiketi döndür
    if label_map:
        return label_map[predicted_index]
    else:
        return predicted_index



"""
ÖRNEK KULLANIM:

from tensorflow.keras.models import load_model

# Modeli yükle
model = load_model("lung_cancer_cnn.h5")

# Etiket sözlüğü (model çıktılarına karşılık gelen sınıflar)
LABEL_MAP = {
    0: 'Benign cases',
    1: 'Malignant cases',
    2: 'Normal cases'
}

# Kullanıcıdan gelen ya da test etmek istediğin görselin yolu
image_path = "uploads/user_uploaded_image.jpg"

# Tahmin yap
prediction_result = predict_uploaded_image(
    image_path=image_path,
    model=model,
    label_map=LABEL_MAP,
    target_size=(128, 128),
    color_mode='grayscale'  # Modelin eğitildiği formatla aynı olmalı
)

# Sonucu yazdır
print("Tahmin edilen sınıf:", prediction_result)


"""