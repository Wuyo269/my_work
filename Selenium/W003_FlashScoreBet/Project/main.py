'''
User trigger process with this file
'''
import time

from Project import process_flashscore_bet

########################################################################################################################

if __name__ == "__main__":
    try:
        process_flashscore_bet.process()
    except Exception as error_message:
        print(str(error_message))
        time.sleep(10)
