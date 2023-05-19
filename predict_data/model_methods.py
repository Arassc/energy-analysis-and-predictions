from keras import Model, optimizers
import numpy as np
from keras.callbacks import EarlyStopping
from typing import Tuple

def compile_model(model: Model, learning_rate: int, optimizer="rmsprop", metric="mae")-> Model:
    """
    method that compiles the selected model. \n
    by default the optimizer is RMSprop\n
    by defaul metric ="mae"\n
    """
    opt = optimizers.RMSprop(learning_rate=learning_rate)
    if optimizer == 'adam':
        opt = optimizers.Adam(learning_rate=learning_rate)
    if optimizer == 'nadam':
        opt = optimizers.Nadam(learning_rate=learning_rate)

    model.compile(loss='mse', optimizer=opt, metrics=[metric])

    return model

def train_model(model: Model, X_train: np.ndarray, y_train: np.ndarray,
              patience:int, epochs_num: int, batch_size: int)->  Tuple[Model, dict]:

    # es = EarlyStopping(patience=patience, monitor="val_loss",  mode = "min", start_from_epoch=0,
    #                    restore_best_weights = True)

    es = EarlyStopping(patience=patience, monitor="val_loss")

    #es = EarlyStopping(patience=patience)

    history = model.fit(X_train, np.array(y_train),
            validation_split=0.3,
            batch_size=batch_size,
            epochs=epochs_num,
            verbose=0,
            callbacks=[es])

    return model, history


def evaluate_model(model: Model, X_test: np.ndarray, y_test: np.ndarray) -> list:
    """
    returns loss and mae in a list
    """
    result = model.evaluate(X_test, y_test, verbose = 1)
    return result

def predict_model(model: Model, X_test: np.ndarray) -> np.ndarray:
    y_pred = model.predict(X_test)
    return y_pred
