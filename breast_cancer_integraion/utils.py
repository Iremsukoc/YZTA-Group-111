from torchvision import transforms
from PIL import Image
import torch

def get_default_transforms(img_size=224):
    """Breast cancer için varsayılan transform fonksiyonu"""
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.Lambda(lambda img: img.convert("RGB")),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

def load_and_transform_image(image_path, img_size=224):
    """Resim yükleme ve transform fonksiyonu"""
    transform = get_default_transforms(img_size)
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)  # [1, C, H, W]
    return image

def predict_image(model, image_path, class_names, device):
    """Tek resim tahmin fonksiyonu"""
    model.eval()
    image_tensor = load_and_transform_image(image_path).to(device)
    with torch.no_grad():
        output = model(image_tensor)
        pred_label = torch.argmax(output, dim=1).item()
    return class_names[pred_label] 