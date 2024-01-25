import os

import  pandas as pd

'''
File contains all additional method that cannot be categoried to specific file
'''


# Append dataframe to excel
def append_to_excel(file_path: str, df_data: object)-> None:
    """
    Append data to Excel file
    """
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
        df_concat.to_excel(file_path, index=False)
    except Exception as error_message:
        raise Exception(f"Method 'append_to_excel' fails - {error_message}") from error_message

