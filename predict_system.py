import torch
import torch.nn as nn
from PIL import Image
import os
import random
from pathlib import Path
import numpy as np

# Import transform functions from existing utils
from brain_tumor.utils import get_default_transforms as brain_transforms
from skin_cancer.src.preprocessing import get_val_transform as skin_transforms
from torchvision import transforms

# Import model architectures
from brain_tumor.model_training import BrainTumorCNN
from breast_cancer.model import get_model as get_breast_model
from skin_cancer.src.model import get_model as get_skin_model
from skin_cancer.src.preprocessing import get_val_transform as get_skin_val_transform
import yaml
import numpy as np
import matplotlib.pyplot as plt

class CancerPredictor:
    def __init__(self, device='cpu'):
        self.device = device
        self.models = {}
        self.class_names = {
            'brain': ['glioma', 'meningioma', 'notumor', 'pituitary'],
            'breast': ['benign', 'malignant', 'normal'],
            'skin': ['Benign', 'Malignant'],
        }
        self.transforms = {}
        self._load_models()
        print(f"✅ All models loaded successfully on {device}")

    def _load_models(self):
        # Brain Tumor Model
        try:
            brain_model = BrainTumorCNN(num_classes=4)
            state_dict = torch.load('brain_tumor/saved_model.pth', map_location=self.device)
            brain_model.load_state_dict(state_dict)
            brain_model.eval()
            brain_model.to(self.device)
            self.models['brain'] = brain_model
            self.class_names['brain'] = ['glioma', 'meningioma', 'notumor', 'pituitary']
            self.transforms['brain'] = brain_transforms(img_size=224)
            print("✅ Brain tumor model loaded")
        except Exception as e:
            print(f"❌ Error loading brain model: {e}")
        # Breast Cancer Model
        try:
            breast_model = get_breast_model(num_classes=3)
            state_dict = torch.load('breast_cancer/breast_cancer_model.pth', map_location=self.device)
            breast_model.load_state_dict(state_dict)
            breast_model.eval()
            breast_model.to(self.device)
            self.models['breast'] = breast_model
            self.class_names['breast'] = ['benign', 'malignant', 'normal']
            self.transforms['breast'] = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.Lambda(lambda img: img.convert("RGB")),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])
            print("✅ Breast cancer model loaded")
        except Exception as e:
            print(f"❌ Error loading breast model: {e}")
        # Skin Cancer Model
        try:
            skin_model = get_skin_model(self.device, data_parallel=True)
            state_dict = torch.load('skin_cancer/best_model.pth', map_location=self.device)
            skin_model.load_state_dict(state_dict, strict=False)
            skin_model.eval()
            skin_model.to(self.device)  # Ensure model is on the correct device
            self.models['skin'] = skin_model
            self.class_names['skin'] = ['Benign', 'Malignant']
            self.transforms['skin'] = transforms.Compose([
                transforms.Resize(size=(112, 112), antialias=True),
                transforms.CenterCrop(size=(112, 112)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            print("✅ Skin cancer model loaded")
        except Exception as e:
            print(f"❌ Error loading skin model: {e}")

    def predict_single_image(self, image_path, cancer_type):
        try:
            if not image_path or not cancer_type:
                return {'error': 'image_path or cancer_type is missing'}
            if cancer_type in ['brain', 'breast', 'skin']:
                model = self.models.get(cancer_type)
                transform = self.transforms.get(cancer_type)
                class_names = self.class_names.get(cancer_type)
                if model is None or transform is None or class_names is None:
                    return {'error': f'Model or transform not loaded for {cancer_type}'}
                image = Image.open(image_path).convert("RGB")
                image_tensor = transform(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    outputs = model(image_tensor)
                    if cancer_type == 'skin':
                        probabilities = torch.sigmoid(outputs)
                        threshold = 0.5
                        predicted_class = 1 if probabilities[0] > threshold else 0
                        confidence = probabilities[0].item() if predicted_class == 1 else 1 - probabilities[0].item()
                        return {
                            'cancer_type': 'skin',
                            'predicted_class': class_names[predicted_class],
                            'confidence': round(confidence * 100, 2)
                        }
                    else:
                        probabilities = torch.softmax(outputs, dim=1)
                        predicted_class = torch.argmax(probabilities, dim=1).item()
                        confidence = probabilities[0][predicted_class].item()
                        return {
                            'cancer_type': cancer_type,
                            'predicted_class': class_names[predicted_class],
                            'confidence': round(confidence * 100, 2),
                            'all_probabilities': {
                                class_names[i]: round(prob.item() * 100, 2)
                                for i, prob in enumerate(probabilities[0])
                            }
                        }
            return {'error': f'Unsupported cancer type or model not loaded: {cancer_type}'}
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}

    def get_random_test_images(self, cancer_type, num_images=5):
        """
        Get random test images from the test data pool.
        Args:
            cancer_type: 'brain', 'breast', 'skin'
            num_images: Number of random images to return
        Returns:
            list: List of image paths
        """
        test_pool_path = Path(f"test_data_pool/{cancer_type}")
        if not test_pool_path.exists():
            return []
        all_images = []
        for class_folder in test_pool_path.iterdir():
            if class_folder.is_dir():
                for image_file in class_folder.iterdir():
                    if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        all_images.append(str(image_file))
        if not all_images:
            return []
        import random
        return random.sample(all_images, min(num_images, len(all_images)))

    def batch_predict(self, cancer_type, num_images=10):
        """
        Perform batch prediction on random test images.
        Returns: list of dict (her zaman dict, None asla yok)
        """
        test_images = self.get_random_test_images(cancer_type, num_images)
        results = []
        for image_path in test_images:
            result = self.predict_single_image(image_path, cancer_type)
            if result is None:
                result = {'error': 'Prediction returned None', 'image_path': image_path}
            else:
                result['image_path'] = image_path
            results.append(result)
        return results

    def batch_predict_skin(self, num_images=5):
        """
        Skin kanseri için src/predict_random_test.py ile aynı şekilde batch prediction ve accuracy hesaplama.
        """
        # Test görsellerini (image_path, true_label) tuple olarak çek
        test_dir = 'skin_cancer/data/skin_test'
        from pathlib import Path
        import random
        all_images = []
        for class_name in ['Benign', 'Malignant']:
            class_path = Path(test_dir) / class_name
            if class_path.exists():
                for img_file in class_path.glob('*.jpg'):
                    all_images.append((str(img_file), class_name))
                for img_file in class_path.glob('*.jpeg'):
                    all_images.append((str(img_file), class_name))
                for img_file in class_path.glob('*.png'):
                    all_images.append((str(img_file), class_name))
        if len(all_images) < num_images:
            selected_images = all_images
        else:
            selected_images = random.sample(all_images, num_images)
        # Model ve transform
        model = self.models['skin']
        transform = self.transforms['skin']
        device = self.device
        # Tahminler
        predictions = []
        correct_predictions = 0
        for image_path, true_label in selected_images:
            from PIL import Image
            image = Image.open(image_path).convert('RGB')
            input_tensor = transform(image).unsqueeze(0).to(device)
            # Debug prints for device
            print(f"Model device: {next(model.parameters()).device}")
            print(f"Input tensor device: {input_tensor.device}")
            with torch.no_grad():
                output = model(input_tensor)
                probability = torch.sigmoid(output).item()
            pred_class = 'Malignant' if probability > 0.5 else 'Benign'
            is_correct = pred_class == true_label
            if is_correct:
                correct_predictions += 1
            predictions.append({
                'image_path': image_path,
                'true_label': true_label,
                'pred_class': pred_class,
                'probability': probability,
                'is_correct': is_correct
            })
        # Sonuçları yazdır
        print("\n" + "="*60)
        print("SKIN CANCER PREDICTION RESULTS (src logic)")
        print("="*60)
        for i, pred in enumerate(predictions):
            print(f"Image {i+1}: {os.path.basename(pred['image_path'])}")
            print(f"True Label: {pred['true_label']}")
            print(f"Prediction: {pred['pred_class']}")
            print(f"Probability: {pred['probability']:.4f}")
            print(f"Correct: {'✓' if pred['is_correct'] else '✗'}\n")
        print(f"Total images: {len(predictions)}")
        print(f"Correct predictions: {correct_predictions}")
        print(f"Accuracy: {correct_predictions/len(predictions)*100:.1f}%")
        return predictions

# Example usage functions
def demo_single_prediction():
    predictor = CancerPredictor(device='cuda')
    for cancer_type in ['brain', 'breast', 'skin']:
        test_images = predictor.get_random_test_images(cancer_type, 1)
        if test_images:
            print(f"\n🔬 Testing {cancer_type} cancer prediction:")
            result = predictor.predict_single_image(test_images[0], cancer_type)
            if result is None:
                print("   Prediction: Error (result is None)")
            elif 'error' in result:
                print(f"   Prediction: Error ({result['error']})")
            else:
                print(f"   Image: {test_images[0]}")
                print(f"   Prediction: {result.get('predicted_class', 'Error')}")
                print(f"   Confidence: {result.get('confidence', 0)}%")

def demo_batch_prediction():
    predictor = CancerPredictor(device='cuda')
    for cancer_type in ['brain', 'breast', 'skin']:
        print(f"\n🔬 Batch testing {cancer_type} cancer:")
        if cancer_type == 'skin':
            predictor.batch_predict_skin(5)
        else:
            results = predictor.batch_predict(cancer_type, 3)
            for result in results:
                if result is None:
                    print("   Error: result is None")
                elif 'error' in result:
                    print(f"   Error: {result['error']}")
                else:
                    print(f"   {result['image_path']} → {result['predicted_class']} ({result['confidence']}%)")

if __name__ == "__main__":
    print("🏥 Cancer Detection Prediction System")
    print("=" * 50)
    
    # Demo single predictions
    demo_single_prediction()
    
    # Demo batch predictions
    demo_batch_prediction() 