import os
import yaml
import torch
from data_preprocessing import create_data_loaders, plot_class_distribution
from model_training import BrainTumorCNN, train_model
from evaluation import evaluate_model, plot_training_history

def main():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Parameteres
    data_dir = config['data_dir']
    img_size = config['img_size']
    batch_size = config['batch_size']
    epochs = config['epochs']
    model_path = config['model_path']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Class distribution
    plot_class_distribution(os.path.join(data_dir, 'Training'))

    # Create data loaders
    train_loader, test_loader = create_data_loaders(data_dir, img_size, batch_size)

    # Create model
    model = BrainTumorCNN(num_classes=4).to(device)

    # Train model
    history = train_model(model, train_loader, epochs, model_path, device)

    plot_training_history(history, save_path='results/training_plot.png')

    evaluate_model(model, test_loader, device)

if __name__ == "__main__":
    main()
