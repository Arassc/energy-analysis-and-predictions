import numpy as np
import pandas as pd
import os
pd.options.mode.chained_assignment = None

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
        #print(filename)
        # load file
        filename = os.path.join(ENERGY_COMPANIES_FOLDER, file)
        df = pd.read_csv(filename, delimiter=',', decimal='.')
        # TODO average data if there is more than one column
        # append df to
        company = file.split('_')[0]
        condition = sector_df['Name'].str.contains(company)
        sector_df[condition]
        company_df =  sector_df[condition]
        company_sector = company_df['Energy_Source'].values[0]
        dict_companies[company_sector].append(df)

    return dict_companies
