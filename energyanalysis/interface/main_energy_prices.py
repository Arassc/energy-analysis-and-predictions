
# define folders
from utils.parameters import ENERGY_PRICE_FOLDER
from preprocess_data.load_energy_prices import load_energy_prices_from_all_files

def preprocess_energy_prices():
    country = 'Germany'
    energy_prices_df = load_energy_prices_from_all_files(ENERGY_PRICE_FOLDER, country)

def train_energy_prices():
    #split train and test data
    # initialize model
    # train model
    pass

def evaluate_energy_prices():
    # score model
    # save params and results in text file
    pass

def predict_energy_prices():
    # predict X_test
    # plot train, test and preditc data
    # save plot
