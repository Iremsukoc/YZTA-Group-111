import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_generators(df, img_height=128, img_width=128, batch_size=16, color_mode='grayscale'):
    """
    Verilen DataFrame'den train/val/test split yapar ve ImageDataGenerator nesneleri döndürür.
    """
    # 1. Ayrım
    train_df, temp_df = train_test_split(df, test_size=0.3, stratify=df['label'], random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df['label'], random_state=42)

    # 2. Preprocessing ayarları
    datagen = ImageDataGenerator(rescale=1./255)

    # 3. Generator'lar
    train_gen = datagen.flow_from_dataframe(
        dataframe=train_df,
        x_col='filename',
        y_col='label',
        target_size=(img_height, img_width),
        color_mode=color_mode,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True
    )

    val_gen = datagen.flow_from_dataframe(
        dataframe=val_df,
        x_col='filename',
        y_col='label',
        target_size=(img_height, img_width),
        color_mode=color_mode,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=False
    )

    test_gen = datagen.flow_from_dataframe(
        dataframe=test_df,
        x_col='filename',
        y_col='label',
        target_size=(img_height, img_width),
        color_mode=color_mode,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=False
    )

    return train_gen, val_gen, test_gen
