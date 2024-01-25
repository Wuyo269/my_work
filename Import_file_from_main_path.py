import os.path
import time
import pandas as pd
import pathlib

print(__file__)

filename = str(__file__)

while not filename.split("\\")[-1] == "W002_PolishElections":
    filename = "\\".join(filename.split("\\")[:-1])

import importlib.util
import sys
spec = importlib.util.spec_from_file_location("framework.py",
                                              r"/tensorEnv/Selenium/W002_PolishElections/Libraries/framework.py")
FrameWork = importlib.util.module_from_spec(spec)
sys.modules["framework.py"] = FrameWork
spec.loader.exec_module(FrameWork)
FrameWork = FrameWork.FrameWork

spec = importlib.util.spec_from_file_location("wybory_gov.py",
                                              r"/tensorEnv/Selenium/W002_PolishElections/Libraries/wybory_gov.py")
WyboryGov = importlib.util.module_from_spec(spec)
sys.modules["wybory_gov.py"] = WyboryGov
spec.loader.exec_module(WyboryGov)
WyboryGov = WyboryGov.WyboryGov



#from wybory_gov import WyboryGov
#from framework import FrameWork


# Save all DataFrames in dictionary to Excel File
def save_df_to_excel(excel_name: str, dict_of_dataframes: dict):
    # If excel name does not have extenstion - add it
    if not str(excel_name).endswith(".xlsx"):
        excel_name += ".xlsx"
    # 1. Create a pandas excel writer instance and name the Excel file
    xlwriter = pd.ExcelWriter(excel_name)

    # 2. Write each dataframe to a worksheet with a name
    for item in dict_of_dataframes:
        df_item = dict_of_dataframes[item]
        df_item.to_excel(xlwriter, sheet_name=item, index=False)

    # 3. Close the instance
    xlwriter.close()

# Save all DataFrames in dictionary to Excel File
def save_df_to_excel2222(file_path: str, dict_of_dataframes: dict):
    # If excel name does not have extenstion - add it
    if not str(file_path).endswith(".xlsx"):
        file_path += ".xlsx"

    if (os.path.exists(file_path)):
        # 1. Create a pandas excel writer instance and name the Excel file
        xlwriter = pd.ExcelWriter(file_path,mode='a',if_sheet_exists='overlay')
    else:
        xlwriter = pd.ExcelWriter(file_path)



    # 2. Write each dataframe to a worksheet with a name
    for item in dict_of_dataframes:
        # If excel exist read sheet as DataTable
        if (os.path.exists(file_path)):
            try:
                df_current = pd.read_excel(xlwriter, sheet_name=item)
            except Exception as error_message:
                df_current = pd.DataFrame()
        df_item = dict_of_dataframes[item]

        # Merge two data frames
        df_concat = pd.concat([df_item, df_current])
        df_concat.to_excel(xlwriter, sheet_name=item, index=False)

    # 3. Close the instance
    xlwriter.close()



# Save link of each district to Excel file
def save_links_to_districts(config_dict: dict = None, year: int = 2023) -> None:
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            webdriver_path = str(config_dict["webdriver_path"])
            url_wybory_gov_links = str(config_dict["url_wybory_gov_links"])
            url_wybory_gov_links = url_wybory_gov_links.replace("###YEAR###", str(year))
            district_links_file_name = str(config_dict["district_links_file_name"])
            disrtrict_links_file_directory = os.path.join(os.path.dirname(__file__), 'W002_PolishElections/Project',
                                                          framework_instance.INPUT_FOLDER_PATH, str(year))
            disrtrict_links_file_path = os.path.join(disrtrict_links_file_directory, district_links_file_name)

        # Process ##########################################################################################################
        if True:
            # Create instance of wybory gov
            wybory_gov_instance = WyboryGov()

            # Open url
            wybory_gov_instance.open_url(url_wybory_gov_links, webdriver_path)

            # Get links to districts
            df_districts_links = wybory_gov_instance.get_electoral_districts_links()

            # Make directory
            pathlib.Path(disrtrict_links_file_directory).mkdir(exist_ok=True)

            # Save to excel
            df_districts_links.to_excel(disrtrict_links_file_path, sheet_name="df_districts_links", index=False)

    except Exception as error_message:
        raise Exception(f"Method 'save_links_to_districts' fails - {error_message}") from error_message


# Save all DataFrames in dictionary to Excel File
def save_district_results(excel_name, dict_of_dataframes):
    # If excel name does not have extenstion - add it
    if not str(excel_name).endswith(".xlsx"):
        excel_name += ".xlsx"
    # 1. Create a pandas excel writer instance and name the Excel file
    xlwriter = pd.ExcelWriter(excel_name)
    # NB: If you don't include a file path like 'C:\Users\Ron\Desktop\File_Name.xlsx'
    # It will save to your default folder, that is,
    # where the file you're reading from is located.

    # 2. Write each dataframe to a worksheet with a name
    for item in dict_of_dataframes:
        df_item = dict_of_dataframes[item]
        append_to_excel(excel_name,df_item,item)
        #df_item.to_excel(xlwriter, sheet_name=item, index=False)

    # 3. Close the instance
    xlwriter.close()

# Append dataframe to excel
def append_to_excel(file_path: str, df_data: object, sheet_name:str):
    try:
        # If excel exist read sheet as DataTable
        if (os.path.exists(file_path)):
            try:
                df_current = pd.read_excel(file_path, sheet_name=sheet_name)
            except Exception as error_message:
                df_current = pd.DataFrame()
        # If Excel does not exist create new empty DataFrame
        else:
            df_current = pd.DataFrame()

        # Merge two data frames
        df_concat = pd.concat([df_data, df_current])
        # Save data in excel
        df_concat.to_excel(file_path, index=False,sheet_name=sheet_name)
        df_concat.to_excel()
    except Exception as error_message:
        raise Exception(f"Method 'append_to_excel' fails - {error_message}") from error_message


# Save link of each district to Excel file
def save_data_from_all_districts(config_dict: dict = None, year: int = 2023, one_item: bool = False) -> None:
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            webdriver_path = str(config_dict["webdriver_path"])
            district_links_file_name = str(config_dict["district_links_file_name"])
            disrtrict_links_file_directory = os.path.join(os.path.dirname(__file__), 'W002_PolishElections/Project',
                                                          framework_instance.INPUT_FOLDER_PATH, str(year))
            disrtrict_links_file_path = os.path.join(disrtrict_links_file_directory, district_links_file_name)
            merged_file_path = os.path.join(disrtrict_links_file_directory, ("results_"+ str(year)+".xlsx"))

        # Process ##########################################################################################################
        if True:
            # Create instance of wybory gov
            wybory_gov_instance = WyboryGov()

            # Load data from Excel
            df_districts_links = pd.read_excel(disrtrict_links_file_path)

            # loop through all rows
            for id, row in df_districts_links.iterrows():
                district_name = row[wybory_gov_instance.DISTRICT_NAME_COLUMN_NAME]
                district_url = row[wybory_gov_instance.DISTRICT_LINK_COLUMN_NAME]

                # Open url
                wybory_gov_instance.open_url(district_url, webdriver_path)
                #Wait untill page is loaded
                wybory_gov_instance.wait_until_web_is_loaded()

                # Get DataFrame Data
                df_district_winners = wybory_gov_instance.get_district_winners()
                df_district_mandates_number = wybory_gov_instance.get_district_mandates_number_df()
                df_committee_results = wybory_gov_instance.get_votes_results_divided_by_committee()
                df_person_results = wybory_gov_instance.get_votes_results_divided_by_person()

                # Calc district file path
                disrtrict_file_path = os.path.join(disrtrict_links_file_directory, (district_name + ".xlsx"))
                # Save to excel
                #df_district_winners.to_excel(disrtrict_file_path, sheet_name="df_district_winners", index=False)
               # df_committee_results.to_excel(disrtrict_file_path, sheet_name="df_committee_results", index=False)

                # Create empty dictionaryx
                dict_disctrict_df = {}
                # Assign data to dictionary
                dict_disctrict_df["df_district_winners"] = df_district_winners
                dict_disctrict_df["df_district_mandates_number"] = df_district_mandates_number
                dict_disctrict_df["df_committee_results"] = df_committee_results
                dict_disctrict_df["df_person_results"] = df_person_results

                #Save data to specified Excel for this district
                save_df_to_excel2222(disrtrict_file_path, dict_disctrict_df)

                #Save data to merged file
                save_df_to_excel2222(merged_file_path, dict_disctrict_df)


                # If one item = True end code. Used for testing
                if one_item:
                    break


    except Exception as error_message:
        raise Exception(f"Method 'save_links_to_districts' fails - {error_message}") from error_message


def merge_disctrict_data(config_dict: dict = None, year: int = 2023):
    # if config empty read config file
    if config_dict is None:
        # Create instance of FrameWork
        framework_instance = FrameWork()
        # Read config file
        config_dict = framework_instance.config_dict

    # Initial Values ###################################################################################################
    if True:
        disrtrict_links_file_directory = os.path.join(os.path.dirname(__file__), 'W002_PolishElections/Project',
                                                      framework_instance.INPUT_FOLDER_PATH, str(year))

    # Process ##########################################################################################################
    if True:
        # Get district files
        district_files = [filename for filename in os.listdir(disrtrict_links_file_directory) if
                          filename.startswith("Okręg wyborczy nr")]

        for file in district_files:
            # Calc full path
            file_path = os.path.join(disrtrict_links_file_directory, file)
            # Read current file as DataFrame
            df_district_winners_current = pd.read_excel(file_path, sheet_name="df_district_winners")
            df_district_mandates_number_current = pd.read_excel(file_path, sheet_name="df_district_mandates_number")
            df_committee_results_current = pd.read_excel(file_path, sheet_name="df_committee_results")
            df_person_results_current = pd.read_excel(file_path, sheet_name="df_person_results")




    print("")


