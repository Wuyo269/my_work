import pandas as pd
import os
import datetime
import logging
import time

'''
Start logging
Calc process time
Read Config File
'''

# Constant Values ###################################################################################################
CONFIG_FILE_PATH = r"Config/Config.xlsx"
LOGS_FOLDER_PATH = r"Logs_Folder"
INPUT_FOLFER_PATH = "Data/Input"
OUTPUT_FOLFER_PATH = "Data/Output"

# Calc Absolute Path
CONFIG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONFIG_FILE_PATH))
LOGS_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', LOGS_FOLDER_PATH))

# Constant Values ###################################################################################################


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

    # Read config xlsx file and return dictionary
    def read_config_file(self):
        try:
            # Read Config File
            df_config = pd.read_excel(CONFIG_FILE_PATH)
            # Assign values to dictionary
            for row in df_config.itertuples():
                self.config_dict[row.Asset] = row.Value
        except Exception as error_message:
            logging.info(f"df_config method fails - {error_message}")
            raise Exception(f"df_config method fails - {error_message}") from error_message

    # Add calculation to config values specific for this project
    def upgrade_config_file(self):
        try:
            # This project do not require any additional calculation
            self.config_dict["input_file_path"] = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", INPUT_FOLFER_PATH, self.config_dict["input_file_name"]))
            self.config_dict["output_file_path"] = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", OUTPUT_FOLFER_PATH, self.config_dict["output_file_name"]))
        except Exception as error_message:
            logging.info(f"upgrade_config_file method fails - {error_message}")
            raise Exception(f"upgrade_config_file method fails - {error_message}") from error_message

    # Start logging session
    def start_logging(self) -> None:
        try:
            # Calc log file name
            log_file_name = "Log_" + datetime.datetime.today().strftime("%d%m%Y_%H%M%S") + ".txt"
            # Calc Year and Month folder
            sub_folders = f"{datetime.datetime.today().strftime('%Y')}/{datetime.datetime.today().strftime('%m')}"
            # Calc full foldet path, Main log folder + Year & month
            full_log_folder_path = os.path.join(LOGS_FOLDER_PATH, sub_folders)
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
            raise Exception(f"start_logging method fails - {error_message}") from error_message

    # Return the time of process duration
    def get_process_time(self) -> str:
        try:
            self.end_time = time.time()
            script_time = self.end_time - self.start_time
            mon, sec = divmod(script_time, 60)
            hr, mon = divmod(mon, 60)
            return '%d:%02d:%02d' % (hr, mon, sec)
        except Exception as error_message:
            raise Exception(f"get_process_time method fails - {error_message}") from error_message

# DEBUG
#my_instance = FrameWork()
#print("TEST")
