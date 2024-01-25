import os.path

import pandas as pd
import pathlib

from Libraries.framework import FrameWork
from Libraries.wybory_gov import WyboryGov


def save_df_to_excel(file_path: str, dict_of_dataframes: dict)-> None:
    """
    Save all DataFrames in dictionary to Excel File.
    If Excel file/ sheet already exists append data.
    If Excel file/ sheet does not exist create new file/ sheet.
    """
    # If excel name does not have extenstion - add it
    if not str(file_path).endswith(".xlsx"):
        file_path += ".xlsx"
    # 1. Create a pandas excel writer instance and name the Excel file
    if (os.path.exists(file_path)):
        # Append mode
        xlwriter = pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay')
    else:
        # Create new file
        xlwriter = pd.ExcelWriter(file_path)

    # 2. Write each dataframe to a worksheet with a name
    for item in dict_of_dataframes:
        #### If excel exist read sheet as DataTable
        ###if (os.path.exists(file_path)):
        try:
            df_current = pd.read_excel(xlwriter, sheet_name=item)
        except Exception as error_message:
            # Crate empty dataframe
            df_current = pd.DataFrame()
        df_item = dict_of_dataframes[item]

        # Merge two data frames
        df_concat = pd.concat([df_item, df_current])
        df_concat.to_excel(xlwriter, sheet_name=item, index=False)

    # 3. Close the instance
    xlwriter.close()


def save_links_to_districts(config_dict: dict = None) -> None:
    """
    # Save link of each district to Excel file
    """
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            year = int(config_dict["election_year"])
            webdriver_path = str(config_dict["webdriver_path"])
            url_wybory_gov_links = str(config_dict["url_wybory_gov_links"])
            url_wybory_gov_links = url_wybory_gov_links.replace("###YEAR###", str(year))
            district_links_file_name = str(config_dict["district_links_file_name"])
            election_data_folder_path = os.path.join(os.path.dirname(__file__), '..',
                                                     framework_instance.INPUT_FOLDER_PATH, str(year))
            disrtrict_links_file_path = os.path.join(election_data_folder_path, district_links_file_name)

        # Process ##########################################################################################################
        if True:
            # Create instance of wybory gov
            wybory_gov_instance = WyboryGov()

            # Open url
            wybory_gov_instance.open_url(url_wybory_gov_links, webdriver_path)

            # Get links to districts
            df_districts_links = wybory_gov_instance.get_electoral_districts_links()

            # Make directory
            pathlib.Path(election_data_folder_path).mkdir(exist_ok=True)

            # Save to excel
            df_districts_links.to_excel(disrtrict_links_file_path, sheet_name="df_districts_links", index=False)

    except Exception as error_message:
        raise Exception(f"Method 'save_links_to_districts' fails - {error_message}") from error_message


def save_data_from_all_districts(config_dict: dict = None, one_item: bool = False) -> None:
    """
    Save data from all district to seperate file
    Merge all data in one merge file
    Input for this method is file with links to all districts
    """
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            year = int(config_dict["election_year"])
            webdriver_path = str(config_dict["webdriver_path"])
            district_links_file_name = str(config_dict["district_links_file_name"])
            election_data_folder_path = os.path.join(os.path.dirname(__file__), '..',
                                                     framework_instance.INPUT_FOLDER_PATH, str(year))
            district_links_file_path = os.path.join(election_data_folder_path, district_links_file_name)
            merged_file_path = os.path.join(election_data_folder_path, ("results_" + str(year) + ".xlsx"))

        # Process ##########################################################################################################
        if True:
            # Create instance of wybory gov
            wybory_gov_instance = WyboryGov()

            # Load district links from Excel
            df_districts_links = pd.read_excel(district_links_file_path)

            # loop through all rows
            for id, row in df_districts_links.iterrows():
                district_name = row[wybory_gov_instance.DISTRICT_NAME_COLUMN_NAME]
                district_url = row[wybory_gov_instance.DISTRICT_LINK_COLUMN_NAME]

                # Open url
                wybory_gov_instance.open_url(district_url, webdriver_path)
                # Wait until page is loaded
                wybory_gov_instance.wait_until_web_is_loaded()

                # Get DataFrame Data
                df_district_winners = wybory_gov_instance.get_district_winners()
                df_district_mandates_number = wybory_gov_instance.get_district_mandates_number_df()
                df_committee_results = wybory_gov_instance.get_votes_results_divided_by_committee()
                df_person_results = wybory_gov_instance.get_votes_results_divided_by_person()

                # Calc district file path
                district_file_path = os.path.join(election_data_folder_path, (district_name + ".xlsx"))

                # Create empty dictionary
                dict_district_df = {}
                # Assign data to dictionary
                dict_district_df["df_district_winners"] = df_district_winners
                dict_district_df["df_district_mandates_number"] = df_district_mandates_number
                dict_district_df["df_committee_results"] = df_committee_results
                dict_district_df["df_person_results"] = df_person_results

                # Save data to specified Excel for this district
                save_df_to_excel(district_file_path, dict_district_df)

                # Save data to merged file
                save_df_to_excel(merged_file_path, dict_district_df)

                # If one item = True end code. Used for testing
                if one_item:
                    break

    except Exception as error_message:
        raise Exception(f"Method 'save_links_to_districts' fails - {error_message}") from error_message
