import time

import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


# Selenium methods for FlashScore website
class Glosbe():
    # Initialize instance
    def __init__(self) -> None:
        self.driver = None

    #### CONSTANT Variables ############################################################################################
    LOGGING_MARKER = "GLOSBE:"
    # Web elements locators
    VERB_IN_POLISH_XPATH = r"/html/body/div[1]/div/div[2]/main/article/div/div[1]/section[1]/div[2]/div/ul[1]/li[1]/div[2]/div[1]/div[2]/h3"
    VERB_IN_POLISH_XPATH2 = r"/html/body/div[1]/div/div[2]/main/article/div/div[1]/section[1]/div[2]/div/ul[1]/li[2]/div[2]/div[1]/div[2]/h3"
    VERB_IN_SPANISH_CSS_SELECTOR = r"#phraseDetails_activator-0 > div.text-xl.text-gray-900.px-1.pb-1 > span.font-medium.break-words"
    MORE_BUTTON_XPATH = r"/html/body/div[1]/div/div[2]/main/article/div/div[1]/section[1]/div[1]/div[2]/div/div[2]/label/span"
    CONJUGATION_TABLE_XPATH = r"//tbody"
    CONJUGATION_TABLE_ROWS_XPATH = r"tr"
    CONJUGATION_TABLE_COLUMN_XPATH = ".//*"

    #### CONSTANT Variables ############################################################################################

    #### selenium methods ##############################################################################################
    # Open url, create driver object
    def open_url(self, in_url: str, in_webdriver_path: str) -> None:
        try:
            # Create webdriver object
            service = Service(in_webdriver_path)
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
            # open URL
            self.driver.get(in_url)
        except Exception as error_message:
            raise Exception(f"{self.LOGGING_MARKER} Method  'Open_url' fails - {error_message}") from error_message

    # Check if driver connection is alive
    def is_driver_alive(self) -> bool:
        try:
            # Try to get current url, if connection is dead pytho raise exception
            current_url = self.driver.current_url
            return True
        except Exception as error_message:
            return False

    # Close connection, if unable -> quit connection
    def close_driver_connection(self) -> None:
        try:
            self.driver.close()
        except Exception as error_message:
            self.quit_driver_connection()

    # Quit connection
    def quit_driver_connection(self) -> None:
        try:
            self.driver.quit()
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'quit_driver_connection' fails - {error_message}") from error_message

    # Switch to frame to use its element
    def switch_to_frame(self, frame_name: str) -> None:
        try:
            self.driver.switch_to.frame(frame_name)
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'switch_to_frame' fails - {error_message}") from error_message

    # Switch back to default frame
    def switch_back_to_main_frame(self) -> None:
        try:
            self.driver.switch_to.default_content()
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'switch_back_to_main_frame' fails - {error_message}") from error_message

    # map element
    def map_element(self, base_element: object, locator_type: object, locator_value: str) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = base_element.find_element(locator_type, locator_value)
            return element
        except Exception as error_message:
            raise Exception(f"{self.LOGGING_MARKER} Method 'map_element' fails - {error_message}") from error_message

    # map all elements
    def map_all_elements(self, base_element: object, locator_type: object, locator_value: str) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = base_element.find_elements(locator_type, locator_value)
            return element
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_all_elements' fails - {error_message}") from error_message

    # map element with wait
    def map_element_with_wait(self, locator_type: object, locator_value: str, wait_time: int = 10) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((locator_type, locator_value)))
            return element
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_element_with_wait' method fails - {error_message}") from error_message

    # map all elements by css_selector value
    def map_all_elements_with_wait(self, locator_type: object, locator_value: str, wait_time: int = 10) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located((locator_type, locator_value)))
            return element
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_all_elements_with_wait' fails - {error_message}") from error_message

    # Check if checkbox element is selected / marked
    def is_checkbox_selected(self, element: object) -> bool:
        try:
            return element.is_selected()
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method  'is_checkbox_selected' fails - {error_message}") from error_message

    # click element / mark checkbox
    def click_element(self, element: object) -> None:
        try:
            element.click()
        except Exception as error_message:
            raise Exception(f"{self.LOGGING_MARKER} Method 'click_element' fails - {error_message}") from error_message

    # Scroll up to the beginning of the page
    def scroll_up_to_start(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body"))).send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(3)
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'scroll_up_to_start' fails - {error_message}") from error_message

    # Scroll down to end of page
    def scroll_down_to_end(self) -> None:
        script_text = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        try:
            len_of_page = self.driver.execute_script(script_text)
            match = False
            while match == False:
                last_count = len_of_page
                time.sleep(3)
                len_of_page = self.driver.execute_script(script_text)
                if last_count == len_of_page:
                    match = True
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'scroll_down_to_end' fails - {error_message}") from error_message

    # Refresh webpage until page is loaded
    def refresh_until_loads_correctly(self, element_css_selector) -> None:
        # DEBUG:
        # element_id = "#\32  > a"
        attempts = 0
        while attempts < 4:
            try:
                # Switch to frame "FrameGauche"
                self.switch_to_frame(self.frame_gauche_name)
                # Click Activity search button
                element_button_activity_search = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, element_css_selector)))
                break
            except Exception as e:
                attempts += 1
                self.driver.refresh()
                error_message = e

        # Raise error if page not loaded
        if attempts >= 4:
            raise Exception(f"{self.LOGGING_MARKER} Method Unable to load page. {attempts} attempts  - {error_message}")

        # Switch back to default
        self.switch_back_to_main_frame()

    #### selenium methods ##############################################################################################

    #### simple methods ################################################################################################
    # Get the translation of spanish verb in Polish
    def get_verb_in_polish(self) -> str:
        try:
            # try get 2 elements
            try:
                element = self.map_element_with_wait(By.XPATH, self.VERB_IN_POLISH_XPATH, 4)
            except Exception as error_message:
                element = self.map_element_with_wait(By.XPATH, self.VERB_IN_POLISH_XPATH2, 4)
            return element.text
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method  'get_verb_in_polish' fails - {error_message}") from error_message

    # Get spanish verb
    def get_verb_in_spanish(self) -> str:
        try:
            element = self.map_element_with_wait(By.CSS_SELECTOR, self.VERB_IN_SPANISH_CSS_SELECTOR)
            return element.text
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_verb_in_spanish' fails - {error_message}") from error_message

    # Click in the verb to show more details
    def click_verb_element(self) -> None:
        try:
            element = self.map_element_with_wait(By.CSS_SELECTOR, self.VERB_IN_SPANISH_CSS_SELECTOR)
            self.click_element(element)
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'click_verb_element' fails - {error_message}") from error_message

    # Click in the more button to expand details
    def click_more_button(self) -> None:
        try:
            element = self.map_element_with_wait(By.XPATH, self.MORE_BUTTON_XPATH)
            self.click_element(element)
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'click_more_button' fails - {error_message}") from error_message

    # Map table with al kind of conjugations
    def map_conjugation_table(self) -> object:
        try:
            element = self.map_element_with_wait(By.XPATH, self.CONJUGATION_TABLE_XPATH)
            return element
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_conjugation_table' fails - {error_message}") from error_message

    # Map rows of table with al kind of conjugations
    def map_conjugation_table_rows(self) -> object:
        try:
            element_table = self.map_conjugation_table()
            elements = self.map_all_elements(element_table, By.XPATH, self.CONJUGATION_TABLE_ROWS_XPATH)
            return elements
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_conjugation_table_rows' fails - {error_message}") from error_message

    #### simple methods ################################################################################################

    #### advanced methods ##############################################################################################

    # Get all details from conjugation table
    def get_conjugation_table(self) -> pd.DataFrame:
        try:

            # Get word in polish
            verb_in_polish = self.get_verb_in_polish()
            # Get word in spanish
            verb_in_spanish = self.get_verb_in_spanish()

            # Create datatable
            column_names = ["czasownik_pl", "czasownik_sp", "Tryb", "czas", "osoba", "wartosc"]
            persons = ["yo", "tu", "el", "nosotros", "vosotros", "ustedes"]
            df = pd.DataFrame(columns=column_names)

            # Get rows of conjugation table
            rows = self.map_conjugation_table_rows()

            # Loop through all rows
            for row in rows:
                # Get columns elements
                columns = self.map_all_elements(row, By.XPATH, self.CONJUGATION_TABLE_COLUMN_XPATH)

                # skip empty lines
                if len(columns) == 1:
                    continue

                # Skip unwanted rows
                unwanted_rows_list = ["INFINITIVE", "SINGULAR", "1ST", "YO", "PERSON", "FIRST"]
                if row.text.split(" ")[0] in unwanted_rows_list:
                    continue

                # Get data for Gerundio and Past Participle
                if row.text.startswith("GERUND") or row.text.startswith("PAST PARTICIPLE"):
                    list_row = [verb_in_polish, verb_in_spanish, columns[0].text, "", "", columns[1].text]
                    # Add row to datatable
                    df.loc[len(df)] = list_row
                    continue

                # get current type
                if row.text.startswith("INDICATIVE") or row.text.startswith("SUBJUNCTIVE") or \
                        row.text.startswith("IMPERATIVE"):
                    type = columns[0].text

                # Ignore persons headers
                if columns[1].text == "":
                    continue

                # loop through all columns
                for i in range(1, len(columns)):
                    list_row = [verb_in_polish, verb_in_spanish, type, columns[0].text, persons[i - 1], columns[i].text]
                    # Add row to datatable
                    df.loc[len(df)] = list_row
                continue

            return df
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_conjugation_table' fails - {error_message}") from error_message

    #### advanced methods ##############################################################################################


# DEBUG TEST
if False:
    url = "https://glosbe.com/es/pl/ver"
    webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
    glosbe_instance = Glosbe()
    # Open url
    glosbe_instance.open_url(url, webdriver_path)

    translation = glosbe_instance.get_verb_in_polish()

    glosbe_instance.click_verb_element()
    glosbe_instance.click_more_button()
    rows = glosbe_instance.get_conjugation_table()

    for row in rows:
        columns = row.find_elements(By.XPATH, ".//*")

    print("Check")
