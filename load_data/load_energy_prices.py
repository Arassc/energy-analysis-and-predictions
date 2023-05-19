import numpy as np
import pandas as pd
import functools
import os

def load_csv_file(filename:str, country:str)->list:
    """
    Load file with calulated resolutions of prices in  [€/MWh]\n
    for a selected country.\n
    \n
    Arguments:\n
    - filename: path\\file.format\n
    - country: country name in English\n
    \n
    Returns:\n
    - df_list: a list of dataframes corresponding to the data\n
        belonging to the selected country
    """
    prices_df = pd.read_csv(filename, delimiter=';', decimal=',')
    prices_df.columns = ['Date', 'Start', 'End',
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

    main_cols = [col for col in prices_df.columns if country in col]
    df_list = []
    for col in main_cols:
        print(f'\t{col}')
        condition = prices_df[col] != '-'
        df = prices_df[condition]
        if df.shape[0] != 0 :
            print(f'\t\t df.shape ={df.shape}')
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
            df = df[['Date', col]]
            if df[col].dtypes == 'object':
                df[col] = df[col].str.replace(',', '.')
                df[col] = df[col].astype('float32')
            df_list.append(df)

    return df_list

def average_price_from_merge_df_list(df_list:list, country:str)->pd.DataFrame:
    """
    Merge the dataframes in list and average the price value to get a final price.\n
    The indices of the dataframes should be the same for all dataframes in the list.
    """
    df = functools.reduce(lambda left, right: pd.merge(left, right, on='Date'), df_list)
    len_cols = len(df.columns)
    selected_cols = df.columns[1:len_cols]
    df[f'Average {country} [€/MWh]'] = df[selected_cols].mean(axis=1)
    df = df.drop(columns=selected_cols)
    return df

def concat_df_list(df_list:list, country:str)-> pd.DataFrame:
    """
    Concat dataframes in list. The data frames should have different indices \n
    and therefore each dataframe can be concataned and complete the final dataframe
    """
    for df in df_list:
        df.columns = ['Date', f'{country} [€/MWh]']
    df_final = pd.concat(df_list).sort_index()
    return df_final

def combine_two_dataframes(df_list: list, country: str) -> pd.DataFrame:

    df = pd.DataFrame.empty

    if len(df_list) == 2:
        index_df0 = list(df_list[0].index)
        index_df1 = list(df_list[1].index)

        if index_df0 == index_df1:
            print(f'\taverage df')
            df = average_price_from_merge_df_list(df_list, country)
        else:
            if len(index_df0) == 365:
                print(f'\tdf0 taken')
                df = df_list[0]
            if len(index_df1) == 365:
                print(f'\tdf1 taken')
                df = df_list[0]
            if (len(index_df0) + len(index_df1)) == 365:
                print(f'\tconcat df')
                df = concat_df_list(df_list, country)
    return df


def get_final_price_value(df_list: list, country: str)->pd.DataFrame:

    df = pd.DataFrame.empty

    # df list with length 1
    if len(df_list) == 1:
        df = df_list[0]

    # df list with length 2
    if len(df_list) == 2:
        df = combine_two_dataframes(df_list, country)

    # df list with length 3
    if len(df_list) == 3:
        index_df0 = list(df_list[0].index)
        index_df1 = list(df_list[1].index)
        index_df2 = list(df_list[2].index)

        if index_df0 == index_df1 and index_df2 == index_df1:
            print(f'\tavergae df')
            df = average_price_from_merge_df_list(df_list, country)

        if index_df0 == index_df1 and index_df2 != index_df1:
            print(f'\taverge df0 and df1 and then concat df2')
            df1 = average_price_from_merge_df_list(df_list[0:2])
            df_list2 = [df1, df_list[2]]
            df = combine_two_dataframes(df_list2, country)

        if index_df0 == index_df2 and index_df2 != index_df1:
            print(f'\taverge df0 and df2 and then concat df1')
            df1 = average_price_from_merge_df_list([df_list[0], df_list[2]])
            df_list2 = [df1, df_list[1]]
            df = combine_two_dataframes(df_list2, country)

        if index_df1 == index_df2 and index_df0 != index_df1:
            print(f'\taverge df1 and df2 and then concat df0')
            df1 = average_price_from_merge_df_list([df_list[1], df_list[2]])
            df_list2 = [df1, df_list[0]]
            df = combine_two_dataframes(df_list2, country)
        else:
            print(f'\tconcat dfs')
            df = pd.concat(df_list).sort_index()

    df.columns = ['Date', f'{country} [€/MWh]']
    return df


def load_energy_prices_data(filename:str, country:str)->pd.DataFrame:
    """
    Load energy price data for a specific country using load_csv_file function.\n
    Data is already cleaned up using get_final_price_value function.
    """
    df_list = load_csv_file(filename, country)
    df = get_final_price_value(df_list, country)
    return df

def load_energy_prices_from_all_files(folder:str, country:str)->pd.DataFrame:
    list_files =  os.listdir(folder)
    df_list = []
    for file in list_files:
        print(file)
        filename = os.path.join(folder, file)
        df = load_energy_prices_data(filename, country)
        #print(df.columns)
        df.set_index('Date', inplace=True)
        #print(df.columns)
        df_list.append(df)
        print('\n')

    final_df = pd.concat(df_list).sort_index()
    return final_df
