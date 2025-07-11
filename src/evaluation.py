import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import torch
import numpy as np
from torchmetrics import Accuracy, Precision, Recall
import torch.nn as nn  

def plot_training_history(history, save_path):
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history['accuracy'], label='Train Accuracy')
    plt.plot(history['loss'], label='Train Loss')
    plt.title('Model Accuracy and Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history['precision'], label='Train Precision')
    plt.plot(history['recall'], label='Train Recall')
    plt.title('Model Precision and Recall')
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def evaluate_model(model, test_loader, device):
    model.eval()
    criterion = nn.CrossEntropyLoss()
    accuracy = Accuracy(task="multiclass", num_classes=4).to(device)
    precision = Precision(task="multiclass", num_classes=4, average='macro').to(device)
    recall = Recall(task="multiclass", num_classes=4, average='macro').to(device)

    test_loss = 0.0
    test_acc = 0.0
    test_prec = 0.0
    test_rec = 0.0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            test_loss += loss.item() * inputs.size(0)
            test_acc += accuracy(outputs, labels).item() * inputs.size(0)
            test_prec += precision(outputs, labels).item() * inputs.size(0)
            test_rec += recall(outputs, labels).item() * inputs.size(0)
            total += inputs.size(0)

            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    test_loss /= total
    test_acc /= total
    test_prec /= total
    test_rec /= total

    print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.4f}, "
          f"Test Precision: {test_prec:.4f}, Test Recall: {test_rec:.4f}")

    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, target_names=test_loader.dataset.classes))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(all_labels, all_preds)
    class_names = test_loader.dataset.classes
    print("Raw Confusion Matrix:\n", cm)

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        linewidths=0.5,
        linecolor='gray',
        annot_kws={"size": 14},
        square=True
    )
    plt.title('Confusion Matrix', fontsize=16)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(rotation=0, fontsize=12)
    plt.tight_layout()
    plt.savefig("results/confusion_matrix.png")
    plt.show()
