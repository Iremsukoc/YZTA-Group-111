import numpy as np
import matplotlib.pyplot as plt
import random
from tensorflow.keras.models import load_model
from config import MODEL_PATH, LABEL_ENCODER_PATH, CLASS_NAMES
from data_loader import load_data
import os

def show_random_predictions(model, X_test, y_test, label_encoder, num_images=5):
    indices = random.sample(range(len(X_test)), num_images)
    selected_images = X_test[indices]
    true_labels = y_test[indices]

    pred_probs = model.predict(selected_images)
    pred_labels = np.argmax(pred_probs, axis=1)

    class_names = label_encoder.classes_

    plt.figure(figsize=(15, 5))
    for i in range(num_images):
        img = selected_images[i].astype("uint8")
        true_class = class_names[true_labels[i]]
        pred_class = class_names[pred_labels[i]]

        color = 'green' if true_class == pred_class else 'red'

        plt.subplot(1, num_images, i+1)
        plt.imshow(img)
        plt.title(f"True: {true_class}\nPred: {pred_class}", color=color)
        plt.axis('off')

    plt.tight_layout()
    plt.show()
    #plt.savefig(os.path.join("outputs", "predict_random_results.png"))
    #plt.close()


if __name__ == "__main__":
    # Veriyi yükle (sadece test verisi için)
    _, _, X_test, y_test, label_encoder = load_data()

    # Modeli ve etiket sınıflarını yükle
    model = load_model(MODEL_PATH)

    # Tahminleri göster
    show_random_predictions(model, X_test, y_test, label_encoder)
