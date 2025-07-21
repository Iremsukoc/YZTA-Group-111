import os
import random
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Modeli yükle
model = load_model("lung_cancer_cnn.h5")

# Parametreler
IMG_SIZE = (128, 128)
COLOR_MODE = "grayscale"
DATA_DIR = "test_split_lung"
LABEL_MAP = {0: 'Benign cases', 1: 'Malignant cases', 2: 'Normal cases'}

# Tüm görselleri klasörlere göre topla
all_image_paths = []
for class_dir in os.listdir(DATA_DIR):
    class_path = os.path.join(DATA_DIR, class_dir)
    if os.path.isdir(class_path):
        images = [os.path.join(class_path, f) for f in os.listdir(class_path)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        all_image_paths.extend(images)

# Rastgele 5 örnek seç
random_images = random.sample(all_image_paths, 5)

# Görselleştir
plt.figure(figsize=(15, 6))
for i, img_path in enumerate(random_images):
    # Görseli yükle
    img = load_img(img_path, target_size=IMG_SIZE, color_mode=COLOR_MODE)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Tahmin
    pred = model.predict(img_array)
    pred_label = LABEL_MAP[np.argmax(pred)]

    # Gerçek etiket (klasör adına göre)
    true_class_name = os.path.basename(os.path.dirname(img_path))

    # Plot
    plt.subplot(1, 5, i + 1)
    plt.imshow(img_array.squeeze(), cmap="gray")
    plt.title(f"True: {true_class_name}\nPred: {pred_label}")
    plt.axis("off")

plt.tight_layout()
plt.show()
