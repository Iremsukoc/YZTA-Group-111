from tensorflow.keras.callbacks import EarlyStopping

def train_model(model, train_generator, test_generator, epochs=50):
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )

    history = model.fit(
        train_generator,
        validation_data=test_generator,
        epochs=epochs,
        callbacks=[early_stopping]
    )

    return history
