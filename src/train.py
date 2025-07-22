from data_loader import load_data
from model_builder import build_model
from trainer import train_model
from evaluator import evaluate_model
from visualizer import plot_training_history
from config import MODEL_PATH, LABEL_ENCODER_PATH
import numpy as np

from tensorflow.keras.models import save_model

def main():
    # Veriyi yükle
    print("Loading data...")
    train_gen, test_gen, X_test, y_test, label_encoder = load_data()

    # Modeli oluştur
    print("Building model...")
    model = build_model(num_classes=len(label_encoder.classes_))

    # Eğitimi başlat
    print("Training model...")
    history = train_model(model, train_gen, test_gen)

    # Modeli ve label encoder'ı kaydet
    print("Saving model...")
    save_model(model, MODEL_PATH)
    np.save(LABEL_ENCODER_PATH, label_encoder.classes_)

    # Metrikleri yazdır
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test, label_encoder)

    # Grafik üret
    print("Plotting training history...")
    plot_training_history(history)

    print("Training complete.")

if __name__ == "__main__":
    main()
