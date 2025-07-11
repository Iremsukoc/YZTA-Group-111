import torch
import matplotlib.pyplot as plt
import random
from torchvision import transforms
from PIL import Image
from src.data_preprocessing import create_data_loaders
from src.model_training import BrainTumorCNN

def main():
    # Cihaz seçimi
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Parametreler
    data_dir = "data"
    img_size = 224
    batch_size = 32

    # Data loader
    _, test_loader = create_data_loaders(data_dir, img_size, batch_size)
    class_names = test_loader.dataset.classes

    # Modeli yükle
    model = BrainTumorCNN(num_classes=len(class_names))
    model.load_state_dict(torch.load("models/saved_model_final.pth", map_location=device))
    model.eval().to(device)

    # Tüm test verisini topla
    all_images = []
    all_labels = []

    for images, labels in test_loader:
        all_images.extend(images)
        all_labels.extend(labels)

    # Random 5 örnek seç
    indices = random.sample(range(len(all_images)), 5)
    selected_images = [all_images[i] for i in indices]
    selected_labels = [all_labels[i] for i in indices]

    # Görselleştir
    plt.figure(figsize=(12, 8))
    for i in range(5):
        image = selected_images[i].unsqueeze(0).to(device)
        true_label = selected_labels[i]
        pred = model(image)
        pred_label = torch.argmax(pred, dim=1).item()

        # Görseli normalize et
        img_np = selected_images[i].permute(1, 2, 0).cpu().numpy()
        img_np = img_np * [0.229, 0.224, 0.225] + [0.485, 0.456, 0.406]
        img_np = img_np.clip(0, 1)

        plt.subplot(2, 3, i + 1)
        plt.imshow(img_np)
        plt.title(f"True: {class_names[true_label]}\nPredicted: {class_names[pred_label]}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()