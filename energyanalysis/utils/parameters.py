"""
contributor specific parameters
"""

import os

#parameters
COUNTRY = os.environ.get('COUNTRY')
SPLIT_RADIO = 0.9
MEMORY_SPLIT_RATIO = 0.011
STRIDE_RATIO = 0.2
ACTIVATION_FUNCTION_1 = os.environ.get('ACTIVATION_FUNCTION_1')
ACTIVATION_FUNCTION_2 = os.environ.get('ACTIVATION_FUNCTION_2')
MODEL_LAYER_UNITS_1 = os.environ.get('MODEL_LAYER_UNITS_1')
MODEL_LAYER_UNITS_2 = os.environ.get('MODEL_LAYER_UNITS_2')
MODEL_TYPE = os.environ.get('MODEL_TYPE')
MODEL_LOSS = os.environ.get('MOLDE_LOSS')
OPT_COMPILER = os.environ.get('OPT_COMPILER')
MODEL_METRIC = os.environ.get('MODEL_METRIC')
LEARNING_RATE = os.environ.get('LEARNING_RATE')
PATIENCE = os.environ.get('PATIENCE')
EPOCHS = os.environ.get('EPOCHS')
BATCH_SIZE = os.environ.get('BATCH_SIZE')
REGULARIZER = os.environ.get('REGULARIZER')
PENALTY = os.environ.get('PENALTY ')



# folders
ENERGY_PRICE_FOLDER = os.environ.get('ENERGY_PRICE_FOLDER')
ENERGY_COMPANIES_FOLDER  =  os.environ.get('ENERGY_COMPANIES_FOLDER')
ENERGY_COMPANY_SECTOR = os.environ.get('ENERGY_COMPANY_SECTOR')
EVALUATION_START_DATE = os.environ.get('EVALUATION_START_DATE')
EVALUATION_END_DATE = os.environ.get('EVALUATION_END_DATE')
GREEN_ENERGIES_FOLDER = os.environ.get('GREEN_ENERGIES_FOLDER')
RESULTS = os.environ.get('RESULTS')
PROCESSED_DATA_FOLDER  = os.environ.get('PROCESSED_DATA_FOLDER')
MODELS_PRICES_FOLDER = os.environ.get('MODELS_PRICES_FOLDER')

# ML flow
MODEL_TARGET = os.environ.get('MODEL_TARGET')
LOCAL_REGISTRY_PATH = os.environ.get('LOCAL_REGISTRY_PATH')
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")


# Energy prices
PRICE_COLUMN_TRANSLATED_EN = ['Date', 'Start', 'End',
         'Germany/Luxembourg [€/MWh]',
         '∅ residents Germany/Luxembourg [€/MWh]',
         'Belgium [€/MWh]',
         'Denmark 1 [€/MWh]',
         'Denmark 2 [€/MWh]',
         'France [€/MWh]',
         'Netherlands [€/MWh]',
         'Norway 2 [€/MWh]',
         'Austria [€/MWh]',
         'Poland [€/MWh]',
         'Sweden 4 [€/MWh]',
         'Switzerland [€/MWh]',
         'Czech Republic [€/MWh]',
         'Germany/Luxembourg/Austria [€/MWh]',
         'Italy (North) [€/MWh]',
         'Slovenia [€/MWh]',
         'Hungary [€/MWh]']


# param dates
WINTER_START = '-12-21 1:00:00'
WINTER_END = '-03-20 00:00:00'

SPRING_START = '-03-21 1:00:00'
SPRING_END = '-06-20 00:00:00'

SUMMER_START = '-06-21 1:00:00'
SUMMER_END = '-09-21 00:00:00'

AUTUM_START = '-09-22 1:00:00'
AUTUM_END = '-12-20 00:00:00'

SEASONS_DICT = {'Winter' : [WINTER_START, WINTER_END],
                'Spring' : [SPRING_START, SPRING_END],
                'Summer' : [SUMMER_START, SUMMER_END],
                'Autum' : [AUTUM_START, AUTUM_END]}

# Power Plants
LIST_COMA_DELIMITER_FILES = ['Abwinden-Asten', 'Duisburg_Heizkraftwerk_III', 'Duisburg_Ruhrort']# use coma in delimiter

DICT_COMPANIES_NAME_TO_CHANGE = {'Altenw_rth': 'Altenwoerth',
                                 'Heizkraftwerk_Altbach_Deizisau' : 'Heizkraftwerk-Altbach/Deizisau',
                                 'GKH_St_cken' : 'GKH-Stoecken',
                                 'H_usling':'Haeusling',
                                 'S_ckingen':'Saeckingen',
                                 'Ro_hag':'Rosshag',
                                 'M_nchen_Nord_2':'Muenchen-Nord-2',
                                 'Linz-S_d_Fernheizkraftwerk':'Linz-Sued-Fernheizkraftwerk',
                                 'Gro_kraftwerk_Mannheim': 'Grosskraftwerk-Mannheim',
                                 'K_stenkraftwerk_K.I.E.L.':'Kuestenkraftwerk-K.I.E.L',
                                 'Heizkraftwerk_R_merbr_cke': 'Heizkraftwerk-Roemerbruecke',
                                 'Heizkraftwerk_Dresden-Nossener_Br_cke': 'Heizkraftwerk-Dresden-Nossener-Bruecke',
                                 'Heizkraftwerk_M_nchen_S_d_GUD1_': 'Heizkraftwerk-Muenchen-Sued-GUD1',
                                 'Heizkraftwerk_M_nchen_S_d_GUD2': 'Heizkraftwerk-Muenchen-Sued-GUD2',
                                 'Heizkraftwerk_West__Frankfurt_': 'Heizkraftwerk-West-(Frankfurt)',
                                 'Kraftwerk_BASF_Ludwigshafen_S_d' : 'Kraftwerk_BASF_Ludwigshafen_Sued',
                                 'Kraftwerk_J_nschwalde' : 'Kraftwerk-Jaenschwalde',
                                 'Kraftwerk_K_htai' : 'Kraftwerk-Kuehtai',
                                 'Kraftwerk_Mittelsb_ren' : 'Kraftwerk-Mittelsbueren',
                                 'Niederau_em' : 'Niederaussem',
                                 'Restm_ll-Heizkraftwerk_Stuttgart-M_nster' : 'Restmuell-Heizkraftwerk-Stuttgart-Muenster',
                                 'Thei_' : 'Theiss',
                                 'Trianel_Kohlekraftwerk_L_nen' : 'Trianel-Kohlekraftwerk-Luenen',
                                 'V_lklingen' : 'Voelklingen',
                                 'Vorarlberger_Illwerke_AG__Obervermuntwerk_II_' : 'Vorarlberger-Illwerke-AG-"Obervermuntwerk-II"',
                                 'Vorarlberger_Illwerke_AG__Rellswerk_' : 'Vorarlberger-Illwerke-AG-"Rellswerk"'
                                 }

LIST_WEIRD_FIRST_RAW = ['[MW] Berechnete Auflösungen', '(3 GT + 1 DT, Sammelschiene)', 'GT 1, GT 2, DT 1 [MW] Berechnete Auflösungen']
