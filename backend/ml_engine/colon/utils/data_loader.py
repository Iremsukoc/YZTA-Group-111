import os
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def loading_the_data(data_dir):
    filepaths = []
    labels = []

    folds = [f for f in os.listdir(data_dir) if not f.startswith('.')]
    for fold in folds:
        foldpath = os.path.join(data_dir, fold)
        filelist = [f for f in os.listdir(foldpath) if not f.startswith('.')]
        for file in filelist:
            fpath = os.path.join(foldpath, file)
            filepaths.append(fpath)
            labels.append(fold)

    df = pd.DataFrame({'filepaths': filepaths, 'labels': labels})
    return df

def get_data_generators(config):
    df = loading_the_data(config['data_dir'])

    train_df, ts_df = train_test_split(df, train_size=0.8, shuffle=True, random_state=42)
    valid_df, test_df = train_test_split(ts_df, train_size=0.5, shuffle=True, random_state=42)

    batch_size = config['batch_size']
    img_size = tuple(config['img_size'])

    tr_gen = ImageDataGenerator(rescale=1./255)
    ts_gen = ImageDataGenerator(rescale=1./255)

    train_gen = tr_gen.flow_from_dataframe(
        train_df,
        x_col='filepaths',
        y_col='labels',
        target_size=img_size,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True
    )

    valid_gen = ts_gen.flow_from_dataframe(
        valid_df,
        x_col='filepaths',
        y_col='labels',
        target_size=img_size,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True
    )

    test_gen = ts_gen.flow_from_dataframe(
        test_df,
        x_col='filepaths',
        y_col='labels',
        target_size=img_size,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=False
    )

    class_names = list(train_gen.class_indices.keys())
    return train_gen, valid_gen, test_gen, class_names
