from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

delay = 3
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options)

url = "https://www.amazon.com/progress-tracker/package/ref=oh_aui_hz_st_btn?_encoding=UTF8&itemId=jnljnvjtqlspon&orderId="

with open("orders.txt") as orders:
    for orderId in orders.readlines():
        driver.get(url+orderId)
        time.sleep(2)
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'primaryStatus')))
            status = myElem.text
            print("order: {}\n status: {}".format(orderId.strip(),  status))
        except TimeoutException:
            print("Loading took too much time!\n\n")
driver.close()
