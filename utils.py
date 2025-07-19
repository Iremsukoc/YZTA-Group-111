from PIL import Image
from torchvision import transforms
import torch

def get_default_transforms(img_size=224):
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],  
                             std=[0.229, 0.224, 0.225])
    ])

def load_and_transform_image(image_path, img_size=224):
    transform = get_default_transforms(img_size)
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)  # [1, C, H, W]
    return image

def predict_image(model, image_path, class_names, device):
    model.eval()
    image_tensor = load_and_transform_image(image_path).to(device)
    with torch.no_grad():
        output = model(image_tensor)
        pred_label = torch.argmax(output, dim=1).item()
    return class_names[pred_label]
