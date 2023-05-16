
from tensorflow import keras
from keras import Sequential, optimizers
import numpy as np
from keras.callbacks import EarlyStopping
from typing import Tuple

def compile_model(model: Sequential, learning_rate: int, optimizer="rmsprop", metric="mae")-> Sequential:
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

def fit_model(model: Sequential, X_train: np.ndarray, y_train: np.ndarray,
              patience:int, epochs_num: int, batch_size: int)->  Tuple[Sequential, dict]:

    es = EarlyStopping(patience=patience, monitor="val_loss",  mode = "min", start_from_epoch=0,
                       restore_best_weights = True)

    #es = EarlyStopping(patience=patience)

    history = model.fit(X_train, np.array(y_train),
            validation_split=0.3,
            batch_size=batch_size,
            epochs=epochs_num,
            verbose=1,
            callbacks=[es])

    return model, history


def evaluate_model(model: Sequential, X_test: np.ndarray, y_test: np.ndarray) -> list:
    """
    returns loss and mae in a list
    """
    result = model.evaluate(X_test, y_test, verbose = 1)
    return result

def predict_model(model: Sequential, X_test: np.ndarray) -> np.ndarray:
    y_pred = model.predict(X_test)
    return y_pred
