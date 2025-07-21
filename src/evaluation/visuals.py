import matplotlib.pyplot as plt
import numpy as np

def plot_history(history):
    """
    Eğitim geçmişini accuracy ve loss olarak çizer.
    """
    plt.figure(figsize=(14, 6))

    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.title('Accuracy')
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Loss')
    plt.legend()
    plt.show()
