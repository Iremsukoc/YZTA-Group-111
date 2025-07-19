import os
import re
import shutil
import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tqdm import tqdm
from src.config import *
from src.data_utils import get_dataloaders
from src.model import get_model
import matplotlib.pyplot as plt
import mlflow
import mlflow.pytorch

def get_next_model_version():
    SAVE_DIR = "saved_model"
    os.makedirs(SAVE_DIR, exist_ok=True)
    version = 0
    for fname in os.listdir(SAVE_DIR):
        match = re.match(r"best_model_confset_v(\d+)\.pth", fname)
        if match:
            version = max(version, int(match.group(1)))
    return version + 1

def snapshot_data_utils(version):
    src = "src/data_utils.py"
    dst = f"src/data_utils_confset_v{version}.py"
    shutil.copy(src, dst)
    return dst

def train():
    version = get_next_model_version()
    snapshot_path = snapshot_data_utils(version)
    model_save_path = f"saved_model/best_model_confset_v{version}.pth"

    print(f"\nTraining started... (Version v{version})\n")
    print(f"Snapshot taken: {snapshot_path}")
    print(f"Model to be saved: {model_save_path}\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model().to(device)

    class_weights = torch.tensor([1.0, 2.5, 2.8]).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader, val_loader, test_loader = get_dataloaders()

    best_acc = 0.0
    train_losses = []
    val_losses = []

    # MLflow tracking
    mlflow.set_experiment("breast_cancer_classification")
    with mlflow.start_run(run_name=f"v{version}"):
        mlflow.log_param("version", version)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("learning_rate", LEARNING_RATE)
        mlflow.log_param("class_weights", class_weights.cpu().numpy().tolist())
        mlflow.log_param("img_size", IMG_SIZE)
        mlflow.log_param("num_classes", NUM_CLASSES)

        for epoch in range(EPOCHS):
            print(f"Epoch {epoch+1}/{EPOCHS}")
            model.train()
            train_preds, train_labels = [], []
            running_train_loss = 0.0

            for images, labels in tqdm(train_loader):
                images, labels = images.to(device), labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_train_loss += loss.item()

                _, preds = torch.max(outputs, 1)
                train_preds.extend(preds.cpu().numpy())
                train_labels.extend(labels.cpu().numpy())

            avg_train_loss = running_train_loss / len(train_loader)
            train_losses.append(avg_train_loss)

            train_acc = accuracy_score(train_labels, train_preds)
            print(f"Train Accuracy: {train_acc:.4f}")

            # Validation
            model.eval()
            val_preds, val_labels = [], []
            running_val_loss = 0.0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    running_val_loss += loss.item()

                    _, preds = torch.max(outputs, 1)
                    val_preds.extend(preds.cpu().numpy())
                    val_labels.extend(labels.cpu().numpy())

            avg_val_loss = running_val_loss / len(val_loader)
            val_losses.append(avg_val_loss)

            val_acc = accuracy_score(val_labels, val_preds)
            print(f"Val Accuracy: {val_acc:.4f}")

            # MLflow log epoch metrics
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)
            mlflow.log_metric("train_acc", train_acc, step=epoch)
            mlflow.log_metric("val_acc", val_acc, step=epoch)

            if val_acc > best_acc:
                best_acc = val_acc
                torch.save(model.state_dict(), model_save_path)
                print(" Best model saved.")
                # MLflow: Save the best model as an artifact
                mlflow.pytorch.log_model(model, "best_model")

        # --- Loss Plot ---
        os.makedirs("results", exist_ok=True)
        plt.figure(figsize=(8, 5))
        plt.plot(train_losses, label='Train Loss')
        plt.plot(val_losses, label='Validation Loss')
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title(f"Loss Curve – v{version}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        loss_curve_path = f"results/loss_curve_v{version}.png"
        plt.savefig(loss_curve_path)
        plt.close()
        mlflow.log_artifact(loss_curve_path)

        # --- Test Evaluation ---
        print("\nTraining completed. Testing with the best model...")
        model.load_state_dict(torch.load(model_save_path))
        model.eval()

        test_preds, test_labels = [], []
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                test_preds.extend(preds.cpu().numpy())
                test_labels.extend(labels.cpu().numpy())

        print("\n--- Confusion Matrix ---")
        cm = confusion_matrix(test_labels, test_preds)
        print(cm)
        mlflow.log_dict({"confusion_matrix": cm.tolist()}, "confusion_matrix.json")

        print("\n--- Classification Report ---")
        report = classification_report(test_labels, test_preds, target_names=CLASSES, output_dict=True)
        print(classification_report(test_labels, test_preds, target_names=CLASSES))
        mlflow.log_dict(report, "classification_report.json")

        import seaborn as sns
        import numpy as np
        # Confusion Matrix
        plt.figure(figsize=(6,6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=CLASSES, yticklabels=CLASSES)
        plt.xlabel("Tahmin")
        plt.ylabel("Gerçek")
        plt.title(f"Confusion Matrix – v{version}")
        plt.tight_layout()
        confmat_path = f"results/confmat_confset_v{version}.png"
        plt.savefig(confmat_path)
        plt.close()
        mlflow.log_artifact(confmat_path)


if __name__ == "__main__":
    train()
