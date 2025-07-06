import torch

# Donanım kontrolü
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model için sabitler
NUM_CLASSES = 3
IMG_SIZE = 224
EPOCHS = 50
PATIENCE = 10
BATCH_SIZE = 32
LEARNING_RATE = 0.0001
MODEL_PATH = "saved_model/best_model.pth"

# Sınıf isimleri (split işleminde gördüğümüz)
CLASSES = ['benign', 'malignant', 'normal']
