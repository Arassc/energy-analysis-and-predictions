"""
contributor specific parameters
"""

import os

ENERGY_PRICE_FOLDER = os.environ.get('ENERGY_PRICE_FOLDER')
ENERGY_COMPANIES_FOLDER  =  os.environ.get('ENERGY_COMPANIES_FOLDER')
ENERGY_COMPANY_SECTOR = os.environ.get('ENERGY_COMPANY_SECTOR')
EVALUATION_START_DATE = os.environ.get('EVALUATION_START_DATE')
EVALUATION_END_DATE = os.environ.get('EVALUATION_END_DATE')

MODEL_TARGET = os.environ.get('MODEL_TARGET')
LOCAL_REGISTRY_PATH = os.environ.get('LOCAL_REGISTRY_PATH')
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")


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
#'Braunkohlekraftwerk Lippendorf':'Braunkohlekraftwerk-Lippendorf'

# Heizkraftwerk_Dresden-Nossener_Br_cke' -> weird first raw with
