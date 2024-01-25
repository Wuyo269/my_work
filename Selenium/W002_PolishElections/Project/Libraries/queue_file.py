import pandas as pd
import os
import datetime
import logging


class QueueFile():
    # Initialize instance
    def __init__(self) -> None:
        self.create_queue_file()
        pass

    # Constants
    QUEUE_FILE_PATH = "Queue_Folder/Queue.xlsx"
    QUEUE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', QUEUE_FILE_PATH))
    LOGGING_MARKER = "QUEUE:"

    # Default queue column names
    REFERENCE_COLUMN_NAME = "reference"
    STATUS_COLUMN_NAME = "status"
    DESCRIPTION_COLUMN_NAME = "description"
    DATA_COLUMN_NAME = "data"
    QUEUE_COLUMNS_NAMES = [REFERENCE_COLUMN_NAME, STATUS_COLUMN_NAME, DESCRIPTION_COLUMN_NAME, DATA_COLUMN_NAME]

    # Default queue statuses
    PENDING_STATUS_NAME = "pending"
    ERROR_STATUS_NAME = "error"
    COMPLETED_STATUS_NAME = "completed"

    # Add default columns that always need to be in Queue file
    def add_default_columns_to_df(self, df_data: pd.DataFrame) -> pd.DataFrame:
        try:
            df_data[self.REFERENCE_COLUMN_NAME] = ""
            df_data[self.STATUS_COLUMN_NAME] = self.PENDING_STATUS_NAME
            df_data[self.DESCRIPTION_COLUMN_NAME] = ""
            df_data[self.DATA_COLUMN_NAME] = ""
            return df_data
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'add_default_columns_to_df' fails - {error_message}") from error_message

    # Get all items from queue
    def queue_get_all_items(self, filter_status: str = None) -> pd.DataFrame:
        try:
            # Read queue from file
            df_data = pd.read_excel(self.QUEUE_FILE_PATH, keep_default_na=False, index_col=0)
            # If filter is not set up get all items
            if filter_status is not None:
                df_data = df_data[df_data[self.STATUS_COLUMN_NAME] == filter_status]
            return df_data
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_get_all_items' fails - {error_message}") from error_message

    # Get all items from queue
    def queue_get_all_pending_items(self) -> pd.DataFrame:
        try:
            # Read queue from file, get only pending items
            df_data = self.queue_get_all_items(filter_status=self.PENDING_STATUS_NAME)
            return df_data
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_get_all_pending_items' fails - {error_message}") from error_message

    # Get next item for status pending
    def queue_get_next_item(self, filter_status: str = PENDING_STATUS_NAME) -> pd.DataFrame:
        try:
            # Read queue from file
            df_data = self.queue_get_all_items(filter_status)
            # Get only first
            df_data = df_data.head(1)

            # Log number of items
            if len(df_data) == 1:
                logging.info(f"{self.LOGGING_MARKER} Item started - {df_data[self.REFERENCE_COLUMN_NAME].iloc[0]}")
            else:
                logging.info(f"{self.LOGGING_MARKER} No items in Queue")
            return df_data
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_get_next_item' fails - {error_message}") from error_message

    # Update status based on Index
    def queue_update_status(self, index: int, new_status: str = "", error_message: str = ""):
        try:
            # Read queue from file
            df_data = self.queue_get_all_items()
            # Update status in dataframe
            df_data.loc[index, self.STATUS_COLUMN_NAME] = new_status
            # Update error message in dataframe
            df_data.loc[index, self.DESCRIPTION_COLUMN_NAME] = error_message
            # Save data in queue file
            df_data.to_excel(self.QUEUE_FILE_PATH)
            logging.info(f"{self.LOGGING_MARKER} Item status updated - {new_status}")
        except Exception as error_message:
            logging.info(f"{self.LOGGING_MARKER} Item status not updated - {new_status}")
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_update_status' fails - Unable to change status - {error_message}") from error_message

    # Check if item exists in queue
    def queue_check_if_item_in_queue(self, unique_value: str, unique_column_name: str,
                                     filter_status: str = PENDING_STATUS_NAME) -> bool:
        try:
            # Read queue from file
            df_data = self.queue_get_all_items(filter_status)
            # Filter df based on provided criteria
            df_item = df_data[df_data[unique_column_name] == unique_value]
            # Check if item exist and return bool
            if df_item.shape[0] == 0:
                return False
            else:
                return True
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_check_if_item_in_queue' fails - {error_message}") from error_message

    # Add Items to Queue_Folder
    def queue_add_new_items(self, df_new_items: pd.DataFrame) -> int:
        try:
            # Read queue from file
            df_queue = self.queue_get_all_items()
            # Add column exist which will show if item already in queue
            df_new_items = pd.merge(df_new_items, df_queue[self.REFERENCE_COLUMN_NAME], on=[self.REFERENCE_COLUMN_NAME],
                                    how='left',
                                    indicator='Exist')
            # Filter only new items
            df_new_items = df_new_items[df_new_items["Exist"] == "left_only"]
            # Delete column 'Exists'
            df_new_items.drop('Exist', inplace=True, axis=1)
            # Add items to df queue
            df_queue = pd.concat([df_queue, df_new_items], axis=0)

            # Save df to Excel file
            df_queue.to_excel(self.QUEUE_FILE_PATH)
            logging.info(f"{self.LOGGING_MARKER} Items added to Queue - {str(df_new_items.shape[0])}")
            # Return number of added items
            return df_new_items.shape[0]
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'queue_add_new_items' fails - {error_message}") from error_message

    # Check if queue file exist
    def check_if_queue_file_exist(self) -> bool:
        try:
            file_exist = os.path.exists(self.QUEUE_FILE_PATH)
            return file_exist
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'check_if_queue_file_exist fails - {error_message}") from error_message

    # Create empty queue file
    def create_queue_file(self):
        try:
            # Check if queue file exist, if not -> create a new one
            if not self.check_if_queue_file_exist():
                # Create dataframe
                df_queue = pd.DataFrame(columns=[self.QUEUE_COLUMNS_NAMES])
                # Save df to excel
                df_queue.to_excel(self.QUEUE_FILE_PATH)
        except Exception as error_message:
            raise Exception(
                f"{self.LOGGING_MARKER} Method 'create_queue_file' fails - {error_message}") from error_message
