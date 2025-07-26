# colon_service.py
from tensorflow.keras.models import load_model
from ColonProject.utils import transform_image, predict_image
from PIL import Image
import io

class ColonService:
    def __init__(self, model_path: str, target_size=(224, 224)):
        self.model = load_model(model_path)
        self.target_size = target_size
        self.class_names = ['Colon_adenocarcinoma', 'Colon_benign_tissue']

    def transform_image(self, uploaded_image):
        return transform_image(uploaded_image, target_size=self.target_size)

    def predict_from_path(self, image_path: str):
        img_array = self.transform_image(image_path)
        predicted_class, confidence = predict_image(self.model, img_array, self.class_names)
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4)
        }

    def predict_from_file(self, image_bytes: bytes):
        image = io.BytesIO(image_bytes)  # RAW byte stream olarak veriyoruz
        img_array = self.transform_image(image)
        predicted_class, confidence = predict_image(self.model, img_array, self.class_names)
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4)
        }
