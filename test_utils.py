import os
from tensorflow.keras.models import load_model
from src.preprocessing.image_transform import predict_uploaded_image, preprocess_single_image
# Modeli yükle
model = load_model("lung_cancer_cnn.h5")

# Etiket sözlüğü (model çıktılarına karşılık gelen sınıflar)
LABEL_MAP = {
    0: 'Benign cases',
    1: 'Malignant cases',
    2: 'Normal cases'
}

# Kullanıcıdan gelen ya da test etmek istediğin görselin yolu
image_path = r"C:\Users\Ali İhsan Sancar\Desktop\lung_cancer_project\test_split_lung\Normal cases\colorjitter (12).jpg"



if not os.path.exists(image_path):
    print("HATA: Görsel dosyası bulunamadı!\nYol:", image_path)
    exit()


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