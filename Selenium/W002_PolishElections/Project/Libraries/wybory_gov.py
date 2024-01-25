from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import time
import pandas as pd


# Selenium methods for FlashScore website
class WyboryGov():
    # Initialize instance
    def __init__(self) -> None:
        self.driver = None

    #### CONSTANT Variables ############################################################################################
    LOGGING_MARKER = "WYBORY_GOV:"
    # Web elements locators
    TABLE_0_ROWS_CSS_SELECTOR_NAME = r"#DataTables_Table_0 > tbody > tr"
    WINNERS_LI_ELEMENTS_CSS_SELECTOR_NAME = r"#root > div.res > div.can.mt-3 > ul > li"
    COMMITTEE_DETAILS_TABLES_CLASS_NAME = R"col-xs-12.col-xl-6.table-responsive"
    DISTRICT_NAME_CSS_SELECTOR_NAME = r"div[class='res'] div[class='row'] h3"
    DISTRICT_MANDATES_NUMBER_XPATH_NAME = r"//*[@id='DataTables_Table_0']/tfoot/tr/td[4]"
    DISTRICT_LINKS_CSS_SELECTOR_NAME = r"#root > div.res > div.row > div.stats.col-xs-12.col-md-6.col-lg-7 > div > ul > li > ul > li >a"

    # Column Names
    COMMITTEE_COLUMN_NAME = "committee_name"
    PERSON_COLUMN_NAME = "person_name"
    VOTES_NUMBER_COLUMN_NAME = "votes_number"
    VOTES_PERCENTAGE_COLUMN_NAME = "votes_percentage"
    MANDATES_NUMBER_COLUMN_NAME = "mandates_number"
    MANDATES_PERCENTAGE_COLUMN_NAME = "mandates_percentage"
    DISTRICT_NAME_COLUMN_NAME = "district_name"
    POSITION_ON_LIST_COLUMN_NAME = "position_on_list"
    DISTRICT_LINK_COLUMN_NAME = "district_link"
    DISTRICT_MANDATES_NUMBER = "district_mandates_number"

    #### CONSTANT Variables ############################################################################################

    #### selenium methods ##############################################################################################
    if True:
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
                raise Exception(
                    f"{self.LOGGING_MARKER} Method 'map_element' fails - {error_message}") from error_message

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
                raise Exception(
                    f"{self.LOGGING_MARKER} Method 'click_element' fails - {error_message}") from error_message

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
                raise Exception(
                    f"{self.LOGGING_MARKER} Method Unable to load page. {attempts} attempts  - {error_message}")

            # Switch back to default
            self.switch_back_to_main_frame()

    #### selenium methods ##############################################################################################

    #### simple methods ################################################################################################
    # map element Table 0 rows - Results of votes split of committee
    def map_element_table_0_rows(self) -> object:
        try:
            # Find element
            element = self.map_all_elements_with_wait(By.CSS_SELECTOR, self.TABLE_0_ROWS_CSS_SELECTOR_NAME)
            return element
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'map_element_table_0_rows' method fails - {error_message}") from error_message

    # Get the name/number of current district
    def get_district_number(self) -> str:
        try:
            # Find element
            element = self.map_element_with_wait(By.CSS_SELECTOR, self.DISTRICT_NAME_CSS_SELECTOR_NAME)
            # Format element
            district_name = str(element.text).split(" ")[-1]
            return district_name
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_district_number' method fails - {error_message}") from error_message

    # Check if the page is fully loaded. Selenium should be able to extract district number
    def wait_until_web_is_loaded(self) -> None:
        """
        Check if the page is fully loaded. Selenium should be able to extract district number
        """
        try:
            time_counter = 0
            district_name = self.get_district_number()
            while district_name == "" and time_counter < 5:
                time.sleep(1)
                time_counter += 1
                district_name = self.get_district_number()

            if district_name == "":
                raise Exception(
                    f"{self.LOGGING_MARKER} Method 'wait_until_web_is_loaded' method fails - page not loaded")
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'wait_until_web_is_loaded' method fails - {error_message}")

    # Get district mandates number | how many persons are elected from this district
    def get_district_mandates_number(self) -> int:
        try:
            # The number of mandates
            mandates_number = int(self.map_element_with_wait(By.XPATH, self.DISTRICT_MANDATES_NUMBER_XPATH_NAME).text)
            return mandates_number
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_district_mandates_number' method fails - {error_message}")

    # Get district mandates number as DataFrame | how many persons are elected from this district
    def get_district_mandates_number_df(self) -> pd.DataFrame:
        try:
            # Get district name
            district_name = "Okręg wyborczy nr " + self.get_district_number()
            # The number of mandates
            mandates_number = self.get_district_mandates_number()

            # Create panda dataframe
            df_district_mandates_number = pd.DataFrame([[mandates_number, district_name]],
                                                       columns=[self.DISTRICT_MANDATES_NUMBER,
                                                                self.DISTRICT_NAME_COLUMN_NAME])

            return df_district_mandates_number
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_district_mandates_number_df' method fails - {error_message}")

    #### simple methods ################################################################################################

    #### advanced methods ##############################################################################################
    # unify the committee names to 1 form
    def unify_committee_names(self, df_table) -> pd.DataFrame:
        # Create a dictionary of unified names
        dict_unified_names = {}
        dict_unified_names['KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ'] = 'PIS'
        dict_unified_names['KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI'] = 'PO'
        dict_unified_names[
            'KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE'] = 'PL2050'
        dict_unified_names['KOMITET WYBORCZY NOWA LEWICA'] = 'LEWICA'
        dict_unified_names['KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ'] = 'KONFEDERACJA'
        dict_unified_names['KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY'] = 'BEZPARTYJNI'
        dict_unified_names['KOMITET WYBORCZY POLSKA JEST JEDNA'] = 'PJJ'
        dict_unified_names['KW BEZPARTYJNI SAMORZĄDOWCY'] = 'BEZPARTYJNI'
        dict_unified_names['KKW TRZECIA DROGA PSL-PL2050 SZYMONA HOŁOWNI'] = 'PL2050'
        dict_unified_names['KW NOWA LEWICA'] = 'LEWICA'
        dict_unified_names['KW PRAWO I SPRAWIEDLIWOŚĆ'] = 'PIS'
        dict_unified_names['KW KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ'] = 'KONFEDERACJA'
        dict_unified_names['KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI'] = 'PO'
        dict_unified_names['KKW KOALICJA OBYWATELSKA PO .N IPL ZIELONI'] = 'PO'
        dict_unified_names['KW POLSKA JEST JEDNA'] = 'PJJ'

        # Check if item in dict
        for item in df_table[self.COMMITTEE_COLUMN_NAME].unique():
            if not item in dict_unified_names:
                print(f"dict_unified_names['{item}'] = 'ADDNAME'")
                with open("new_committee.txt", 'a+') as f:
                    f.write(f"dict_unified_names['{item}'] = 'ADDNAME'" + "\n")
                f.close()

        # unify names
        for item in dict_unified_names:
            df_table[self.COMMITTEE_COLUMN_NAME] = df_table[self.COMMITTEE_COLUMN_NAME].replace([item],
                                                                                                dict_unified_names[
                                                                                                    item])

        return df_table

    # Get votes results divided on committee
    def get_votes_results_divided_by_committee(self) -> pd.DataFrame:
        try:
            # Create empty array
            final_array = []
            # Get district name
            district_name = "Okręg wyborczy nr " + self.get_district_number()

            # Map rable 0 rows. It contains votes results divided by committees
            table_rows = self.map_element_table_0_rows()

            # Loop through all rows
            for row in table_rows:
                # Get column element
                col = self.map_all_elements(row, By.TAG_NAME, "td")

                # Get details
                committee = str(col[0].text)
                votes_number = int(col[1].text.replace(" ", ""))
                votes_percentage = float(col[2].text.replace("%", "").replace(",", ".")) / 100
                mandates_number = int(col[3].text.replace(" ", ""))
                mandates_percentage = float(col[4].text.replace("%", "").replace(",", ".")) / 100

                # Add details to current array
                current_array = [committee, votes_number, votes_percentage, mandates_number, mandates_percentage,
                                 district_name]
                # Append current array to final array
                final_array.append(current_array)

            # Column names
            column_names = [self.COMMITTEE_COLUMN_NAME, self.VOTES_NUMBER_COLUMN_NAME,
                            self.VOTES_PERCENTAGE_COLUMN_NAME,
                            self.MANDATES_NUMBER_COLUMN_NAME, self.MANDATES_PERCENTAGE_COLUMN_NAME,
                            self.DISTRICT_NAME_COLUMN_NAME]

            # Create DataFrame with final data
            df_results = pd.DataFrame(data=final_array, columns=column_names)
            # Unify names
            df_results = self.unify_committee_names(df_results)

            return df_results
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_votes_results_divided_by_committee' method fails - {error_message}") from error_message

    # Get list of persons who got mandate | the winners of district
    def get_district_winners(self):
        try:
            # Initialize empty array for data
            data = []
            # Get district name
            district_name = "Okręg wyborczy nr " + self.get_district_number()
            # Get elements li
            li_elements = self.map_all_elements_with_wait(By.CSS_SELECTOR, self.WINNERS_LI_ELEMENTS_CSS_SELECTOR_NAME)

            # loop through all li elements
            for li in li_elements:
                # Get committee name
                committee_name = self.map_element(li, By.TAG_NAME, "a").text
                # Get sub element li
                li_sub_elements = self.map_all_elements(li, By.TAG_NAME, "li")
                # loop through all li elements
                for sub_li in li_sub_elements:
                    # Get person name
                    person_name = self.map_element(sub_li, By.TAG_NAME, "a").text
                    # Add data t array
                    data.append([person_name, committee_name, district_name])

            # Create panda dataframe
            df_district_winners = pd.DataFrame(data, columns=[self.PERSON_COLUMN_NAME, self.COMMITTEE_COLUMN_NAME,
                                                              self.DISTRICT_NAME_COLUMN_NAME])
            # Unify names
            df_district_winners = self.unify_committee_names(df_district_winners)

            return df_district_winners
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_district_winners' method fails - {error_message}") from error_message

    # Get votes results divided by persons | Get list of all party members and theirs votes
    def get_votes_results_divided_by_person(self) -> pd.DataFrame:
        try:
            # Initialize empty array for data
            data = []
            # Get district name
            district_name = "Okręg wyborczy nr " + self.get_district_number()

            # Get all web element of tables with details votes
            committee_details_tables = self.map_all_elements_with_wait(By.CLASS_NAME,
                                                                       self.COMMITTEE_DETAILS_TABLES_CLASS_NAME)

            # loop through all committees
            for committee_element in committee_details_tables:
                # get element h5
                h5_element = self.map_element(committee_element, By.TAG_NAME, "h5")

                # if class name is strikeout committee is disabled | get next one
                if h5_element.get_attribute("class") == "strikeout":
                    continue

                # Get committee name
                committee_name = self.map_element(h5_element, By.TAG_NAME, "a").text

                # Get tbody element
                element_tbody = self.map_element(committee_element, By.TAG_NAME, "tbody")
                tbody_rows = self.map_all_elements(element_tbody, By.TAG_NAME, "tr")

                # loop through all persons on list
                for row in tbody_rows:
                    # if class name is strikeout person is disabled | go to next one
                    if row.get_attribute("class") == "strikeout":
                        continue

                    # Get td elements = columns
                    column = self.map_all_elements(row, By.TAG_NAME, "td")
                    # Get details
                    position_on_list = int(column[0].text)
                    person_name = column[1].text
                    votes_number = int(column[2].text.replace(" ", ""))

                    # Create current array
                    current_array = [person_name, position_on_list, votes_number, committee_name, district_name]
                    # Add to array
                    data.append(current_array)

            # Column names
            column_names = [self.PERSON_COLUMN_NAME, self.POSITION_ON_LIST_COLUMN_NAME,
                            self.VOTES_NUMBER_COLUMN_NAME,
                            self.COMMITTEE_COLUMN_NAME, self.DISTRICT_NAME_COLUMN_NAME]
            # Create panda dataframe
            df_committee_details = pd.DataFrame(data, columns=column_names)
            # Unify names
            df_committee_details = self.unify_committee_names(df_committee_details)

            return df_committee_details
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_votes_results_divided_by_person' method fails - {error_message}")

    # Get links to each district details information
    def get_electoral_districts_links(self) -> pd.DataFrame:
        try:
            # Initialize empty array for data
            data = []

            # Get Rows - All electorals districts
            rows_li = self.map_all_elements_with_wait(By.CSS_SELECTOR, self.DISTRICT_LINKS_CSS_SELECTOR_NAME)

            # For every electoral district in rows_li
            for row in rows_li:
                electoral_district_link = row.get_attribute("href")
                electoral_district_name = row.text

                # Create current array
                current_array = [electoral_district_name, electoral_district_link]
                # Add to array
                data.append(current_array)

            # Column names
            column_names = [self.DISTRICT_NAME_COLUMN_NAME, self.DISTRICT_LINK_COLUMN_NAME]
            # Create panda dataframe
            df_table = pd.DataFrame(data, columns=column_names)

            return df_table
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_electoral_districts_links' method fails - {error_message}")

    #### advanced methods ##############################################################################################
