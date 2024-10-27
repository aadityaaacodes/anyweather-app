from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json, os

json_path = 'dataStorage.json'

def getInfo():
    with open(json_path, 'r') as jFile:
        return(json.load(jFile))

def putInfo(dumpFile):
    with open(json_path, 'w') as jFile:
        return(json.dump(dumpFile, jFile, indent=4))

def performGoogleSearch(query):
    # JSON -> Dictionary
    x = getInfo() 
    weatherData = x['weatherData']

    # Bot setup to be Headless
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")  
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument('--disable-gpu')

    # Starting selenium bot
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Performing google search
    driver.get("https://www.google.com/")
    bar = driver.find_element(By.CLASS_NAME, "gLFyf")
    bar.send_keys(f"{query} Weather", Keys.RETURN)
    driver.get_screenshot_as_file("google.png")
    
    # collecting information on page
    weatherData["temperature"] = (driver.find_element(By.ID, "wob_tm")).text
    weatherData["precipitation"] = (driver.find_element(By.ID, "wob_pp")).text
    weatherData["humidity"] = (driver.find_element(By.ID, "wob_hm")).text
    weatherData["windspeed"] = (driver.find_element(By.ID, "wob_ws")).text
    weatherData["condition"] = (driver.find_element(By.ID, "wob_dc")).text

    # Clicking button to weather.com
    wait = WebDriverWait(driver, 10)
    anchor = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "weather.com")))
    anchor.click()

    # weather.com opens
    driver.get_screenshot_as_file("weather.png")
    dawn_dusk = driver.find_elements(By.CLASS_NAME, "TwcSunChart--datesContainer--dM3Nk")
    weatherData['dawn'] = dawn_dusk[0].text
    weatherData['dusk'] = dawn_dusk[1].text

    cssSelectors = {
    "pressure" : "span[data-testid = 'PressureValue']", 
    "visibility" : "span[data-testid = 'VisibilityValue']"
    }

    weatherData['pressure'] = (driver.find_elements(By.CSS_SELECTOR, "span[data-testid = 'PressureValue']"))[0].text
    weatherData['visibility'] = (driver.find_elements(By.CSS_SELECTOR, "span[data-testid = 'VisibilityValue']"))[0].text

    print(weatherData["pressure"])
    print(weatherData["visibility"])

    # Shutting bot
    driver.quit

    # Dumping JSON file to save changes
    putInfo(x)

    # Deleting images
    os.remove("google.png")
    os.remove("weather.png")


# # TEST RUN:
performGoogleSearch(query="Cincinnati")
