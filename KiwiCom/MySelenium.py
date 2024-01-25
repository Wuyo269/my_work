from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager

import time
import datetime
import pandas as pd

#library of my custom methods
class MySelenium():

    def __init__(self, in_url, in_webdriver_path):
        #Initilize driver
        self.open_url(in_url, in_webdriver_path)

    # Open elecion url | return driver
    def open_url(self,in_url, in_webdriver_path):
        # DEBUG
        # in_url = 'https://wybory.gov.pl/sejmsenat2023/pl/sejm/wynik/okr/2'

        # Create webdriver object
        service = Service(in_webdriver_path)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)

        # open URL
        self.driver.get(in_url)

    #Switch to frame to use its element
    def switch_to_frame(self, frame_name):
        self.driver.switch_to.frame(frame_name)

    #Switch back to default from frame
    def switch_back_to_main_frame(self):
        # Swithc back to default
        self.driver.switch_to.default_content()


    # Scroll down to end of page
    def scroll_down_to_end(self):
        len_of_page = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while match == False:
            last_count = len_of_page
            time.sleep(3)
            len_of_page = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if last_count == len_of_page:
                match = True


    #Scroll up to the beginning of the page
    def scroll_up_to_start(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body"))).send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)


    #Map element | Wait for presence
    #element_button_accept = WebDriverWait(driver, 20).until(
    #    EC.presence_of_element_located((By.ID, "cookies_accept")))


#Selenium methods for Active Administration website
class ActiveAdministration(MySelenium):

    def __init__(self, in_url, in_webdriver_path):
        #Initilize driver
        self.open_url(in_url, in_webdriver_path)

    def download_file(self, selector_value):
        #DEBUG
        #selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        #Find element
        element_button_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,selector_value)))
        #Click button
        element_button_search.click()

#Selenium method for Kiwi.com
class KiwiCom(MySelenium):

    def __init__(self, in_url, in_webdriver_path):
        #Initilize driver
        self.open_url(in_url, in_webdriver_path)


    # Get details information from fly card | return array
    def get_details_information(self,element_web):
        # Get details
        element_mb_xxs = element_web.find_element(By.CLASS_NAME, 'mb-xxs.text-small.text-secondary-foreground')

        departure_datetime = element_mb_xxs.find_element(By.TAG_NAME, "time").get_attribute("datetime").split(".")[
            0].replace("T", " ")
        departure_datetime = datetime.datetime.strptime(departure_datetime, '%Y-%m-%d %H:%M:%S').strftime(
            "%d.%m.%Y %H:%M")
        departure_price = element_web.find_element(By.CLASS_NAME,
                                                   'whitespace-nowrap.text-heading-title2.font-heading-title2.text-primary-foreground').text.replace(
            " zł", "").replace(" €", "")
        departure_company = element_web.find_element(By.CLASS_NAME,
                                                     "CarrierLogo__StyledImage-sc-1rhi78a-0.cXhcBL").accessible_name
        departure_airport_in = element_web.find_elements(By.CLASS_NAME,
                                                         'overflow-hidden.text-ellipsis.whitespace-nowrap.font-medium.text-ink-dark.flex-grow')[
            0].text.replace("Port lotniczy", "").strip()
        departure_airport_out = element_web.find_elements(By.CLASS_NAME,
                                                          'overflow-hidden.text-ellipsis.whitespace-nowrap.font-medium.text-ink-dark.flex-grow')[
            1].text.replace("Port lotniczy", "").strip()

        return [departure_datetime, departure_price, departure_company, departure_airport_in, departure_airport_out]

    # Get information from all fly cards | return array
    def get_all_cards_information(self,in_elements_cards):
        # Initialize Array
        data = []
        # Loop through all cards
        for element_card in in_elements_cards:
            # Get details information
            try:
                data_current = self.get_details_information(element_web=element_card)
                # Add data to array
                data.append(data_current)
            except Exception as e:
                print("Element failed")

        return data

#data transforming methods
class KiwiMethods():

    # dictionary of cities presented on kiwiw website
    # kiwi_dict["malaga"] = "malaga-hiszpania"
    kiwi_dict = {}
    kiwi_dict["malaga"] = "malaga-hiszpania"
    kiwi_dict["katowice"] = "katowice-polska"
    kiwi_dict["krakow"] = "krakow-polska"
    kiwi_dict["mediolan"] = "mediolan-wlochy"

    # Build kiwi url based on proivided criteria
    def build_kiwi_url(in_airport_start="", in_airport_end="", in_datetime_start="", in_datetime_end="",
                       in_b_one_way=True, in_b_direct_fly=True):
        # DEBUG
        # dt1 = "19.03.2024 19:05"
        # dt2 = "26.03.2024 10:05"
        # datetime_start = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
        # datetime_end = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")

        # One way or return
        if in_b_one_way:
            one_way = "no-return"
        else:
            one_way = ""

        # direct fly or multiple airports
        if in_b_direct_fly:
            direct_fly = "?stopNumber=0%7Etrue"
        else:
            direct_fly = ""

        # Date range
        date_range = f"{in_datetime_start:%Y}-{in_datetime_start:%m}-{in_datetime_start:%d}_{in_datetime_end:%Y}-{in_datetime_end:%m}-{in_datetime_end:%d}"

        # Create final url
        url = f"https://www.kiwi.com/pl/search/results/{in_airport_start}/{in_airport_end}/{date_range}/{one_way}{direct_fly}"

        return url

    #Calculate how many nights are between dates
    def midnights(dt1, dt2):
        dt1 = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
        dt2 = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")
        dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
        dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
        return (dt2 - dt1).days

    #Calculate how many days are between dates
    def wholedays(dt1, dt2):
        #DEBUG
        #dt1 = "13.03.2024 17:20"
        #dt2 = "20.03.2024 21:45"
        dt1 = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
        dt2 = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")

        #If start date start after 10 do not count it
        if dt1.hour > 10:
            dt1 = dt1.replace(day=dt1.day+1)
        # If end date is after 18 do not count it
        if dt2.hour > 18:
            dt2 = dt2.replace(day=dt2.day+1)

        dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
        dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
        return (dt2 - dt1).days

    #Create combination af all flies from the dataframes
    def create_fly_combinations(in_excel_departure, in_excel_arrival):
        #Read input excels
        df_departure = pd.read_excel(in_excel_departure)
        df_arrival = pd.read_excel(in_excel_arrival)

        #Rename columns in arrival
        df_arrival.rename(columns={"departure_datetime": "arrival_datetime", "departure_price": "arrival_price",
                            "departure_company":"arrival_company","departure_airport_in":"arrival_airport_in",
                            "departure_airport_out":"arrival_airport_out"}, inplace=True)

        #Create every combination based on two dataframes
        df_departure.merge(df_arrival, how='cross')
        df_departure['key'] = 1
        df_arrival['key'] = 1
        df_fly_combination = pd.merge(df_departure, df_arrival, on='key').drop('key', axis=1)

        return df_fly_combination

    # Add additional columns with calculations
    def transform_fly_combinations(df_fly_combination):
        # Total price for both flies
        df_fly_combination["total_price"] = df_fly_combination["departure_price"].astype("int") + df_fly_combination[
            "arrival_price"].astype("int")
        # Convert datetime strings to datetime variables
        pd.to_datetime(df_fly_combination['departure_datetime'])
        pd.to_datetime(df_fly_combination['arrival_datetime'])
        # Count how many days are in trip
        df_fly_combination["days"] = df_fly_combination.apply(
            lambda x: KiwiMethods.wholedays(x["departure_datetime"], x["arrival_datetime"]), axis=1)
        # Count how many nights are in trip
        df_fly_combination["nights"] = df_fly_combination.apply(
            lambda x: KiwiMethods.midnights(x["departure_datetime"], x["arrival_datetime"]), axis=1)
        # Check if the start airport and end airport are the same
        df_fly_combination["same_airport"] = df_fly_combination["departure_airport_in"] == df_fly_combination[
            "arrival_airport_out"]
        # Check if there is more nights than days
        df_fly_combination["days_night_difference"] = df_fly_combination["days"] - df_fly_combination["nights"]
        # Flter only by days > 0
        df_fly_combination = df_fly_combination[df_fly_combination["days"]>0]

        return df_fly_combination
