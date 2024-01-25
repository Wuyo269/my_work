'''
Description
Put the description of your process
'''

import os
import logging

# library of my custom methods
from Selenium.S00X_TemplateProcess.Project.Libraries.framework import FrameWork
from Selenium.S00X_TemplateProcess.Project.Libraries.queue_file import QueueFile

# Get input for process
def process_input(config_dict: dict = None) -> None:
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            input_file_path = config_dict["input_file_path"]

        # Process ##########################################################################################################
        if True:
            pass
    except Exception as error_message:
        raise Exception(f"Method 'process_input' fails - {error_message}") from error_message

# Download single Excel file
def process_item(my_Selenium_instance: object, item: object, df_employees: object,config_dict: dict = None):
    try:
        log_marker = "Process_item:"

        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            # Initial Variables from Config
            final_destination_folder_path = config_dict["final_destination_folder_path"]
            # Input current User in download fodler path
            download_folder_path = config_dict["download_folder_path"]
            download_folder_path = download_folder_path.replace("###USER###", os.getlogin())

            # Initial variables from item
            reference = item["reference"].iloc[0]
            excel_file_name = item["excel_file"].iloc[0]
            employee_number = reference.split("(")[1].split(")")[0].strip()
            # file name contains only surname. If two persons have the same surname the files names will be identical
            final_excel_file_name = excel_file_name.replace(".xls", f"_{employee_number}.xls")


        # Process ##########################################################################################################
        if True:
            logging.info("")
            logging.info(f"{log_marker} Item '{reference}' started")

            pass

            logging.info(f"{log_marker} - End")

    except Exception as error_message:
        raise Exception(f"process_item method fails - {error_message}") from error_message

# Prepare output for the process
def process_output(config_dict: dict = None) -> None:
    try:
        # if config empty read config file
        if config_dict is None:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            # Read config file
            config_dict = framework_instance.config_dict

        # Initial Values ###################################################################################################
        if True:
            input_file_path = config_dict["input_file_path"]

        # Process ##########################################################################################################
        if True:
            pass
    except Exception as error_message:
        raise Exception(f"Method 'process_output' fails - {error_message}") from error_message

def process():
    # Create instance of FrameWork
    framework_instance = FrameWork()
    # Create instance of Queue
    queue_file_instance = QueueFile()
    df_employees = None
    # Add new items to Queue_Folder
    if True:
        new_items_added = queue_file_instance.queue_add_new_items(df_employees, "reference")
        logging.info(f"Items added to Queue - {str(new_items_added)}")

    # Get number of pending items
    pending_items = queue_file_instance.queue_get_all_items(filter_status="Pending").shape[0]
    print(f"Items to process: {pending_items}")
    # Get new item
    new_item = queue_file_instance.queue_get_next_item()
    processed_items = 0

    # Do while there is new item
    while new_item.shape[0] > 0:
        try:
            index = new_item.index[0]
            processed_items += 1
            print(
                f"Process item '{new_item['excel_file'].iloc[0]}' {processed_items}/{pending_items}. Progress: {format(processed_items / pending_items, '.2%')}")

            # Download item
            queue_file_instance.queue_update_status(index, new_status="Completed")
        except Exception as error_message:
            queue_file_instance.queue_update_status(index, new_status="Error", error_message=error_message)
        # Get new item
        new_item = queue_file_instance.queue_get_next_item()

    process_duration = framework_instance.get_process_time()
    print(f"Process finished. Time: {process_duration}")
    logging.info(f"Time - {process_duration}")


# # DEBUG - Local testing
# if __name__ == "__main__":
#process()
