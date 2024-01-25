from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import time
import pandas as pd


# Selenium methods for FlashScore website
class FlashScore():
    # Initialize instance
    def __init__(self) -> None:
        self.driver = None

    #### CONSTANT Variables ############################################################################################
    # Web elements locators
    MAIN_TABLE_CLASS_NAME = "ui-table__body"
    MAIN_TABLE_ROWS_CLASS_NAME = r"ui-table__row  "
    POSITION_CLASS_NAME = "tableCellRank"
    CLUB_NAME_CLASS_NAME = "tableCellParticipant__name"
    CELL_VALLUES_XPATH = ".//span[@class = ' table__cell table__cell--value   ']"
    COUNTRY_CSS_SELECTOR_NAME = "#mc > div.container__livetable > div.container__heading > h2 > a:nth-child(5)"
    LEAGUE_CSS_SELECTOR_NAME = "#mc > div.container__livetable > div.container__heading > div.heading > div.heading__title > div.heading__name"
    ROW_CELL_VALUE_CLASS_NAME = "table__cell.table__cell--value"
    TABLE_CELL_FORM_ICON_TBD = "tableCellFormIcon.tableCellFormIcon--TBD"

    MAIN_TABLE_COLUMN_NAMES = ["position", "club_name", "matches_played", "wins", "draws", "loses", "balance",
                               "goals_difference", "points", "next_game"]

    MAIN_TABLE_COLUMN_NAMES_OLD_PROCESS = ["county", "league", "name", "position", "matches_played", "wins",
                                           "percentage", "matches_all",
                                           "points_left", "club_points", "next_club_points", "points_surplus",
                                           "points_to_champion"]

    # Frames names

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
            raise Exception(f"Open_url method fails - {error_message}") from error_message

    # Check if driver connection is alive
    def is_driver_alive(self):
        try:
            # Try to get current url, if connection is dead pytho raise exception
            current_url = self.driver.current_url
            return True
        except Exception as error_message:
            return False

    # Close connection, if unable -> quit connection
    def close_driver_connection(self):
        try:
            self.driver.close()
        except Exception as error_message:
            self.quit_driver_connection()

    # Quit connection
    def quit_driver_connection(self):
        try:
            self.driver.quit()
        except Exception as error_message:
            raise Exception(f"Method 'quit_driver_connection'fails - {error_message}") from error_message

    # Switch to frame to use its element
    def switch_to_frame(self, frame_name: str) -> None:
        try:
            self.driver.switch_to.frame(frame_name)
        except Exception as error_message:
            raise Exception(f"switch_to_frame method fails - {error_message}") from error_message

    # Switch back to default frame
    def switch_back_to_main_frame(self) -> None:
        try:
            self.driver.switch_to.default_content()
        except Exception as error_message:
            raise Exception(f"switch_back_to_main_frame method fails - {error_message}") from error_message

    # map element
    def map_element(self, base_element: object, locator_type: object, locator_value: str) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = base_element.find_element(locator_type, locator_value)
            return element
        except Exception as error_message:
            raise Exception(f"map_element method fails - {error_message}") from error_message

    # map all elements
    def map_all_elements(self, base_element: object, locator_type: object, locator_value: str) -> object:
        # DEBUG
        # css_selector_value = "#grdResultat_ctl02 > td:nth-child(1) > a"
        try:
            # Find element
            element = base_element.find_elements(locator_type, locator_value)
            return element
        except Exception as error_message:
            raise Exception(f"map_all_elements method fails - {error_message}") from error_message

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
            raise Exception(f"map_element_with_wait method fails - {error_message}") from error_message

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
            raise Exception(f"map_all_elements_with_wait method fails - {error_message}") from error_message

    # Check if checkbox element is selected / marked
    def is_checkbox_selected(self, element: object) -> bool:
        try:
            return element.is_selected()
        except Exception as error_message:
            raise Exception(f"is_checkbox_selected method fails - {error_message}") from error_message

    # click element / mark checkbox
    def click_element(self, element: object) -> None:
        try:
            element.click()
        except Exception as error_message:
            raise Exception(f"click_element method fails - {error_message}") from error_message

    # Scroll up to the beginning of the page
    def scroll_up_to_start(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body"))).send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(3)
        except Exception as error_message:
            raise Exception(f"scroll_up_to_start method fails - {error_message}") from error_message

    # Scroll down to end of page
    def scroll_down_to_end(self):
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
            raise Exception(f"scroll_down_to_end method fails - {error_message}") from error_message

    # Refresh webpage until page is loaded
    def refresh_until_loads_correctly(self, element_css_selector):
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
            raise Exception(f"Unable to load page. {attempts} attempts  - {error_message}")

        # Switch back to default
        self.switch_back_to_main_frame()

    #### selenium methods ##############################################################################################

    #### simple methods ################################################################################################
    # Map main table element
    def map_main_table(self) -> object:
        try:
            element_table = self.map_element_with_wait(By.CLASS_NAME, self.MAIN_TABLE_CLASS_NAME)
            return element_table
        except Exception as error_message:
            raise Exception(f"Method 'map_main_table' fails - {error_message}") from error_message

    # Map rows of main table element
    def map_main_table_rows(self) -> object:
        try:
            element_table = self.map_main_table()
            element_rows = self.map_all_elements(element_table, By.CLASS_NAME, self.MAIN_TABLE_ROWS_CLASS_NAME)
            return element_rows
        except Exception as error_message:
            raise Exception(f"Method 'map_main_table_rows' fails - {error_message}") from error_message

    # Get the name of country
    def get_country_name(self) -> str:
        try:
            element = self.map_element_with_wait(By.CSS_SELECTOR, self.COUNTRY_CSS_SELECTOR_NAME)
            return element.text
        except Exception as error_message:
            raise Exception(f"Method 'get_country_name' fails - {error_message}") from error_message

    # Get the name of league
    def get_league_name(self) -> str:
        try:
            element = self.map_element_with_wait(By.CSS_SELECTOR, self.LEAGUE_CSS_SELECTOR_NAME)
            return element.text
        except Exception as error_message:
            raise Exception(f"Method 'get_league_name' fails - {error_message}") from error_message

    #### simple methods ################################################################################################

    #### advanced methods ##############################################################################################
    # Get all data from main table
    def get_main_table_data(self) -> object:
        # Initialize Array
        data = []

        # Get element rows of main table
        element_rows = self.map_main_table_rows()

        # Loop through all rows
        for row in element_rows:
            # Get details
            club_position = self.map_element(row, By.CLASS_NAME, self.POSITION_CLASS_NAME).text
            club_position = int(club_position.replace(".", ""))
            club_name = self.map_element(row, By.CLASS_NAME, self.CLUB_NAME_CLASS_NAME).text
            cell_values = self.map_all_elements(row, By.CLASS_NAME, self.ROW_CELL_VALUE_CLASS_NAME)
            matches_played = int(cell_values[0].text)
            wins = int(cell_values[1].text)
            draws = int(cell_values[2].text)
            loses = int(cell_values[3].text)
            balance = cell_values[4].text
            goals_difference = int(cell_values[5].text)
            points = int(cell_values[6].text)
            try:
                next_game_text = self.map_element(row, By.CLASS_NAME, self.TABLE_CELL_FORM_ICON_TBD).get_attribute("title")
                next_game_text = next_game_text.split("\n")[2]
            except Exception as error_message:
                next_game_text = "???"

            # Create current array
            data_current = [club_position, club_name, matches_played, wins, draws, loses, balance, goals_difference,
                            points, next_game_text]

            # Append current data to main data
            data.append(data_current)

        # Create pandas dataframe
        df = pd.DataFrame(data, columns=self.MAIN_TABLE_COLUMN_NAMES)

        return df

    #### advanced methods ##############################################################################################
