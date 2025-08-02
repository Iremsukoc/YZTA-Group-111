import torch
import torch.nn as nn
from PIL import Image
import os
import argparse
import json
import numpy as np
from pathlib import Path
from torchvision import transforms

import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array

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
            transforms.CenterCrop(size=(112, 112)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'prediction_logic': 'sigmoid'
    },
    'lung': {
        'model_path': 'lung/lung_cancer_cnn.h5',
        'input_shape': (128, 128),
        'color_mode': 'grayscale',
        'class_names': ['Benign cases', 'Malignant cases', 'Normal cases'],
        'framework': 'tensorflow'
    },
    'leukemia': {
        'model_path': 'leukemia/models/resnet50.h5',
        'input_shape': (224, 224),
        'color_mode': 'rgb',
        'class_names': ['B-Cell', 'Early T-Cell', 'Pre B-Cell', 'T-Cell'],
        'framework': 'tensorflow'
    },
    'colon': {
        'model_path': 'colon/model_cnn.h5',
        'input_shape': (224, 224),
        'color_mode': 'rgb',
        'class_names': ['Benign', 'adenocarcinoma'],
        'framework': 'tensorflow'
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
                if config.get('framework') == 'tensorflow':
                    model_path = os.path.join(base_dir, config['model_path'])
                    model = tf.keras.models.load_model(model_path)
                    self.models[cancer_type] = model
                    print(f"✅ {cancer_type.upper()} (TF) modeli yüklendi.")
                else:
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
                    print(f"✅ {cancer_type.upper()} (Torch) modeli yüklendi.")
            except Exception as e:
                print(f"❌ {cancer_type.upper()} modeli yüklenemedi: {e}")

    def predict_single_image(self, image_path, cancer_type):
        try:
            config = MODEL_CONFIG[cancer_type]
            model = self.models[cancer_type]

            if config.get('framework') == 'tensorflow':
                img_size = config['input_shape']
                color_mode = config.get('color_mode', 'rgb')
                img = load_img(image_path, target_size=img_size, color_mode=color_mode)
                img_array = img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                predictions = model.predict(img_array)[0]
                predicted_index = np.argmax(predictions)
                confidence = float(predictions[predicted_index])
                class_names = config['class_names']

                return {
                    'image_path': image_path,
                    'predicted_class': class_names[predicted_index],
                    'confidence': round(confidence * 100, 2),
                    'all_probabilities': {
                        class_names[i]: round(prob * 100, 2)
                        for i, prob in enumerate(predictions)
                    }
                }
            else:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kanser Türü Sınıflandırıcı")
    parser.add_argument("--image_path", type=str, help="Tek görsel tahmini için dosya yolu")
    parser.add_argument("--model_type", type=str, choices=MODEL_CONFIG.keys(), required=True, help="Kanser modeli türü")
    args = parser.parse_args()

    predictor = CancerPredictor(device='cpu')
    result = predictor.predict_single_image(args.image_path, args.model_type)
    print(json.dumps(result, indent=2))

