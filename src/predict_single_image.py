import os
import random
from PIL import Image
import torch
from torchvision import transforms
from model import get_model
from config import MODEL_PATH, IMG_SIZE, CLASSES, DEVICE

def predict_random_image():
    print("Script başladı")

    # Dataset test dizini
    dataset_root = os.path.join("data", "breast_cancer_dataset_split", "test")

    selected_class = random.choice(CLASSES)
    class_path = os.path.join(dataset_root, selected_class)

    image_files = [
        f for f in os.listdir(class_path)
        if f.lower().endswith(".png") and "_mask" not in f
    ]

    if not image_files:
        print("Uygun görüntü bulunamadı.")
        return

    image_file = random.choice(image_files)
    image_path = os.path.join(class_path, image_file)

    print(f"Seçilen sınıf: {selected_class}")
    print(f"Görsel adı: {image_file}")
    print(f"Dosya mevcut mu? {os.path.exists(image_path)}")

    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Lambda(lambda img: img.convert("RGB")),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
])

    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(DEVICE)

    # Model
    model = get_model().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    # Tahmin
    with torch.no_grad():
        outputs = model(image)
        _, pred = torch.max(outputs, 1)

    predicted_class = CLASSES[pred.item()]
    probs = torch.nn.functional.softmax(outputs, dim=1)
    print(" Sınıf olasılıkları:", probs.cpu().numpy())

    # Sonuç
    print(f"\n Tahmin edilen sınıf: {predicted_class}")
    print(f" Gerçek sınıf       : {selected_class}")
    


if __name__ == "__main__":
    predict_random_image()


