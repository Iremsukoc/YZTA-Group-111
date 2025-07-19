import torch
from model import get_model
from data_utils import get_dataloaders
from train import train
from config import *

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device in use: {device}")

    train_loader, val_loader, test_loader = get_dataloaders()
    model = get_model(NUM_CLASSES).to(device)

    train()
