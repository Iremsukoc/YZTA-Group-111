import os
import random
from PIL import Image
import torch
from torchvision import transforms
from model import get_model
from config import IMG_SIZE, CLASSES, DEVICE  # MODEL_PATH kaldırıldı!

def predict_single_image():
    print("Script başladı")

    # MODEL SEÇİMİ
    model_dir = "saved_model"
    model_files = [f for f in os.listdir(model_dir) if f.endswith(".pth")]

    print("\n Mevcut modeller:")
    for i, model_name in enumerate(model_files):
        print(f"{i}: {model_name}")

    choice = int(input("\n Kullanmak istediğiniz modeli seçin (index girin): "))
    MODEL_PATH = os.path.join(model_dir, model_files[choice])
    print(f" Seçilen model: {MODEL_PATH}")

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

    import matplotlib.pyplot as plt


    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Lambda(lambda img: img.convert("RGB")),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5],
                             [0.5, 0.5, 0.5])
    ])

    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(DEVICE)

    model = get_model().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()


    with torch.no_grad():
        outputs = model(image)
        if outputs is None:
            print("❌ Model çıktı üretmedi.")
            return

        _, pred = torch.max(outputs, 1)

        try:
            predicted_class = CLASSES[pred.item()]
        except Exception as e:
            print(f"❌ CLASSES hatası: {e}")
            return

        probs = torch.nn.functional.softmax(outputs, dim=1)

    print(" Sınıf olasılıkları:", probs.cpu().numpy())
    print(f"\n Tahmin edilen sınıf: {predicted_class}")
    print(f" Gerçek sınıf       : {selected_class}")

    from llm_inference import get_llm_response  
    llm_output = get_llm_response(predicted_class)
    print("\n📘 LLM'den açıklama:")
    print(llm_output)


    img = Image.open(image_path)
    plt.imshow(img)
    plt.title(f"Tahmin: {predicted_class}")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    predict_single_image()
