"""
Evaluation script for skin cancer classification.
"""
import argparse
import yaml
import torch
from data_loader import get_dataloaders, get_test_loader
from preprocessing import get_val_transform
from model import get_model
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, precision_recall_curve, classification_report
import matplotlib.pyplot as plt
import os

# Optionally import utils for metrics, logging, etc.
# from src import utils

def evaluate(config):
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Data transforms
    val_transform = get_val_transform(config['data']['img_size'])

    # Test loader
    test_loader = get_test_loader(
        config['data']['test_dir'],
        test_transform=val_transform,
        batch_size=config['data']['batch_size'],
        num_workers=config['data']['num_workers']
    )

    # Model
    model = get_model(device)
    # Load trained weights from models/
    best_model_path = config['train'].get('save_dir', 'models/') + '/best_model.pth'
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path, map_location=device))
        print(f"Loaded model weights from {best_model_path}")
    else:
        print(f"Model weights not found at {best_model_path}. Evaluation aborted.")
        return

    # Evaluation loop
    model.eval()
    all_labels = []
    all_preds = []
    all_probs = []
    with torch.no_grad():
        for batch in test_loader:
            inputs, labels = batch
            inputs = inputs.to(device)
            labels = labels.to(device).float().view(-1, 1)
            outputs = model(inputs)
            probs = outputs.sigmoid().cpu().numpy().flatten()
            preds = (probs > 0.5).astype(int)
            all_probs.extend(probs.tolist())
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.cpu().numpy().astype(int).flatten().tolist())

    os.makedirs("results", exist_ok=True)

    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Benign", "Malignant"])
    disp.plot(cmap='Blues')
    plt.title("Confusion Matrix (Test Set)")
    plt.savefig("results/confusion_matrix.png")
    plt.close()
    print("Confusion matrix saved to results/confusion_matrix.png")
    print("Confusion Matrix:")
    print(cm)

    # ROC Curve
    fpr, tpr, _ = roc_curve(all_labels, all_probs)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (Test Set)')
    plt.legend(loc="lower right")
    plt.savefig("results/roc_curve.png")
    plt.close()
    print("ROC curve saved to results/roc_curve.png")

    # Precision-Recall Curve
    precision, recall, _ = precision_recall_curve(all_labels, all_probs)
    plt.figure()
    plt.plot(recall, precision, color='blue', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve (Test Set)')
    plt.savefig("results/precision_recall_curve.png")
    plt.close()
    print("Precision-Recall curve saved to results/precision_recall_curve.png")

    # Classification Report
    report = classification_report(all_labels, all_preds, target_names=["Benign", "Malignant"])
    with open("results/classification_report.txt", "w") as f:
        f.write(report)
    print("Classification report saved to results/classification_report.txt")
    print(report)

def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate skin cancer classifier')
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to config file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    evaluate(config)
