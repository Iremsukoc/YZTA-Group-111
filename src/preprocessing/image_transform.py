import numpy as np
import cv2

def preprocess_single_image(image_path, target_size=(128, 128), color_mode='grayscale'):
    """
    Verilen tek bir görseli modeli beslemek için uygun formata getirir.
    
    Args:
        image_path (str): Görselin dosya yolu
        target_size (tuple): Beklenen boyut (yükseklik, genişlik)
        color_mode (str): 'grayscale' veya 'rgb'

    Returns:
        np.array: Hazır girdi (model.predict'e verilebilir)
    """
    # Görseli oku
    if color_mode == 'grayscale':
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Boyutlandır
    image = cv2.resize(image, target_size)

    # Normalize et
    image = image.astype('float32') / 255.0

    # Kanal boyutunu ekle (grayscale ise (128, 128) → (128, 128, 1))
    if color_mode == 'grayscale':
        image = np.expand_dims(image, axis=-1)

    # Batch boyutu ekle → (1, 128, 128, 1)
    image = np.expand_dims(image, axis=0)

    return image


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