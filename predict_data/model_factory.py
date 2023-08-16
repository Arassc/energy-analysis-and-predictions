from tensorflow import keras
from keras import Sequential, layers
from keras.regularizers import L1L2, L1, L2
import numpy as np


class EnergyModel():
    def __init__(self, model: str, X_train: np.ndarray, y_train: np.ndarray):

        self._learning_rate = 0.01
        self.units_gru_layers = 32
        self.regularizer = None
        self.penalty = 0
        self.activation_function = 'tanh'
        self.opt_compiler = 'adam'
        self.model_metric = 'mae'
        self.patience = 25
        self.epochs = 100
        self.batch_size = 32
        self.optimizer="rmsprop"
        self.model_type = model
        self.model = Sequential()
