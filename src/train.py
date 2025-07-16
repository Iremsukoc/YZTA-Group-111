import argparse
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
from data_loader import get_dataloaders
from preprocessing import get_train_transform, get_val_transform
from model import get_model
from tqdm import tqdm  
from utils import binary_accuracy
from sklearn.metrics import roc_auc_score, roc_curve

# Optionally import utils for metrics, logging, etc.
# from src import utils

def train(config):
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device} ({torch.cuda.get_device_name(0) if device.type == 'cuda' else 'CPU'})")

    # Data transforms
    train_transform = get_train_transform(config['data']['img_size'])
    val_transform = get_val_transform(config['data']['img_size'])

    # Data loaders
    train_loader, val_loader = get_dataloaders(
        config['data']['train_dir'],
        config['data']['val_dir'],
        train_transform,
        val_transform,
        batch_size=config['data']['batch_size'],
        num_workers=config['data']['num_workers']
    )

    # Model
    model = get_model(device)

    # Loss and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['train']['learning_rate'])

    # Training loop
    best_val_acc = 0.0
    best_model_path = config['train'].get('save_dir', 'models/') + '/best_model.pth'
    patience = 10
    patience_counter = 0
    for epoch in range(config['train']['epochs']):
        model.train()
        running_loss = 0.0
        running_corrects = 0.0
        total = 0
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{config['train']['epochs']}")
        for batch in train_bar:
            inputs, labels = batch
            inputs = inputs.to(device)
            labels = labels.to(device).float().view(-1, 1)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            acc = binary_accuracy(outputs, labels)
            running_corrects += acc.item() * inputs.size(0)
            total += inputs.size(0)
            train_bar.set_postfix(loss=loss.item(), acc=acc.item())
        epoch_loss = running_loss / total
        epoch_acc = running_corrects / total

        # Validation
        model.eval()
        val_loss = 0.0
        val_corrects = 0.0
        val_total = 0
        all_labels = []
        all_probs = []
        with torch.no_grad():
            for batch in val_loader:
                inputs, labels = batch
                inputs = inputs.to(device)
                labels = labels.to(device).float().view(-1, 1)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                acc = binary_accuracy(outputs, labels)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += acc.item() * inputs.size(0)
                val_total += inputs.size(0)
                all_labels.append(labels.cpu())
                all_probs.append(outputs.sigmoid().cpu())
        val_epoch_loss = val_loss / val_total
        val_epoch_acc = val_corrects / val_total
        all_labels = torch.cat(all_labels).numpy()
        all_probs = torch.cat(all_probs).numpy()
        try:
            val_auc = roc_auc_score(all_labels, all_probs)
        except Exception:
            val_auc = float('nan')
        print(f"Epoch {epoch+1} | Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc:.4f} | Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc:.4f} | Val AUC: {val_auc:.4f}")

        # En iyi modeli kaydet
        if val_epoch_acc > best_val_acc:
            best_val_acc = val_epoch_acc
            torch.save(model.state_dict(), best_model_path)
            print(f"Best model saved at epoch {epoch+1} with val acc {val_epoch_acc:.4f}")
            patience_counter = 0
        else:
            patience_counter += 1
            print(f"No improvement in val acc. Patience: {patience_counter}/{patience}")
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch+1} due to no improvement in val acc for {patience} epochs.")
            break

    # TODO: Save final model to models/
    pass

def parse_args():
    parser = argparse.ArgumentParser(description='Train skin cancer classifier')
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to config file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    train(config)
