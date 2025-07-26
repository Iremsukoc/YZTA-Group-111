# lung_service.py

from tensorflow.keras.models import load_model
from LungProject.utils import preprocess_single_image, predict_uploaded_image
from PIL import Image
import io
import numpy as np

class LungService:
    def __init__(self, model_path: str, target_size=(128, 128), color_mode="grayscale"):
        self.model = load_model(model_path)
        self.target_size = target_size
        self.color_mode = color_mode
        self.label_map = {
            0: 'Benign cases',
            1: 'Malignant cases',
            2: 'Normal cases'
        }

    def predict_from_file(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))

        # Geçici olarak kaydetmemiz gerekebilir çünkü utils.py "path" istiyor
        temp_path = "temp_lung_image.jpg"
        image.save(temp_path)

        # Tahmin
        predicted_label = predict_uploaded_image(
            image_path=temp_path,
            model=self.model,
            label_map=self.label_map,
            target_size=self.target_size,
            color_mode=self.color_mode
        )

        return {
            "predicted_class": predicted_label
        }
