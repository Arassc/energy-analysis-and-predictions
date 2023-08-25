import numpy as np
import pandas as pd
import os
pd.options.mode.chained_assignment = None
from sklearn.impute import SimpleImputer
from energyanalysis.utils.parameters import ENERGY_COMPANIES_FOLDER, \
                            DICT_COMPANIES_NAME_TO_CHANGE,\
                            LIST_WEIRD_FIRST_RAW

from energyanalysis.preprocess_data.get_energy_sectors import get_energy_sectors_list

def load_company_data_by_sector():
    # load sectors and companies
    sector_keys, sector_df = get_energy_sectors_list()

    # initalize dictionary
    dict_companies = {sector:[] for sector in sector_keys}

    # get folder with company data
    power_plant_list = os.listdir(ENERGY_COMPANIES_FOLDER)
    power_plant_list.sort()

    #group all companies by sector using a dictionary
    for file in power_plant_list:
        if 'Identifier' not in file:
            # load file
            filename = os.path.join(ENERGY_COMPANIES_FOLDER, file)
            df = pd.read_csv(filename, delimiter=';', decimal=',')

            # company name
            company = get_company_name(file)

            # clean df
            df = clean_data(df, company)
            if len(df.columns) == 4:
                df.columns = ['Date', 'Start', 'End', f'{company} [MW]']
                company_sector = get_company_sector(sector_df, company)
                dict_companies[company_sector].append(df)
            else:
                print('not the right number of columns')
                print('not added to dict')

            print('*************************************************************************')
    return dict_companies


def get_company_name(file:str)->str:
    company = file.split('_20')[0]
    #print(f'original name company ={company}.')
    if company in DICT_COMPANIES_NAME_TO_CHANGE.keys():
        company = DICT_COMPANIES_NAME_TO_CHANGE[company]
        #print(f'first change name company ={company}.')

    company = company.replace('_', '-')
    #print(f'last change name company ={company}')
    return company

def get_company_sector(sector_df, company_name):
    condition = sector_df['Name'] == company_name
    company_df = sector_df[condition]
    #print('company df that matches condition:')
    #print(company_df)
    #print('')
    company_sector = company_df['Sector'].values[0]
    return company_sector

def clean_data(df: pd.DataFrame, name) -> pd.DataFrame:

    # get energy generated columns
    cols =  df.columns[3:]

    # remove weird first raw
    df = remove_weird_first_raw(df)

    # change date to datetime type
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')

    for col in cols:
        if 'Unnamed' in col:
             df = df.drop(columns=col)
        else:
            # change str to float
            df = clean_column_dataframe(df, col)

            # check nan values
            df = interpolate_nan_values(df, col)

    # sum multiple energy generated values
    if len(df.columns) > 4:
        df = sum_multiple_energy_values(df, name)
    return df


def remove_weird_first_raw(df: pd.DataFrame) -> pd.DataFrame:
    for text in LIST_WEIRD_FIRST_RAW:
        if text in df['Datum'][0]:
            df = df.iloc[1:,:]
            df.reset_index(drop=True, inplace=True)
    return df


def clean_column_dataframe(df: pd.DataFrame, col:str):
    #print(df.dtypes)
    if df[col].dtype != 'float64':
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].replace('-', np.nan)
        df[col] = df[col].astype('float64')
    #df[col] = df[col]/1000 # maybe that is the true scale, but not sure
    return df


def interpolate_nan_values(df: pd.DataFrame, col: str) -> pd.DataFrame:
    nan_val = (df[col].isna().value_counts()*100/df.shape[0])
    #print('nan_values', nan_val)
    if nan_val[1] <= 30:
        imputer = SimpleImputer(strategy="mean")
        df[col] = imputer.fit_transform(df[[col]])
    else:
        df = df.drop(columns=col)
    return df


def average_multiple_energy_values(df: pd.DataFrame, filename: str):
    new_cols = df.columns[3:]
    df[filename] = df[new_cols].mean(axis=1)
    df = df.drop(columns=new_cols)
    return df


def sum_multiple_energy_values(df: pd.DataFrame, filename: str):
    new_cols = df.columns[3:]
    df[filename] = df[new_cols].sum(axis=1)
    df = df.drop(columns=new_cols)
    return df
