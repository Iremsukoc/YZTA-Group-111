import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tqdm import tqdm
from config import *
from data_utils import get_dataloaders
from model import get_model


def train():
    print("\n🚀 Eğitim başlıyor...\n")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model().to(device)

    # Class weights: [benign, malignant, normal] — example weights based on imbalance
    class_weights = torch.tensor([1.0, 2.2, 2.8]).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader, val_loader, test_loader = get_dataloaders()

    best_acc = 0.0

    for epoch in range(EPOCHS):
        print(f"Epoch {epoch+1}/{EPOCHS}")
        model.train()
        train_preds, train_labels = [], []

        for images, labels in tqdm(train_loader):
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            train_preds.extend(preds.cpu().numpy())
            train_labels.extend(labels.cpu().numpy())

        train_acc = accuracy_score(train_labels, train_preds)
        print(f"Train Accuracy: {train_acc:.4f}")

        # Validation
        model.eval()
        val_preds, val_labels = [], []
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                val_preds.extend(preds.cpu().numpy())
                val_labels.extend(labels.cpu().numpy())

        val_acc = accuracy_score(val_labels, val_preds)
        print(f"Val Accuracy: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), MODEL_PATH)
            print("✅ En iyi model kaydedildi.")

    # Test Aşaması
    print("\n📊 Eğitim tamamlandı. En iyi model ile test ediliyor...")
    model.load_state_dict(torch.load(MODEL_PATH))
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
    print(confusion_matrix(test_labels, test_preds))

    print("\n--- Classification Report ---")
    print(classification_report(test_labels, test_preds, target_names=CLASSES))


if __name__ == "__main__":
    train()
