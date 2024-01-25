from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("start-maximized")

webdriver_service = Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(options=options, service=webdriver_service)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)
tooltip1 = "div[role='tooltip'] .MuiTypography-root.MuiTypography-body1"
tooltip2 = "div[role='tooltip'] .MuiTypography-root.MuiTypography-body2"

url = "https://idsc.cidadessustentaveis.org.br/rankings"

driver.get(url)

desired_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SdgPerformanceBar__Block-sc-1yl1q71-2.fBQLcJ')))
actions.move_to_element(desired_elem).perform()
tt1_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip1))).text
tt2_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip2))).text
print(tt1_text)
print(tt2_text)

driver.findElement(By.xpath("//input[@id='shub46']"))