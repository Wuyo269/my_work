import os
import time
import pandas as pd
import openpyxl
import datetime


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#library of my custom methods
#from MySelenium import MySelenium
from MySelenium import KiwiCom, KiwiMethods

#Apend data to excel
def append_to_excel(fpath, df):
    #If excel exist read sheet as DataTable
    if (os.path.exists(fpath)):
        df_current=pd.read_excel(fpath)
    #If excel does not exist create new DataTable
    else :
        df_current=pd.DataFrame()

    df_concat=pd.concat([df,df_current])
    df_concat.to_excel(fpath,index=False)


#Procss single Kiwi URL
def process_kiwi(in_url, in_webdriver_path, in_excel_name):
    # 1. Open URL
    #driver = KiwiCom.open_url(in_url, in_webdriver_path)
    # Initialize Kiwi Instance
    kiwi_instance = KiwiCom(url_departure, webdriver_path)
    driver = kiwi_instance.driver

    # Find element button "Accept" & click it
    try:
        element_button_accept = WebDriverWait(kiwi_instance.driver, 10).until(
            EC.presence_of_element_located((By.ID, "cookies_accept")))
        element_button_accept.click()
    except:
        print("Accept button does not exist")

    # Set default value as True
    button_view_more_exist = True

    while button_view_more_exist:
        # Scroll to end of page
        kiwi_instance.scroll_down_to_end()
        # Find element button "View More" & click it
        try:
            element_button_view_more = WebDriverWait(kiwi_instance.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "ButtonPrimitive__StyledButtonPrimitive-sc-j8pavp-0.RZQEq")))
            element_button_view_more.click()
        except:
            print("Button 'View More' does not exist")
            button_view_more_exist = False

    #Scroll up to the beginning of the page
    kiwi_instance.scroll_up_to_start()

    # 2. Get all elements "mb-md" (Cards)
    element_cards_table = WebDriverWait(kiwi_instance.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Box__StyledBox-sc-bvm5o6-0.kceqXj")))
    elements_cards = element_cards_table.find_elements(By.CLASS_NAME, "mb-md")

    # 3. Get information of all flies in current page
    data_flies = kiwi_instance.get_all_cards_information(in_elements_cards=elements_cards)

    # Create DataFrame
    df_flies = pd.DataFrame(data=data_flies, columns=["departure_datetime", "departure_price", "departure_company",
                                                      "departure_airport_in", "departure_airport_out"])

    # 4. Save Data in Excel
    append_to_excel(in_excel_name, df_flies)


'''INPUTS'''
#DEBUG - Test URL
#url = r"https://www.kiwi.com/pl/search/results/katowice-polska,krakow-polska/malaga-hiszpania/2024-02-05_2024-02-20/no-return?stopNumber=0%7Etrue"
#url2 = r"https://www.kiwi.com/pl/search/results/malaga-hiszpania/katowice-polska,krakow-polska/2024-02-05_2024-02-20/no-return?stopNumber=0%7Etrue"

webdriver_path = "C:\Program Files (x86)\chromedriver.exe"
#Excel names
excel_departure = "output_departure.xlsx"
excel_arrival = "output_arrival.xlsx"
excel_output = "output_fly_combination.xlsx"
#Fly criteria
airport_start = "katowice-polska,krakow-polska"
airport_end = "las-palmas-de-gran-canaria-hiszpania"
datetime_start =  datetime.datetime.strptime("05.02.2024", "%d.%m.%Y")
datetime_end =  datetime.datetime.strptime("20.02.2024", "%d.%m.%Y")


#URL
url_departure =  KiwiMethods.build_kiwi_url(in_airport_start=airport_start, in_airport_end=airport_end, in_datetime_start=datetime_start,
                               in_datetime_end=datetime_end,in_b_direct_fly=True, in_b_one_way=True)
url_arrival =KiwiMethods.build_kiwi_url(in_airport_start=airport_end, in_airport_end=airport_start, in_datetime_start=datetime_start,
                               in_datetime_end=datetime_end,in_b_direct_fly=True, in_b_one_way=True)




#1. Get data from Kiwi.com
process_kiwi(in_webdriver_path=webdriver_path, in_url=url_departure, in_excel_name=excel_departure)
process_kiwi(in_webdriver_path=webdriver_path, in_url=url_arrival, in_excel_name=excel_arrival)

#2. Create every combination based on 2 dataframes
df_fly_combination = KiwiMethods.create_fly_combinations(in_excel_departure=excel_departure, in_excel_arrival=excel_arrival)

#3. Add additional calculation
df_fly_combination = KiwiMethods.transform_fly_combinations(df_fly_combination)

# Save results to excel
append_to_excel(excel_output, df_fly_combination)


print("SPAP")


