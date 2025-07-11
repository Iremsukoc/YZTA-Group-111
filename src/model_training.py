import torch
import torch.nn as nn
import torch.optim as optim
from torchmetrics import Accuracy, Precision, Recall

class BrainTumorCNN(nn.Module):
    def __init__(self, num_classes):
        super(BrainTumorCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 28 * 28, 512),  # img_size=224
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def train_model(model, train_loader, epochs, model_path, device):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adamax(model.parameters(), lr=0.001)
    accuracy = Accuracy(task="multiclass", num_classes=4).to(device)
    precision = Precision(task="multiclass", num_classes=4, average='macro').to(device)
    recall = Recall(task="multiclass", num_classes=4, average='macro').to(device)

    history = {'loss': [], 'accuracy': [], 'precision': [], 'recall': []}
    best_acc = 0.0

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        running_acc = 0.0
        running_prec = 0.0
        running_rec = 0.0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_acc += accuracy(outputs, labels).item() * inputs.size(0)
            running_prec += precision(outputs, labels).item() * inputs.size(0)
            running_rec += recall(outputs, labels).item() * inputs.size(0)
            total += inputs.size(0)

        epoch_loss = running_loss / total
        epoch_acc = running_acc / total
        epoch_prec = running_prec / total
        epoch_rec = running_rec / total

        history['loss'].append(epoch_loss)
        history['accuracy'].append(epoch_acc)
        history['precision'].append(epoch_prec)
        history['recall'].append(epoch_rec)

        print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}, "
              f"Precision: {epoch_prec:.4f}, Recall: {epoch_rec:.4f}")

        if epoch_acc > best_acc:
            best_acc = epoch_acc
            torch.save(model.state_dict(), model_path)
            print(f"Saved best model with accuracy: {best_acc:.4f}")

    torch.save(model.state_dict(), model_path.replace('.pth', '_final.pth'))
    return history
