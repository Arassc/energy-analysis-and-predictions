import numpy as np
import pandas as pd
import os
pd.options.mode.chained_assignment = None
from sklearn.impute import SimpleImputer
from utils.parameters import ENERGY_COMPANIES_FOLDER, ENERGY_COMPANY_SECTOR

def load_company_sectors()-> pd.DataFrame:
    energy_sectors = pd.read_csv(ENERGY_COMPANY_SECTOR ,delimiter = ",", encoding = "utf-8")
    energy_sectors = energy_sectors[['Name', 'Energy_Source']]
    energy_sectors.columns = ['Name', 'Sector']
    energy_sectors = energy_sectors.dropna()
    energy_sectors['Sector'] = energy_sectors['Sector'].map(lambda x: str(x)[:-1])
    return energy_sectors

def load_company_data_by_sector():
    # load sectors and companies
    sector_df = load_company_sectors()
    sector_keys = list(sector_df['Sector'].value_counts().index)
    sector_keys = [sector[:-1] for sector in sector_keys]
    sector_keys.sort()

    # initalize dictionary
    dict_companies = {sector:[] for sector in sector_keys}

    # get folder with company data
    power_plant_list = os.listdir(ENERGY_COMPANIES_FOLDER)
    power_plant_list.sort()
    for file in power_plant_list:
        if 'Identifier' in file:
            power_plant_list.remove(file)

    for file in power_plant_list:
        #print(filename)
        # load file
        filename = os.path.join(ENERGY_COMPANIES_FOLDER, file)
        df = pd.read_csv(filename, delimiter=';', decimal='.')
        # clean df
        df = clean_data(df)
        company = file.split('_')[0]
        condition = sector_df['Name'].str.contains(company)
        sector_df[condition]
        company_df =  sector_df[condition]
        company_sector = company_df['Energy_Source'].values[0]
        dict_companies[company_sector].append(df)

    return dict_companies


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cols =  df.columns[3:]
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    for col in cols:
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].replace('-', np.nan)
        df[col] = df[col].astype('float32')
        nan_val = (df[col].isna().value_counts()*100/df.shape[0])
        if nan_val[1] <= 30:
            imputer = SimpleImputer(strategy="mean")
            df[col] = imputer.fit_transform(df[[col]])
        else:
            df = df.drop(col)

    if len(df.columns) > 4:
        df['avg energy [MW]'] = df[cols].mean(axis=1)
        df = df.drop(cols)

    return df
