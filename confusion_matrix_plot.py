import os
import re
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from torchvision import models
from src.config import *
import importlib.util
from datetime import datetime
from src.model import get_model

# --- En son versiyonu bul ---
def get_latest_version():
    version = 0
    for fname in os.listdir("saved_model"):
        match = re.match(r"best_model_confset_v(\d+)\.pth", fname)
        if match:
            version = max(version, int(match.group(1)))
    return version

# --- Dinamik import ---
def dynamic_import(module_name):
    spec = importlib.util.find_spec(f"src.{module_name}")
    if spec is None:
        raise ImportError(f"Modül bulunamadı: {module_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --- CM ve loglama ---
def evaluate_and_plot(version_number, data_utils_module_name):
    data_utils_module = dynamic_import(data_utils_module_name)
    _, _, test_loader = data_utils_module.get_dataloaders()

    model = get_model().to(DEVICE)

    model_path = f"saved_model/best_model_confset_v{version_number}.pth"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model dosyası eksik: {model_path}")

    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    cm = confusion_matrix(all_labels, all_preds)
    class_names = test_loader.dataset.classes

    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.title(f"Confusion Matrix – v{version_number}")
    plt.tight_layout()

    os.makedirs("results", exist_ok=True)
    cm_path = f"results/confmat_confset_v{version_number}.png"
    plt.savefig(cm_path)
    plt.show()

    acc = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds, average='weighted')
    today = datetime.today().strftime("%Y-%m-%d")

    data_utils_pyfile = f"{data_utils_module_name}.py" if not data_utils_module_name.endswith(".py") else data_utils_module_name
    log_text = f"""[confmat_confset_v{version_number}.png]
→ Model: saved_model/best_model_confset_v{version_number}.pth
→ Data augment: src/{data_utils_pyfile}.py
→ Accuracy: {acc:.4f}
→ F1-score: {f1:.4f}
→ Tarih: {today}
"""

    txt_path = f"results/confmat_confset_v{version_number}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(log_text)

    print(f"\nCM Görseli: {cm_path}")
    print(f"Açıklama dosyası: {txt_path}")

# --- Ana akış ---
if __name__ == "__main__":
    version = get_latest_version()
    data_utils_name = f"data_utils_confset_v{version}"
    evaluate_and_plot(version, data_utils_name)
