from tensorflow import keras
from keras import Sequential, layers
from keras.regularizers import L1L2, L1, L2
from keras import Model, optimizers, models
import numpy as np
from keras.callbacks import EarlyStopping
from typing import Tuple
import pickle


class ModelMaker(Sequential):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
        self.layers_info = []
        self.input_shape = None
        self.output_shape = 1
        self.regularizer = None
        self.penalty = 0
        self.optimizer_compiler = 'rmsprop'
        self.learning_rate = 0.01
        self.metric = 'mae'
        self.loss = 'mse'
        self.patience = 25
        self.epochs_count = 100
        self.batch_size = 32
        self.validation_split = 0.3

    def add_input_layer(self, units_layer, layer_type, activation_function):
        if self.input_shape != None:
            if layer_type == 'GRU':
                self.add(layers.GRU(units=units_layer,
                                    activation=activation_function,
                                    return_sequences=True,
                                    kernel_regularizer=self.regularizer,
                                    input_shape=self.input_shape))
            if layer_type == 'LSTM':
                self.add(layers.LSTM(units=units_layer,
                                    activation=activation_function,
                                    return_sequences=True,
                                    kernel_regularizer=self.regularizer,
                                    input_shape=self.input_shape))

            if layer_type == 'SimpleRNN':
                self.add(layers.SimpleRNN(units_layer,
                                    activation=activation_function,
                                    input_shape = self.input_shape,
                                    return_sequences=True))

            layer_dict_info = {'units_layer':units_layer,
                               'activation_function': activation_function}
            self.layers_info.append({layer_type:layer_dict_info})

    def add_middle_layer(self, units_layer, layer_type,
                         activation_function, return_sequences):
        if layer_type == 'GRU':
            self.add(layers.GRU(units_layer,
                        return_sequences=return_sequences,
                        activation=activation_function))
        if layer_type == 'LSTM':
            self.add(layers.LSTM(units_layer,
                        return_sequences=return_sequences,
                        activation=activation_function))
        if layer_type == 'SimpleRNN':
            self.add(layers.SimpleRNN(units_layer,
                                      return_sequences=return_sequences,
                                      activation=activation_function))

        layer_dict_info = {'units_layer':units_layer, 'activation_function': activation_function}
        self.layers_info.append({layer_type:layer_dict_info})

    def add_output_layer(self, output_shape):
        self.add(layers.Dense(units=output_shape, activation='linear'))
        layer_dict_info = {'units_layer':output_shape, 'activation_function': 'linear'}
        self.layers_info.append({'Dense':layer_dict_info})

    def compile_model(self):
        """
        method that compiles the selected model. \n
        by default the optimizer is RMSprop\n
        by defaul metric ="mae"\n
        """
        lr = self.learning_rate
        opt = optimizers.RMSprop(learning_rate=lr)
        if self.optimizer == 'adam':
            opt = optimizers.Adam(learning_rate=lr)
        if self.optimizer == 'nadam':
            opt = optimizers.Nadam(learning_rate=lr)

        self.compile(loss=self.loss, optimizer=opt, metrics=[self.metric])



    def train_model(self, X_train: np.ndarray, y_train: np.ndarray):

        # es = EarlyStopping(patience=patience, monitor="val_loss",  mode = "min", start_from_epoch=0,
        #                    restore_best_weights = True)

        es = EarlyStopping(patience=self.patience, monitor="val_loss")

        self.fit(X_train, np.array(y_train),
                validation_split=self.validation_split,
                batch_size=self.batch_size,
                epochs=self.epochs_count,
                verbose=0,
                callbacks=[es])

    def save_model_and_history(self, foldername:str, filename:str):
        filename_model = foldername + '/model_' + filename + '.h5'
        self.save(filename_model)

        filename_history = foldername + '/history_' + filename + '.pkl'
        with open(filename_history, 'wb') as file_pickle:
            pickle.dump(self.history, file_pickle)

    @classmethod
    def load_model_and_history(cls, foldername:str, filename:str):
        filename_model = foldername + '/model_' + filename + '.h5'
        #model =  models.load_model(filename_model)
        cls = models.load_model(filename_model)
        filename_history = foldername + '/history_' + filename + '.pkl'
        history = pickle.load(open(filename_history, 'rb'))
        return cls, history


# example
# model = CustomSequential(num_classes)
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(x_train, y_train, epochs=10, batch_size=32)

#TODO: check it is bettwer to class methods/@methods, the same wiht parameter/class atributes
#TODO: attribust of sequential models
