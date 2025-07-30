# utils.py
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image

def transform_image(uploaded_image, target_size=(224, 224)):
    """
    Yüklenen görüntüyü modele uygun hale getirir:
    - RGB’ye çevirir
    - Yeniden boyutlandırır
    - NumPy array'e dönüştürür
    - Normalize eder
    - Batch boyutu ekler
    """
    img = Image.open(uploaded_image).convert('RGB')
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)  # batch dimension
    return img_array

def predict_image(model, img_array, class_names):
    """
    İşlenmiş görüntü array'i üzerinden tahmin yapar.
    """
    prediction = model.predict(img_array)[0]
    predicted_class = class_names[np.argmax(prediction)]
    confidence = float(np.max(prediction))
    return predicted_class, confidence



"""
Frontend / API Tarafında Kullanım Örneği


from utils import transform_image, predict_image
from tensorflow.keras.models import load_model

# Model ve etiket listesi
model = load_model('model_cnn.h5')
class_names = ['Colon_adenocarcinoma', 'Colon_benign_tissue']

# Kullanıcıdan gelen dosya
img_array = transform_image(uploaded_file)
label, conf = predict_image(model, img_array, class_names)
"""