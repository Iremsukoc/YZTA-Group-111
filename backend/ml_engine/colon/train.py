import yaml
from utils.data_loader import get_data_generators
from utils.training import train_model
from utils.evaluation import plot_training_history, evaluate_model
from models.cnn_model import build_cnn_model
from models.efficientnet_model import build_efficientnet_model

def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    train_gen, val_gen, test_gen, class_names = get_data_generators(config)

    if config['model_type'] == "cnn":
        model = build_cnn_model(config, len(class_names))
        model_name = "model_cnn.h5"
    elif config['model_type'] == "efficientnet":
        model = build_efficientnet_model(config, len(class_names))
        model_name = "model_efficientnet.h5"
    else:
        raise ValueError("model_type must be 'cnn' or 'efficientnet'")

    history = train_model(model, train_gen, val_gen, config)
    plot_training_history(history)
    evaluate_model(model, test_gen, class_names)
    model.save(model_name)
    print(f"Model saved as: {model_name}")

if __name__ == "__main__":
    main()
