import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from src.model.cnn_model import build_cnn_model

def train_model(train_gen, val_gen, input_shape=(128, 128, 1), num_classes=3, epochs=50):
    """
    Modeli oluşturur, sınıf ağırlıklarını hesaplar ve eğitir.

    Args:
        train_gen: Eğitim için ImageDataGenerator
        val_gen: Doğrulama için ImageDataGenerator
        input_shape (tuple): Girdi boyutu (örn. (128,128,1))
        num_classes (int): Çıkış sınıf sayısı
        epochs (int): Eğitim tur sayısı

    Returns:
        model: Eğitilmiş model
        history: Eğitim geçmişi
    """
    model = build_cnn_model(input_shape=input_shape, num_classes=num_classes)

    # Callback'ler
    early = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    lr_reduce = ReduceLROnPlateau(monitor='val_loss', patience=3, factor=0.3, min_lr=1e-6, verbose=1)

    # Sınıf ağırlıkları
    weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_gen.classes),
        y=train_gen.classes
    )
    class_weights = dict(enumerate(weights))

    # Modeli eğit
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        class_weight=class_weights,
        callbacks=[early, lr_reduce],
        verbose=1
    )

    return model, history
