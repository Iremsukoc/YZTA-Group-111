from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def build_cnn_model(input_shape=(128, 128, 1), num_classes=3):
    """
    CNN mimarisini tanımlar ve derlenmiş model döndürür.

    Args:
        input_shape (tuple): Görüntü boyutu ve kanal bilgisi
        num_classes (int): Çıkış katmanındaki sınıf sayısı

    Returns:
        model (tf.keras.Model): Derlenmiş CNN modeli
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model
