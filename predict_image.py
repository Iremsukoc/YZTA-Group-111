import torch
from src.model_training import BrainTumorCNN
from utils import predict_image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Class names
class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

# Model
model = BrainTumorCNN(num_classes=len(class_names))
model.load_state_dict(torch.load("models/saved_model.pth", map_location=device))
model.to(device)

# Predict
img_path = "data/Testing/meningioma/image1.jpg"  # or input from user
prediction = predict_image(model, img_path, class_names, device)
print(f"Prediction: {prediction}")
