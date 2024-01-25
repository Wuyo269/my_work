import os
import datetime
import logging
import time

import pandas as pd

'''
Start logging
Calc process time
Read Config File
'''


class FrameWork():

    # Initialize instance
    def __init__(self) -> None:
        self.config_dict = {}
        # Start time
        self.start_time = time.time()
        # Start logging
        self.start_logging()
        # Read config file
        self.read_config_file()
        self.upgrade_config_file()


    # Constants
    LOGGING_MARKER = "FRAMEWORK:"
    INPUT_FOLDER_PATH = "Data/Input"
    OUTPUT_FOLDER_PATH = "Data/Output"
    CONFIG_FILE_PATH = r"Config/Config.xlsx"
    CONFIG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONFIG_FILE_PATH))
    LOGS_FOLDER_PATH = r"Logs_Folder"
    LOGS_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', LOGS_FOLDER_PATH))

    # Read config xlsx file and return dictionary
    def read_config_file(self) -> None:
        try:
            # Read Config File
            df_config = pd.read_excel(self.CONFIG_FILE_PATH)
            # Assign values to dictionary
            for row in df_config.itertuples():
                self.config_dict[row.Asset] = row.Value
        except Exception as error_message:
            logging.info(f"df_config method fails - {error_message}")
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'read_config_file' fails - {error_message}") from error_message

    # Add calculation to config values specific for this project
    def upgrade_config_file(self) -> None:
        try:
            # This project do not require any additional calculation
            self.config_dict["input_file_path"] = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", self.INPUT_FOLDER_PATH,
                             self.config_dict["input_file_name"]))
            self.config_dict["output_file_path"] = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", self.OUTPUT_FOLDER_PATH,
                             self.config_dict["output_file_name"]))
        except Exception as error_message:
            logging.info(f"Method 'upgrade_config_file' fails - {error_message}")
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'upgrade_config_file' fails - {error_message}") from error_message

    # Start logging session
    def start_logging(self) -> None:
        try:
            # Calc log file name
            log_file_name = "Log_" + datetime.datetime.today().strftime("%d%m%Y_%H%M%S") + ".txt"
            # Calc Year and Month folder
            sub_folders = f"{datetime.datetime.today().strftime('%Y')}/{datetime.datetime.today().strftime('%m')}"
            # Calc full folder path, Main log folder + Year & month
            full_log_folder_path = os.path.join(self.LOGS_FOLDER_PATH, sub_folders)
            # Create folder if not exist
            if not os.path.exists(full_log_folder_path):
                os.makedirs(full_log_folder_path)
            # Calc full path to log file
            filename = os.path.join(full_log_folder_path, log_file_name)
            # Start logging
            logging.basicConfig(filename=filename,
                                level=logging.INFO,
                                format='%(levelname)s: %(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S',
                                force=True)
        except Exception as error_message:
            raise Exception(f"{self.LOGGING_MARKER} Method 'start_logging' fails - {error_message}") from error_message

    # Return the time of process duration
    def get_process_time(self) -> str:
        try:
            self.end_time = time.time()
            script_time = self.end_time - self.start_time
            mon, sec = divmod(script_time, 60)
            hr, mon = divmod(mon, 60)
            process_duration = '%d:%02d:%02d' % (hr, mon, sec)
            print(f"Process finished. Time: {process_duration}")
            logging.info(f"Time - {process_duration}")
            return process_duration

        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'get_process_time' fails - {error_message}") from error_message

# DEBUG
# my_instance = FrameWork()
# print("TEST")
