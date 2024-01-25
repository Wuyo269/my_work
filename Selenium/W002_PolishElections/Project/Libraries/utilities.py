import datetime
import os
import time
import  pandas as pd

'''
File contains all additional method that cannot be categoried to specific file
'''

# Append dataframe to excel
def pandas_save_in_excel(file_path: str, df_data: pd.DataFrame):
    try:
        # Save data in excel
        df_data.to_excel(file_path, index=False)
    except Exception as error_message:
        raise Exception(f"Method 'append_to_excel' fails - {error_message}") from error_message


# Append dataframe to excel
def append_to_excel(file_path: str, df_data: object):
    try:
        # If excel exist read sheet as DataTable
        if (os.path.exists(file_path)):
            df_current = pd.read_excel(file_path)
        # If Excel does not exist create new empty DataFrame
        else:
            df_current = pd.DataFrame()

        # Merge two data frames
        df_concat = pd.concat([df_data, df_current])
        # Save data in excel
        df_concat.to_excel(file_path, index=False,)
    except Exception as error_message:
        raise Exception(f"Method 'append_to_excel' fails - {error_message}") from error_message


# Create Excel file name based on employee name
def create_file_name(employee_name: str) -> str:
    try:
        file_name = f'RA_{datetime.datetime.today().year}{datetime.datetime.today().month}_{employee_name.split("(")[0].replace(employee_name.split("(")[0].strip().split(" ")[-1], "").strip()}.xls'
        return file_name
    except Exception as error_message:
        raise Exception(f"create_file_name method fails - {error_message}") from error_message


# Check if file exists, wait 20 seconds
def check_if_file_exists(full_file_name: str, counter_check: int = 4, time_sleep: int = 2) -> bool:
    try:
        # Set default values
        file_exist = False
        counter = 0
        # Exit loop if file exists or it was checked 4 times
        while not (file_exist or (counter >= counter_check)):
            time.sleep(time_sleep)
            file_exist = os.path.exists(full_file_name)
            counter += 1
        return file_exist
    except Exception as error_message:
        raise Exception(f"check_if_file_exists method fails - {error_message}") from error_message


# Move file
def move_file(file_path: str, destination_path: str) -> None:
    try:
        # Move file to destination folder
        os.rename(file_path, destination_path)
        # Check if file was moved
        file_moved = check_if_file_exists(destination_path)
    except Exception as error_message:
        raise Exception(f"move_file method fails - {error_message}") from error_message

    # If file was not moved raise exception
    if not file_moved:
        raise Exception(f"move_file method fails - Unable to move file to destination {destination_path}.")


# Delete all files from folder that starts with RA
def delete_all_ra_files(folder_path: str) -> None:
    # DEBUG:
    # folder_path=r"C:\Users\mwojcik\Downloads"

    try:
        # Get list of files
        files = os.listdir(folder_path)
        for file_name in files:
            # Work only on fiels started with "RA"
            if file_name.startswith("RA"):
                # Calc full path
                filename = os.path.join(folder_path, file_name)
                # Remove file
                os.remove(filename)
    except Exception as error_message:
        raise Exception(f"delete_all_ra_files method fails - {error_message}") from error_message


# Delete all files from folder that starts with RA
def list_all_files_from_directory(folder_path: str = "") -> None:
    # DEBUG:
    if folder_path == "":
        folder_path = r"C:\Users\mwojcik\OneDrive - Sopra Steria\Desktop\AA Files"

    try:
        # Get list of files
        files = os.listdir(folder_path)
        for file_name in files:
            print(file_name)
    except Exception as error_message:
        raise Exception(f"delete_all_ra_files method fails - {error_message}") from error_message
