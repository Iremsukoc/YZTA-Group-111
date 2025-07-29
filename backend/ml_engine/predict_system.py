import torch
import torch.nn as nn
from PIL import Image
import os
import argparse
import json
from pathlib import Path
from torchvision import transforms

from ml_engine.brain.model_training import BrainTumorCNN
from ml_engine.breast_cancer_integraion.model import get_model as get_breast_model
from ml_engine.skin.model import get_model as get_skin_model
from ml_engine.brain.utils import get_default_transforms as get_brain_transforms

# --- Merkezi Model Yapılandırması ---
MODEL_CONFIG = {
    'brain': {
        'model_class': BrainTumorCNN,
        'model_params': {'num_classes': 4},
        'model_path': 'brain/saved_model.pth',
        'class_names': ['glioma', 'meningioma', 'notumor', 'pituitary'],
        'transform': get_brain_transforms(img_size=224),
        'prediction_logic': 'softmax'
    },
    'breast': {
        'model_class': get_breast_model,
        'model_params': {'num_classes': 3},
        'model_path': 'breast_cancer_integraion/breast_cancer_model.pth',
        'class_names': ['benign', 'malignant', 'normal'],
        'transform': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ]),
        'prediction_logic': 'softmax'
    },
    'skin': {
        'model_class': get_skin_model,
        'model_params': {'device': 'cpu', 'data_parallel': False},
        'model_path': 'skin/best_model.pth',
        'class_names': ['Benign', 'Malignant'],
        'transform': transforms.Compose([
            transforms.Resize(size=(112, 112)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'prediction_logic': 'sigmoid'
    }
}


class CancerPredictor:
    def __init__(self, device='cpu'):
        self.device = torch.device(device)
        self.models = {}
        self._load_all_models()
        print(f"✅ Tüm modeller {self.device} üzerinde yüklendi.")

    def _load_all_models(self):
        base_dir = os.path.dirname(__file__)

        for cancer_type, config in MODEL_CONFIG.items():
            try:
                if 'device' in config['model_params']:
                    config['model_params']['device'] = self.device

                model = config['model_class'](**config['model_params'])
                strict_loading = False if cancer_type == 'skin' else True

                model_path = os.path.join(base_dir, config['model_path'])
                state_dict = torch.load(model_path, map_location=self.device)

                model.load_state_dict(state_dict, strict=strict_loading)
                model.to(self.device)
                model.eval()

                self.models[cancer_type] = model
                print(f"✅ {cancer_type.upper()} modeli yüklendi.")
            except Exception as e:
                print(f"❌ {cancer_type.upper()} modeli yüklenemedi: {e}")

    def predict_single_image(self, image_path, cancer_type):
        try:
            config = MODEL_CONFIG[cancer_type]
            model = self.models[cancer_type]
            transform = config['transform']
            class_names = config['class_names']

            image = Image.open(image_path).convert("RGB")
            image_tensor = transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = model(image_tensor)

            if config['prediction_logic'] == 'sigmoid':
                probability = torch.sigmoid(outputs).item()
                predicted_index = 1 if probability > 0.5 else 0
                confidence = probability if predicted_index == 1 else 1 - probability
                return {
                    'image_path': image_path,
                    'predicted_class': class_names[predicted_index],
                    'confidence': round(confidence * 100, 2)
                }
            else:
                probabilities = torch.softmax(outputs, dim=1)[0]
                confidence, predicted_index = torch.max(probabilities, 0)
                return {
                    'image_path': image_path,
                    'predicted_class': class_names[predicted_index.item()],
                    'confidence': round(confidence.item() * 100, 2),
                    'all_probabilities': {
                        class_names[i]: round(prob.item() * 100, 2)
                        for i, prob in enumerate(probabilities)
                    }
                }
        except Exception as e:
            return {'error': f"{cancer_type} tahmini başarısız: {str(e)}"}

    def get_random_test_images(self, cancer_type, num_images=5):
        folder = Path(f"test_data_pool/{cancer_type}")
        if not folder.exists():
            return []
        images = list(folder.glob("**/*.jpg")) + list(folder.glob("**/*.jpeg")) + list(folder.glob("**/*.png"))
        if len(images) == 0:
            return []
        return torch.utils.data.random_split(images, [num_images, len(images) - num_images])[0]

    def batch_predict(self, cancer_type, num_images=5, show_logs=True):
        image_paths = self.get_random_test_images(cancer_type, num_images)
        predictions = []
        correct = 0

        for path in image_paths:
            path_str = str(path)
            true_label = Path(path_str).parent.name
            result = self.predict_single_image(path_str, cancer_type)

            if show_logs:
                print(f"📷 {os.path.basename(path_str)}")
                print(f"🔍 Tahmin: {result['predicted_class']}, Doğru Etiket: {true_label}")
                print(f"✅ Güven: {result['confidence']}%\n")

            is_correct = result['predicted_class'].lower() == true_label.lower()
            if is_correct:
                correct += 1

            result.update({'true_label': true_label, 'is_correct': is_correct})
            predictions.append(result)

        accuracy = (correct / len(predictions)) * 100 if predictions else 0
        print(f"\n🎯 {cancer_type.upper()} ACCURACY: {correct}/{len(predictions)} = {accuracy:.2f}%")
        return predictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kanser Türü Sınıflandırıcı")
    parser.add_argument("--image_path", type=str, help="Tek görsel tahmini için dosya yolu")
    parser.add_argument("--model_type", type=str, choices=MODEL_CONFIG.keys(), required=True, help="Kanser modeli türü")
    parser.add_argument("--batch", action="store_true", help="Batch tahmin çalıştır")
    parser.add_argument("--num_images", type=int, default=5, help="Batch modunda kullanılacak görüntü sayısı")
    args = parser.parse_args()

    predictor = CancerPredictor(device='cpu')

    if args.batch:
        predictor.batch_predict(args.model_type, num_images=args.num_images)
    elif args.image_path:
        result = predictor.predict_single_image(args.image_path, args.model_type)
        print(json.dumps(result, indent=2))
    else:
        print("❌ Lütfen ya --image_path ya da --batch parametresini sağlayın.")
