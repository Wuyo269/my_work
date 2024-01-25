

from framework import FrameWork
from flashscore import FlashScore



# Create instance of FrameWork
framework_instance = FrameWork()
config_dict = framework_instance.config_dict

#Initial Values
webdriver_path = config_dict["webdriver_path"]
url = r"https://www.flashscore.pl/pilka-nozna/hiszpania/laliga"

# Create Instance
flashscore_instance = FlashScore()

# Open url
flashscore_instance.open_url(url, webdriver_path)

# Get data from table
df_table = flashscore_instance.get_main_table_data()


