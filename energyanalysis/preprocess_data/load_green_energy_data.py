from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import numpy as np
import pandas as pd
import os
pd.options.mode.chained_assignment = None
from energyanalysis.utils.parameters import GREEN_ENERGIES_FOLDER, PROCESSED_DATA_FOLDER
from energyanalysis.preprocess_data.load_energy_produced_by_companies import clean_column_dataframe
DICT_GREEN_ENERGIES = {'Solar':1004068, 'Wind_Onshore':1004067, 'Wind_Offshore':1001225, 'Natural_Gas':1004071}
# Natural_Gas is for comparing its dataframe with the one loaded with load_energy_produced_by_companies

def load_green_energy_data(energy:str) -> pd.DataFrame:
    folder = GREEN_ENERGIES_FOLDER + '/' + energy
    energy_list = os.listdir(folder)
    energy_list.sort()
    df_list = []
    energy_col = energy + ' [MWh]'

    for file in energy_list:
        # take only csv files
        if 'Identifier' not in file:
            df = pd.read_csv(GREEN_ENERGIES_FOLDER + '/' +  energy + '/' + file, delimiter=';', decimal=',')
            df = clean_and_group_data_per_hour(df, energy_col)
            df_list.append(df)

    final_df = pd.concat(df_list)
    final_df = final_df.reset_index(drop=True)
    final_df.to_csv(PROCESSED_DATA_FOLDER + '/' + 'processed_power_from_' + energy + '.csv')

    return final_df


def clean_and_group_data_per_hour(df: pd.DataFrame, energy_col:str) -> pd.DataFrame:
    df.columns = ['Datum', 'Anfang', 'Ende', energy_col]
    df['Timestamp'] = pd.to_datetime(df['Datum'] + ' ' + df['Anfang'], format='%d.%m.%Y %H:%M')
    df = df.drop(columns=['Datum','Anfang', 'Ende'])
    df = clean_column_dataframe(df, energy_col)

    # sum power values for every hour and ignoring timestamp column
    dict_grouping = {'Timestamp': 'first',  energy_col : 'sum'}
    df = df.groupby(df.index // 4).agg(dict_grouping)
    return df


def load_green_energy_production_from_web(date_1, date_2, energy_sector, region, initial_iteration, limit_iteration):
    # parameters
    i = initial_iteration
    steps_size = 86400000
    days = 2
    start = date_2
    end = 0
    timeout = 5

    # download in a loop
    while i <= limit_iteration:
        print(i)
        driver = webdriver.Chrome()
        sleep(1)
        if initial_iteration==0 and i==0:
            start = date_1
            end = date_2 + steps_size
        elif initial_iteration!=0 and i==initial_iteration:
            start =  date_2 + steps_size*(i+1)
            end = start + steps_size*days
        else:
            start = end + steps_size
            end = start + steps_size*days
        #debug
        print('start = ', start )
        print('end =', end)

        # connect to url
        web_site = 'https://www.smard.de/home/marktdaten?marketDataAttributes=%7B%22resolution%22:%22hour%22,%22from%22:' + \
            str(start) + ',%22to%22:' + str(end) + ',%22moduleIds%22:%5B' + \
                str(DICT_GREEN_ENERGIES[energy_sector]) + \
                    '%5D,%22selectedCategory%22:1,%22activeChart%22:false,%22style%22:%22color%22,%22categoriesModuleOrder%22:%7B%7D,%22region%22:%22' + \
                    region+'%22%7D'

        # print(web_site)
        driver.get(web_site)
        sleep(5)

        # test url
        current_url = driver.current_url
        if current_url == web_site:
            print("WebDriver successfully connected to the URL.")
        else:
            print("WebDriver failed to connect to the URL.")

        # get value from imput
        date_from = driver.find_element(By.XPATH, "//input[@class='c-date-picker__from']")
        print('collect data from: ', date_from.get_attribute('value'))
        date_to = driver.find_element(By.XPATH, "//input[@class='c-date-picker__to']")
        print('to: ', date_to.get_attribute('value'))
        date_from = datetime.strptime(date_from.get_attribute('value'), '%d.%m.%Y')
        date_limit = datetime.strptime('21.03.2023', '%d.%m.%Y')
        if date_from >= date_limit:
            break

        # click menu button
        menu_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-article-menu-opener')))
        menu_button.click()
        sleep(2)

        # click download CSV button
        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space()="CSV"]')))

        download_button.click()
        sleep(timeout)

        # close the file download window
        driver.close()
        i=i+1

# Example file downloaded Realisierte_Erzeugung_2021-07-06-0059_2021-07-08-0059_viertelstunde
