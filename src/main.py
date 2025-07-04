import torch
from model import build_model
from data_utils import get_dataloaders
from train import train
from config import *

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Kullanılan cihaz: {device}")

    train_loader, val_loader = get_dataloaders()
    model = build_model(NUM_CLASSES).to(device)

    train(model, train_loader, val_loader, device)
