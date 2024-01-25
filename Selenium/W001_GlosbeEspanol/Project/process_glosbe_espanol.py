'''
Description
Put the description of your process
'''
import datetime
import logging
import pandas as pd
import os

# library of my custom methods
from Libraries.framework import FrameWork
from Libraries import utilities
from Libraries.queue_file import QueueFile
from Libraries.glosbe import Glosbe


# Delete previous output file
def process_preparation(config_dict: dict) -> None:
    try:
        logging.info(f"Method process_preparation started")
        # Get config if not provided
        if len(config_dict) > 0:
            # Create instance of FrameWork
            framework_instance = FrameWork()
            config_dict = framework_instance.config_dict

        # Get output file path
        output_file_path = config_dict["output_file_path"]

        # Delete current output file
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

    except Exception as error_message:
        raise Exception(f"Method 'process_preparation'  fails - {error_message}") from error_message


# Get input for process and upload to queue
# input for this process are spanish verbs
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
            # Create queue instance
            queue_instance = QueueFile()

            # Read input file
            df_input = pd.read_excel(input_file_path)

            # Add default columns
            df_input = queue_instance.add_default_columns_to_df(df_input)
            # Add verb to data column
            df_input[queue_instance.DATA_COLUMN_NAME] = df_input[["Verb", "status"]].agg(';'.join, axis=1)
            # Create reference
            df_input[queue_instance.REFERENCE_COLUMN_NAME] = df_input["Verb"].apply(
                lambda x: f"{x}_{datetime.datetime.today().strftime('%d%m%Y')}")
            # Delete column 'Verb'
            df_input.drop("Verb", inplace=True, axis=1)

            # Add to queue
            queue_instance.queue_add_new_items(df_input)
    except Exception as error_message:
        raise Exception(f"Method 'process_input' fails - {error_message}") from error_message


# Get information about verb in spanish
def process_item(verb: str = "ver", config_dict: dict = None) -> None:
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
            url_glosbe = config_dict["url_glosbe"]
            webdriver_path = config_dict["webdriver_path"]
            output_file_path = config_dict["output_file_path"]

            # Create full url
            url_glosbe = url_glosbe + "/" + verb

        # Process ##########################################################################################################
        if True:
            # Create glosbe instance
            glosbe_instance = Glosbe()

            # Open Url
            glosbe_instance.open_url(url_glosbe, webdriver_path)

            # Click in the verb element to show details
            glosbe_instance.click_verb_element()
            # Click in the 'more' button to expand details
            glosbe_instance.click_more_button()
            # Get conjugation table
            df_conjugation_table = glosbe_instance.get_conjugation_table()

            # Save data in output file
            utilities.append_to_excel(output_file_path, df_conjugation_table)

            logging.info(f"{log_marker} - End")
    except Exception as error_message:
        raise Exception(f"Method 'process_item' fails - {error_message}") from error_message


# There is no need to do additional action with output
def process_output() -> None:
    pass


def process()-> None:
    # Create instance of FrameWork
    framework_instance = FrameWork()
    # Create instance of Queue
    queue_instance = QueueFile()
    # Get config dictionary
    config_dict = framework_instance.config_dict

    # Make preparation before process started
    process_preparation(config_dict)

    # Add new items to Queue_Folder
    if True:
        process_input(config_dict)

    # Get number of pending items
    pending_items = queue_instance.queue_get_all_pending_items().shape[0]
    print(f"Items to process: {pending_items}")

    # Get new item
    new_item = queue_instance.queue_get_next_item()
    processed_items = 0

    # Do while there is new item
    while new_item.shape[0] > 0:
        try:
            index = new_item.index[0]
            processed_items += 1
            print(
                f"Process item '{new_item[queue_instance.REFERENCE_COLUMN_NAME].iloc[0]}' {processed_items}/{pending_items}. Progress: {format(processed_items / pending_items, '.2%')}")
            verb = new_item[queue_instance.DATA_COLUMN_NAME].iloc[0].split(";")[0]
            # Download item
            process_item(verb, config_dict)
            # Update status - completed
            queue_instance.queue_update_status(index, new_status=queue_instance.COMPLETED_STATUS_NAME)
        except Exception as error_message:
            # Update status - error
            queue_instance.queue_update_status(index, new_status=queue_instance.ERROR_STATUS_NAME,
                                               error_message=error_message)
        # Get new item
        new_item = queue_instance.queue_get_next_item()

    # Get duration time
    framework_instance.get_process_time()

# # DEBUG - Local testing
# if __name__ == "__main__":
#    process()
