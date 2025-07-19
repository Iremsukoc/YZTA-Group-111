import os
import random
from PIL import Image
import torch
from torchvision import transforms
from model import get_model
from config import IMG_SIZE, CLASSES, DEVICE  # MODEL_PATH kaldırıldı!

def predict_single_image():
    print("Script started")

    # MODEL SELECTION
    model_dir = "saved_model"
    model_files = [f for f in os.listdir(model_dir) if f.endswith(".pth")]

    print("\n Available models:")
    for i, model_name in enumerate(model_files):
        print(f"{i}: {model_name}")

    choice = int(input("\n Select the model you want to use (enter index): "))
    MODEL_PATH = os.path.join(model_dir, model_files[choice])
    print(f" Selected model: {MODEL_PATH}")

    # Test dataset directory
    dataset_root = os.path.join("data", "breast_cancer_dataset_split", "test")

    selected_class = random.choice(CLASSES)
    class_path = os.path.join(dataset_root, selected_class)

    image_files = [
        f for f in os.listdir(class_path)
        if f.lower().endswith(".png") and "_mask" not in f
    ]

    if not image_files:
        print("No suitable image found.")
        return

    image_file = random.choice(image_files)
    image_path = os.path.join(class_path, image_file)

    print(f"Selected class: {selected_class}")
    print(f"Image name: {image_file}")
    print(f"Does file exist? {os.path.exists(image_path)}")

    import matplotlib.pyplot as plt

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Lambda(lambda img: img.convert("RGB")),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5],
                             [0.5, 0.5, 0.5])
    ])

    pil_image = Image.open(image_path)
    if not isinstance(pil_image, Image.Image):
        pil_image = Image.open(image_path)
    image_tensor = transform(pil_image)
    if not isinstance(image_tensor, torch.Tensor):
        raise TypeError('Transform did not return a tensor')
    image_tensor = image_tensor.unsqueeze(0).to(DEVICE)

    model = get_model().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    with torch.no_grad():
        outputs = model(image_tensor)
        if outputs is None:
            print("Model did not produce any output.")
            return

        _, pred = torch.max(outputs, 1)

        try:
            predicted_class = CLASSES[int(pred.item())]
        except Exception as e:
            print(f"CLASSES error: {e}")
            return

        probs = torch.nn.functional.softmax(outputs, dim=1)

    print(" Class probabilities:", probs.cpu().numpy())
    print(f"\n Predicted class: {predicted_class}")
    print(f" Actual class    : {selected_class}")

    # LLM explanation removed because llm_inference.py is deleted
    # from llm_inference import get_llm_response  
    # llm_output = get_llm_response(predicted_class)
    # print("\nLLM explanation:")
    # print(llm_output)

    img = Image.open(image_path)
    plt.imshow(img)
    plt.title(f"Prediction: {predicted_class}")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    predict_single_image()
