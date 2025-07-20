"""
Defines the neural network architecture (EfficientNetV2L, as in the notebook).
"""

import torch.nn as nn
from torchvision import models

def get_model(device, data_parallel=True):
    """
    Returns a modified EfficientNetV2L model for binary classification.
    Args:
        device: torch.device object
        data_parallel (bool): If True, wraps model in nn.DataParallel
    Returns:
        model (nn.Module)
    """
    # Load pre-trained EfficientNetV2L
    model = models.efficientnet_v2_l(weights='DEFAULT')
    # Modify the classifier for binary output
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)
    if data_parallel:
        model = nn.DataParallel(model)
    model = model.to(device)
    return model
