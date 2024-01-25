import pandas as pd
import os
import datetime
import logging



# Constant Values ###################################################################################################
QUEUE_COLUMNS_NAMES = ['reference', 'status', 'description', 'employee_name', 'excel_file', 'month', 'web_row_position']
QUEUE_FILE_PATH = "Queue_Folder/Queue.xlsx"
STATUS_COLUMN_NAME = "status"
ERROR_MESSAGE_COLUMN_NAME = "description"
LOGGING_MARKER_QUEUE = "Queue:"

#Calc Absolute Path
QUEUE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', QUEUE_FILE_PATH))
# Constant Values ###################################################################################################

class QueueFile():
    # Initialize instance
    def __init__(self) -> None:
        self.create_queue_file()
        pass
    # Get all items from queue
    # Status filter is optional
    def queue_get_all_items(self,filter_status: str = None) -> object:
        try:
            # Read queue from file
            df_data = pd.read_excel(QUEUE_FILE_PATH, keep_default_na=False, index_col=0)
            #If filter is not set up get all items
            if filter_status is not None:
                df_data = df_data[df_data[STATUS_COLUMN_NAME] == filter_status]
            return df_data
        except Exception as error_message:
            raise Exception(f"queue_get_all_items method fails - {error_message}") from error_message

    #Get next item for status pending
    def queue_get_next_item(self,filter_status: str = "Pending") -> object:
        try:
            # Read queue from file
            df_data = self.queue_get_all_items(filter_status)
            # Get only first
            df_data = df_data.head(1)
            return df_data
        except Exception as error_message:
            raise Exception(f"queue_get_next_item method fails - {error_message}") from error_message


    # Update status based on Index
    def queue_update_status(self,index: int, new_status: str = "", error_message: str = ""):
        try:
            # Read queue from file
            df_data = self.queue_get_all_items()
            # Update status in dataframe
            df_data.loc[index, STATUS_COLUMN_NAME] = new_status
            # Update error message in dataframe
            df_data.loc[index, ERROR_MESSAGE_COLUMN_NAME] = error_message
            # Save data in queue file
            df_data.to_excel(QUEUE_FILE_PATH)
            logging.info(f"{LOGGING_MARKER_QUEUE} Item status updated - {new_status}")
        except Exception as error_message:
            logging.info(f"{LOGGING_MARKER_QUEUE} Item status not updated - {new_status}")
            raise Exception(f'queue_update_status method fails - Unable to change status - {error_message}') from error_message


    # Check if item exists in queue
    def queue_check_if_item_in_queue(self, unique_value: str, unique_column_name: str, filter_status: str = "Pending") -> bool:
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
            raise Exception(f'queue_check_if_item_in_queue method fails - {error_message}') from error_message


    # Add Items to Queue_Folder
    def queue_add_new_items(self,df_new_items: object, unique_column_name: str) -> int:
        try:
            # Read queue from file
            df_queue = self.queue_get_all_items()
            # Add column Exist which will show if item already in queue
            df_new_items = pd.merge(df_new_items, df_queue[unique_column_name], on=[unique_column_name], how='left',
                                    indicator='Exist')
            # Filter only new items
            df_new_items = df_new_items[df_new_items["Exist"] == "left_only"]
            # Delete column 'Exists'
            df_new_items.drop('Exist', inplace=True, axis=1)
            # All new items has status Pending
            df_new_items[STATUS_COLUMN_NAME] = "Pending"
            # Add items to df queue
            df_queue = pd.concat([df_queue, df_new_items], axis=0)

            # Save df to Excel file
            df_queue.to_excel(QUEUE_FILE_PATH)
            # Return number of added items
            return df_new_items.shape[0]
        except Exception as e:
            raise Exception(f'Queue_Folder: Unable to add new items - {e}') from e


    # Check if queue file exist
    def check_if_queue_file_exist(self) -> bool:
        try:
            file_exist = os.path.exists(QUEUE_FILE_PATH)
            return file_exist
        except Exception as error_message:
            raise Exception(f'check_if_queue_file_exist method fails - {error_message}') from error_message

    # Create empty queue file
    def create_queue_file(self):
        try:
            # Check if queue file exist, if not -> create a new one
            if not self.check_if_queue_file_exist():
                # Create dataframe
                df_queue = pd.DataFrame(columns=[QUEUE_COLUMNS_NAMES])
                # Save df to excel
                df_queue.to_excel(QUEUE_FILE_PATH)
        except Exception as error_message:
            raise Exception(f'create_queue_file method fails - {error_message}') from error_message

