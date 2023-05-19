#import tensorflow as tf
from tensorflow import keras
from keras import Sequential, layers
from keras.regularizers import L1L2, L1, L2
import numpy as np

def load_gru_model(X_train: np.ndarray, y_train: np.ndarray,
                   activation_function: str,
                   regularizer=None, penalty=0.0) -> Sequential:
    """
    Initialize a GRU RNN model with a specific regularizer\n
    The regularizer is None by default.\\
    If the regularizer is not none it can have the following values:\\
    'L1L2', 'L1', and 'L2' and one must set its corresponding penalty
    """

    # RNN architecture

    model = Sequential()

    ## Regularizer
    if regularizer == 'L1L2':
        regularizer = L1L2(l1=penalty, l2=penalty)
    if regularizer == 'L1':
         regularizer= L1(penalty)
    if regularizer == 'L2':
        regularizer= L2(penalty)

    ## Recurrent Layer
    model.add(layers.GRU(units=32,
                          activation=activation_function,
                          return_sequences=True,
                          kernel_regularizer=regularizer,
                          input_shape = X_train[0].shape)
                          )

    model.add(layers.GRU(units=32,
                        return_sequences=True,
                        activation=activation_function))

    model.add(layers.GRU(units=32, activation="sigmoid"))

    ## Predictive Dense Layers
    output_shape = y_train.shape[1]
    model.add(layers.Dense(units=output_shape, activation='linear'))
    return model
