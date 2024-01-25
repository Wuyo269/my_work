from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime

from Project.Libraries.framework import FrameWork
from test_flashscore import FlashScore
from selenium.webdriver import ActionChains

# Create instance of FrameWork
framework_instance = FrameWork()
config_dict = framework_instance.config_dict

# Initial Values
webdriver_path = config_dict["webdriver_path"]
url = r"https://www.flashscore.pl/pilka-nozna/hiszpania/laliga"
#url = r"https://www.flashscore.pl/pilka-nozna/albania/super-liga"

# Create Instance
flashscore_instance = FlashScore()

options = Options()
options.add_argument("start-maximized")

webdriver_service = Service(webdriver_path)
driver = webdriver.Chrome(options=options, service=webdriver_service)

# Open url
driver.get(url)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

element_selector = r"#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body > div:nth-child(1) > div.table__cell.table__cell--form > div.tableCellFormIcon.tableCellFormIcon--TBD._trigger_14qf7_41"
tooltip_selector = r"#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body > div:nth-child(1) > div.table__cell.table__cell--form > div:nth-child(2) > div"
desired_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector)))

tooltip_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tooltip_selector)))


desired_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element_selector)))
tooltip_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip_selector)))


driver.get(url)

desired_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element_selector)))
actions.click(desired_elem)
tt1_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip1))).text
tt2_text = wait.unt



selector = r"#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body > div:nth-child(1) > div.table__cell.table__cell--form > div:nth-child(2) > div"
selector = r'//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div/div/div[2]/div[1]/div[3]/div[2]/div'

tooltip1 = "div[role='tooltip'] .MuiTypography-root.MuiTypography-body1"

url = "https://idsc.cidadessustentaveis.org.br/rankings"


desired_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SdgPerformanceBar__Block-sc-1yl1q71-2.fBQLcJ')))
actions.move_to_element(desired_elem).perform()
tt1_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip1))).text
tt2_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip2))).text


desired_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body > div:nth-child(1) > div.table__cell.table__cell--form > div.tableCellFormIcon.tableCellFormIcon--TBD._trigger_14qf7_41 > button > span')))
actions.move_to_element(desired_elem).perform()

WebDriverWait(flashscore_instance.driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_tooltip_14qf7_5 _textLine_14qf7_17")))

item = flashscore_instance.map_element_with_wait(By.XPATH, selector)

# Get data from table
f = flashscore_instance.get_main_table_data()

# extraContent > div.extraContent__content > div > span > a:nth-child(1)

NEXT_ROUND_CSS_SELECTOR_NAME = r"#extraContent > div.extraContent__content > div > span"

next_round = flashscore_instance.map_element_with_wait(By.CSS_SELECTOR, NEXT_ROUND_CSS_SELECTOR_NAME)

# Get information abut next round
next_round_text = next_round.text
# Split next round information by ","
next_round_split = next_round_text.split(",")

# Create empty dict
dict_next_round = {}

# Loop through each next round
for game in next_round_split:
    # Delete spaces
    game = game.strip()
    # Check if first character is digit - It means it's date
    if str(game[0]).isdigit():
        # Calc next round date
        current_date_short = game[:5]
        current_date = str(datetime.date(datetime.datetime.today().year, int(current_date_short.split(".")[1]),
                                         int(current_date_short.split(".")[0])))
        # Delete date from game
        game = game[6:].strip()

    # create list of 2 teams
    teams = game.split("-")

    # Add each team to dictionary
    for team in teams:
        team = team.strip()
        #Team mights have more then 1 game. Get only the closest one
        if not team in dict_next_round:
            dict_next_round[team.strip()] = current_date

print("End")
