# leukemia_service.py

from LeukemiaProject.utils import load_saved_model, prepare_image, predict_image
from PIL import Image
import io

class LeukemiaService:
    def __init__(self, target_size=(224, 224)):
        self.model, self.class_names = load_saved_model()
        self.target_size = target_size

    def predict_from_file(self, image_bytes: bytes):
        # Upload edilen dosyayı PIL ile aç
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Geçici dosya olarak kaydet
        temp_path = "temp_leukemia.jpg"
        image.save(temp_path)

        # Görseli modele hazırla
        image_array = prepare_image(temp_path, target_size=self.target_size)

        # Tahmini yap
        predicted_label = predict_image(image_array, self.model, self.class_names)

        return {
            "predicted_class": predicted_label
        }
