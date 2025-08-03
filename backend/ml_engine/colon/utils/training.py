from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def train_model(model, train_gen, val_gen, config):
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1)

    history = model.fit(
        train_gen,
        epochs=config['epochs'],
        validation_data=val_gen,
        callbacks=[early_stop, reduce_lr],
        shuffle=True
    )

    return history
