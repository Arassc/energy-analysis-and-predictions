
import pandas as pd
from energyanalysis.utils.parameters import SEASONS_DICT
from datetime import datetime

def get_dict_of_seasons(df_all:pd.DataFrame, energy_sector:str) -> dict:
    min_year = df_all['Timestamp'].min()
    max_year = df_all['Timestamp'].max()
    years = list(df_all['Timestamp'].dt.year.value_counts().index)
    years.sort()
    seasons_data = {}
    print('min_year', min_year)
    print('max_year', max_year)
    print(years)

    for year in years:

        for key, values in SEASONS_DICT.items():
            (date_start, date_end) = get_start_end_dates(year, values, key)

            if date_start < max_year:
                print(f'{key} date_start = {date_start}')
                print(f'{key} date_end = {date_end}')

                seasonal_df = get_seasonal_power_avg_per_hour(df_all, energy_sector, date_start, date_end)
                print('seasonal_df')
                print(seasonal_df.head(2))
                seasons_data[f'{key}_{year}'] = seasonal_df
            print('\n')

    return seasons_data

def get_start_end_dates(year:str, season_values:list, season_key:str) -> tuple:
    start_val = str(year) + season_values[0]
    end_val =  str(year) + season_values[1]

    if season_key == 'Winter':
        start_val = str(year-1) + season_values[0]
        print('new start val', start_val)

    date_start =  datetime.strptime(start_val, '%Y-%m-%d %H:%M:%S')
    date_end =  datetime.strptime(end_val, '%Y-%m-%d %H:%M:%S')
    return (date_start, date_end)


def get_seasonal_power_avg_per_hour(df:pd.DataFrame, energy_sector:str,
                                    date_start='2018-01-01 01:00:00',
                                    date_end='2018-03-21 01:00:00')-> pd.DataFrame:

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

    seasonal = {'Timestamp':timestamp_list, energy_sector + ' [MWh]' : power_list}
    seasonal_df = pd.DataFrame(seasonal, columns=['Timestamp', energy_sector + ' [MWh]'])
    return seasonal_df
