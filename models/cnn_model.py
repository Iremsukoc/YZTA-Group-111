from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adamax

def conv_block(filters, act='relu'):
    block = Sequential()
    block.add(Conv2D(filters, 3, activation=act, padding='same'))
    block.add(Conv2D(filters, 3, activation=act, padding='same'))
    block.add(BatchNormalization())
    block.add(MaxPooling2D())
    return block

def dense_block(units, dropout_rate, act='relu'):
    block = Sequential()
    block.add(Dense(units, activation=act))
    block.add(BatchNormalization())
    block.add(Dropout(dropout_rate))
    return block

def build_cnn_model(config, num_classes):
    img_size = tuple(config['img_size'])
    input_shape = (img_size[0], img_size[1], 3)

    model = Sequential()
    model.add(Conv2D(16, (3,3), padding="same", activation="relu", input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D())
    model.add(conv_block(32))
    model.add(conv_block(64))
    model.add(conv_block(128))
    model.add(conv_block(256))
    model.add(Flatten())
    model.add(dense_block(128, 0.5))
    model.add(dense_block(64, 0.3))
    model.add(dense_block(32, 0.2))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer=Adamax(learning_rate=config['learning_rate']),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model
