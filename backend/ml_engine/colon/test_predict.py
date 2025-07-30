import os
import random
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from tensorflow.keras.preprocessing import image

# ==== KLASÖR YOLLARI ====
TEST_DIRS = {
    'Colon_adenocarcinoma': 'test_split_colon/Colon_adenocarcinoma',
    'Colon_benign_tissue': 'test_split_colon/Colon_benign_tissue'
}

# ==== MODEL VE GÖRSEL AYARLARI ====
IMG_SIZE = (224, 224)
class_names = ['Colon_adenocarcinoma', 'Colon_benign_tissue']

# ==== MODELİ YÜKLE ====
model = load_model('model_cnn.h5')

# ==== TEST GÖRSELLERİNİ RASTGELE SEÇ ====
samples = []
for label, path in TEST_DIRS.items():
    filenames = os.listdir(path)
    chosen = random.sample(filenames, 5)  # Her sınıftan 5 örnek seç
    for file in chosen:
        samples.append((os.path.join(path, file), label))

random.shuffle(samples)
samples = samples[:5]  # Rastgele 5 tanesi alınır

# ==== GÖRSELLEŞTİRME ====
plt.figure(figsize=(15, 5))
for i, (img_path, real_label) in enumerate(samples):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array_exp = np.expand_dims(img_array, axis=0)
    img_pre = img_array_exp / 255.0  # normalize

    pred = model.predict(img_pre)[0]
    pred_label = class_names[np.argmax(pred)]

    plt.subplot(1, 5, i + 1)
    plt.imshow(img_array.astype('uint8'))
    plt.axis('off')
    plt.title(f"Pred: {pred_label}\nReal: {real_label}", fontsize=9)

plt.tight_layout()
plt.show()
