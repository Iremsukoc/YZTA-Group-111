from src.model_training import BrainTumorCNN
from src.data_preprocessing import create_data_loaders
from src.evaluation import evaluate_model
import torch

if __name__ == "__main__":  

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = BrainTumorCNN(num_classes=4).to(device)
    model.load_state_dict(torch.load("models/saved_model.pth"))  # or saved_model_final.pth
    model.eval()

    _, test_loader = create_data_loaders("data", img_size=224, batch_size=32)
    evaluate_model(model, test_loader, device)
