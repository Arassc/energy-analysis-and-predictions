import pandas as pd

from energy_app.utils.parameters import ENERGY_COMPANY_SECTOR

def get_energy_sectors_list()-> tuple:
    sector_df = load_company_sectors()
    sector_keys = list(sector_df['Sector'].value_counts().index)
    # print(sector_keys)
    sector_keys.sort()
    return sector_keys, sector_df

def load_company_sectors()-> pd.DataFrame:
    energy_company_sectors = pd.read_csv(ENERGY_COMPANY_SECTOR ,delimiter = ",", encoding = "utf-8")
    energy_company_sectors = energy_company_sectors[['Name', 'Energy_Source']]
    energy_company_sectors.columns = ['Name', 'Sector']
    energy_company_sectors = energy_company_sectors.dropna()
    energy_company_sectors = energy_company_sectors.drop_duplicates()
    energy_company_sectors['Sector'] = energy_company_sectors['Sector'].map(lambda x: str(x)[:-1])
    energy_company_sectors['Name'] = energy_company_sectors['Name'].map(lambda x: str(x)[:-1])
    energy_company_sectors['Name'] = energy_company_sectors['Name'].map(lambda x: str(x).replace(' ', '-'))
    energy_company_sectors['Name'] = energy_company_sectors['Name'].map(lambda x: str(x).replace('_', '-'))
    return energy_company_sectors
