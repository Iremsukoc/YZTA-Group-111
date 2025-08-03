import torch.nn as nn
import torchvision.models as models

def get_model(num_classes=3):
    model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
    
    # Son katmanı (classifier) değiştir
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model
