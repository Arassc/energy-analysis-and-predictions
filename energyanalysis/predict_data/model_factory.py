from tensorflow import keras
from keras import Sequential, layers
from keras.regularizers import L1L2, L1, L2
from keras import Model, optimizers, models
import numpy as np
from keras.callbacks import EarlyStopping
from typing import Tuple
import pickle


class ModelMaker(Sequential):
    def __init__(self,*args,**kwargs):
        super(ModelMaker,self).__init__(*args,**kwargs)
        #self.model_name = model_name
        self.layers_info = []
        self.layer_input_shape = None
        self.layer_output_shape = 1
        self.regularizer = None
        self.custom_penalty = 0
        self.custom_optimizer= 'rmsprop'
        self.custom_learning_rate = 0.01
        self.custom_metric = 'mae'
        self.custom_loss = 'mse'
        self.custom_patience = 25
        self.epochs_count = 100
        self.custom_batch_size = 32
        self.custom_validation_split = 0.3

    def add_input_layer(self, units_layer, layer_type, activation_function):

        if self.layer_input_shape != None:
            if layer_type == 'GRU':
                self.add(layers.GRU(units=units_layer,
                                    activation=activation_function,
                                    return_sequences=True,
                                    kernel_regularizer=self.regularizer,
                                    input_shape=self.layer_input_shape))
            if layer_type == 'LSTM':
                self.add(layers.LSTM(units=units_layer,
                                    activation=activation_function,
                                    return_sequences=True,
                                    kernel_regularizer=self.regularizer,
                                    input_shape=self.layer_input_shape))

            if layer_type == 'SimpleRNN':
                self.add(layers.SimpleRNN(units_layer,
                                    activation=activation_function,
                                    input_shape = self.layer_input_shape,
                                    return_sequences=True))

            layer_dict_info = {'units_layer':units_layer,
                               'activation_function': activation_function}
            self.layers_info.append({layer_type:layer_dict_info})

        else:
            print('fail to add input layer set layser_input_shape')

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

    def add_output_layer(self):
        self.add(layers.Dense(units=self.layer_output_shape, activation='linear'))
        layer_dict_info = {'units_layer':self.layer_output_shape, 'activation_function': 'linear'}
        self.layers_info.append({'Dense':layer_dict_info})

    def compile_model(self):
        lr = self.custom_learning_rate
        opt = optimizers.RMSprop(learning_rate=lr)

        if self.custom_optimizer == 'adam':
            opt = optimizers.Adam(learning_rate=lr)
        if self.custom_optimizer == 'nadam':
            opt = optimizers.Nadam(learning_rate=lr)

        self.compile(loss=self.custom_loss, optimizer=opt, metrics=[self.custom_metric])


    def train_model(self, X_train: np.ndarray, y_train: np.ndarray):

        es = EarlyStopping(patience=self.custom_patience, monitor="val_loss")

        self.fit(X_train, np.array(y_train),
                validation_split=self.custom_validation_split,
                batch_size=self.custom_batch_size,
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
        model = models.load_model(filename_model, custom_objects={'ModelMaker': ModelMaker})
        print('model loaded')

        filename_history = foldername + '/history_' + filename + '.pkl'
        history = pickle.load(open(filename_history, 'rb'))
        print('history loaded')
        return model, history
