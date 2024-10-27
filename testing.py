from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def perform_search(q):
    service = Service(ChromeDriverManager().install())
 
    driver = webdriver.Chrome(service=service)

    # Performing google search
    driver.get("https://www.google.com/")
    bar = driver.find_element(By.CLASS_NAME, "gLFyf")
    bar.send_keys(f"{q} Weather", Keys.RETURN)

    # print((driver.find_element(By.ID, "wob_tm")).text)
    # print((driver.find_element(By.ID, "wob_pp")).text)
    # print((driver.find_element(By.ID, "wob_ws")).text)
    # print((driver.find_element(By.ID, "wob_dc")).text)

# new
    wait = WebDriverWait(driver, 10)
    anchor = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "weather.com")))
    anchor.click()
    x = (wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'TwcSunChart--datesContainer--dM3Nk')))).text
    print(x)
    driver.quit

# Pressure--pressureWrapper--H9A+x


perform_search("mumbai")