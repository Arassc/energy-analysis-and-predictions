
import pandas as pd
from utils.parameters import SEASONS_DICT
from datetime import datetime

def get_seasonal_power_avg_per_hour(df:pd.DataFrame, energy_sector:str, date_start='2018-01-01 01:00:00', date_end='2018-03-21 01:00:00')-> pd.DataFrame:
    df = df.loc[(df['Timestamp'] >= date_start) & (df['Timestamp'] <= date_end)]
    df.set_index('Timestamp', inplace=True)
    timestamp_list = []
    power_list = []
    for i in range(1,25):
        if i < 10:
            i = f'0{i}'
        if i == 24:
            i = '00'
        timestamp = f'{i}:00:00'
        test = df.between_time(timestamp, timestamp)
        timestamp_list.append(timestamp)
        power_list.append(test.mean(axis=0).values[0])

    seasonal = {'Timestamp':timestamp_list, energy_sector:power_list}
    seasonal_df = pd.DataFrame(seasonal, columns=['Timestamp', energy_sector])
    return seasonal_df

def get_dict_of_seasons(df_all:pd.DataFrame, energy_sector:str)-> dict:
    min_year = df_all['Timestamp'].min()
    max_year = df_all['Timestamp'].max()
    years = list(df_all['Timestamp'].dt.year.value_counts().index)
    seasons_data = {}

    for year in years:

        for key, values in SEASONS_DICT.items():

            star_val = str(year) + values[0]
            end_val =  str(year) + values[1]
            date_start =  datetime.strptime(star_val, '%Y-%m-%d %H:%M:%S')
            date_end =  datetime.strptime(end_val, '%Y-%m-%d %H:%M:%S')

            if date_start < max_year:

                date_start =  star_val if date_start >= min_year else min_year
                date_end = end_val if date_end <= max_year else max_year

                print('date_start', date_start)
                print('date_end', date_end)

                seasonal_df = get_seasonal_power_avg_per_hour(df_all, energy_sector, date_start, date_end)
                seasons_data[f'{key}_{year}'] = seasonal_df

    return seasons_data
