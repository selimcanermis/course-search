import time
import pandas as pd # pip install pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import requests

headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

option = ChromeOptions()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--disable-notifications")

driver = webdriver.Chrome(chrome_options=option)

login_url = "https://www.udemy.com/"
url = f"https://www.udemy.com/courses/search/?src=ukw&q=python"
driver.get(login_url)
time.sleep(10)

#request = requests.get(login_url, headers=headers_driver)