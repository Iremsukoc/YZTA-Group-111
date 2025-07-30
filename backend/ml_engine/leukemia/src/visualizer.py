import random
import matplotlib.pyplot as plt
import numpy as np
from config import OUTPUT_DIR, CLASS_NAMES

def plot_training_history(history):
    # Accuracy
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/accuracy.png")
    plt.close()

    # Loss
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/loss.png")
    plt.close()
