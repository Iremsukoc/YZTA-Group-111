import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input
from config import DATA_DIR, CLASS_NAMES

def load_data(image_size=(224, 224), batch_size=128):
    images = []
    labels = []

    for class_name in CLASS_NAMES:
        class_dir = os.path.join(DATA_DIR, class_name)
        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            img = load_img(img_path, target_size=image_size)
            img = img_to_array(img)
            img = preprocess_input(img)
            images.append(img)
            labels.append(class_name)

    images = np.array(images)
    labels = np.array(labels)

    # Label encode
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels_encoded, test_size=0.2, random_state=42, stratify=labels_encoded
    )

    # Data generators
    train_datagen = ImageDataGenerator()
    test_datagen = ImageDataGenerator()

    train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
    test_generator = test_datagen.flow(X_test, y_test, batch_size=batch_size)

    return train_generator, test_generator, X_test, y_test, label_encoder
