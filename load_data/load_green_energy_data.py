from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
DICT_GREEN_ENERGIES = {'Photovoltaik':1004068, 'Wind (Onshore)':1004067, 'Wind (Offshore)':1001225, 'Erdgas':1004071}

def load_green_energy_data(energy, region, initial_iteration, limit_iteration):

    i = initial_iteration # un a#
    date_1 = 1514761200000
    date_2 = 1514933999999
    steps_size = 86400000
    days = 2
    start = 0
    end = 0
    timeout = 5
    while i <= limit_iteration:
        print(i)
        driver = webdriver.Chrome()
        #sleep(5)
        if initial_iteration==0 and i==0:
            start = date_1
            end = date_2 + steps_size
        elif initial_iteration!=0 and i==initial_iteration:
            start =  date_2 + steps_size*(i+1)
            end = start + steps_size*days
        else:
            start = end + steps_size
            end = start + steps_size*days
        print('start', start )
        print('end', end)
        web_site = 'https://www.smard.de/home/marktdaten?marketDataAttributes=%7B%22resolution%22:%22hour%22,%22from%22:'+ str(start) + ',%22to%22:' + str(end)+',%22moduleIds%22:%5B'+ str(DICT_GREEN_ENERGIES[energy])+'%5D,%22selectedCategory%22:1,%22activeChart%22:false,%22style%22:%22color%22,%22categoriesModuleOrder%22:%7B%7D,%22region%22:%22'+ region +'%22%7D'

        driver.get(web_site)
        sleep(5)
        current_url = driver.current_url

        if current_url == web_site:
            print("WebDriver successfully connected to the URL.")
        else:
            print("WebDriver failed to connect to the URL.")


        menu_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-article-menu-opener')))
        sleep(2)
        menu_button.click()
        sleep(2)

        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space()="CSV"]')))
        sleep(2)
        download_button.click()
        sleep(timeout)
        driver.close()
        i=i+1
