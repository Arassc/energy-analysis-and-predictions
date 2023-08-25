
# define folders
import os
import pandas as pd
import numpy as np
from energyanalysis.utils.parameters import COUNTRY,ENERGY_PRICE_FOLDER, PROCESSED_DATA_FOLDER, \
    SPLIT_RADIO, MEMORY_SPLIT_RATIO, STRIDE_RATIO, MODELS_PRICES_FOLDER, \
        ACTIVATION_FUNCTION_1, ACTIVATION_FUNCTION_2, \
        MODEL_LAYER_UNITS_1, MODEL_LAYER_UNITS_2, \
        MODEL_TYPE, REGULARIZER, PENALTY, \
        MODEL_LOSS, OPT_COMPILER, MODEL_METRIC,LEARNING_RATE, \
        PATIENCE, EPOCHS, BATCH_SIZE

from energyanalysis.preprocess_data.load_energy_prices import load_energy_prices_data, \
                            load_energy_prices_from_all_files

from energyanalysis.predict_data.create_simple_train_test_data import get_X_y_scaled_and_splited
from energyanalysis.predict_data.model_factory import ModelMaker

from energyanalysis.visualize_data.plot_price_with_interactive_timestamps import plot_price_with_interactive_timestamps
from energyanalysis.visualize_data.plot_model_history import plot_history
from energyanalysis.visualize_data.plot_predict_vs_test import plot_predict_vs_test


def preprocess_energy_prices():
    #load if data file exist or create data file
    filename_energy_price = PROCESSED_DATA_FOLDER + '/processed_energy_prices.csv'
    energy_prices_df = pd.DataFrame()

    if os.path.isfile(filename_energy_price):
        energy_prices_df = pd.read_csv(filename_energy_price)
        energy_prices_df.set_index('Date', inplace=True)
        print('energy prices file found')
    else :
        energy_prices_df = load_energy_prices_from_all_files(ENERGY_PRICE_FOLDER, COUNTRY)
        print('energy prices file created and processed')
    return energy_prices_df

def split_scale_train_test_data():
    #load or create data
    energy_prices_df = preprocess_energy_prices()

    X_train = np.array([])
    y_train = np.array([])
    X_test  = np.array([])
    y_test  = np.array([])
    scaler = None
    #split train and test data
    if energy_prices_df.empty == False:
        target = energy_prices_df.columns[0]
        scale_range_min = -1
        scale_range_max = 1
        X_train, y_train, X_test, y_test, scaler = get_X_y_scaled_and_splited(energy_prices_df,
                                                                            SPLIT_RADIO,
                                                                            MEMORY_SPLIT_RATIO,
                                                                            STRIDE_RATIO,
                                                                            target,
                                                                            scale_range_min ,
                                                                            scale_range_max)
    else:
        print('energy prices is empty, dataframe could not be loaded')
    return X_train, y_train, X_test, y_test, scaler


def train_energy_prices():
        # split data in train and test and scale it
        X_train, y_train, X_test, y_test, scaler = split_scale_train_test_data()

        if X_train.size!=0:
            # initialize model
            model = ModelMaker()
            model.layer_input_shape = X_train[0].shape
            model.layer_output_shape = y_train.shape[1]
            #model.regularizer = REGULARIZER
            model.custom_penalty = int(PENALTY) if PENALTY!=None else PENALTY
            #model.custom_loss = MODEL_LOSS
            model.custom_optimizer = OPT_COMPILER
            #model.custom_metric = MODEL_METRIC
            model.custom_learning_rate = float(LEARNING_RATE)
            model.custom_patience = int(PATIENCE)
            model.epochs_count = int(EPOCHS)
            model.custom_batch_size = int(BATCH_SIZE)

            model.add_input_layer(int(MODEL_LAYER_UNITS_1), MODEL_TYPE, ACTIVATION_FUNCTION_1)
            model.add_middle_layer(int(MODEL_LAYER_UNITS_1), MODEL_TYPE, ACTIVATION_FUNCTION_1, True)
            model.add_middle_layer(int(MODEL_LAYER_UNITS_2), MODEL_TYPE, ACTIVATION_FUNCTION_2, False)
            model.add_output_layer()
            print('all layers added')

            #compile
            model.compile_model()
            print('model compiled')

            # train model
            model.train_model(X_train, y_train)
            print('model trained')

            # model evaulate
            model.evaluate(X_test, y_test)
            print('model evaluated')

            # save model
            filename = MODEL_TYPE + '_' + MODEL_LAYER_UNITS_1 + '_' + MODEL_LAYER_UNITS_2 + '_' + LEARNING_RATE + '_' + \
                        OPT_COMPILER + '_' + MODEL_METRIC
            model.save_model_and_history(MODELS_PRICES_FOLDER, filename)
            print('model saved')
        else:
            print('train and test data is empty')



def load_model_energy_prices():
    filename = MODEL_TYPE + '_' + MODEL_LAYER_UNITS_1 + '_' + MODEL_LAYER_UNITS_2 + '_' + LEARNING_RATE + '_' + \
                    OPT_COMPILER + '_' + MODEL_METRIC
    (model, history) = ModelMaker.load_model_and_history(MODELS_PRICES_FOLDER, filename)
    return model,history

def evaluate_model_energy_prices():
    # score model
    # save params and results in text file
    pass

def predict_energy_prices():
    X_train, y_train, X_test, y_test, scaler = split_scale_train_test_data()
    predict = np.array([])

    if X_test.size!=0:
        # load model
        filename = 'model_' + MODEL_TYPE + '_' + MODEL_LAYER_UNITS_1 + '_' + MODEL_LAYER_UNITS_2 + '_' + LEARNING_RATE + '_' + \
                        OPT_COMPILER + '_' + MODEL_METRIC + '.h5'

        filename = MODELS_PRICES_FOLDER + '/' + filename
        print(filename)

        if os.path.isfile(filename):
            (model,history) = load_model_energy_prices()
            predict = model.predict(X_test)
        else:
            print( 'model file not found')
    else:
        print('train and test data is empty')

    return predict, y_test, scaler

def plot_test_vs_predict():
    energy_prices_df = preprocess_energy_prices()
    (predict, y_test, scaler) = predict_energy_prices()

    if y_test.size!=0 and predict.size!=0 and energy_prices_df.empty == False:
        y_test_unscaled = scaler.inverse_transform(y_test[:])
        y_pred_unscaled = scaler.inverse_transform(predict)
        fig_title = 'Germany energy prices'
        fig_name = 'fig_' +  MODEL_TYPE + '_' + MODEL_LAYER_UNITS_1 + '_' + MODEL_LAYER_UNITS_2 + '_' + LEARNING_RATE + '_' + \
                        OPT_COMPILER + '_' + MODEL_METRIC
        target = energy_prices_df.columns[0]
        plot_predict_vs_test(energy_prices_df,
                         y_test_unscaled,
                         y_pred_unscaled,
                         fig_title,
                         target,
                         fig_name)


def plot_loss_history():
    pass
