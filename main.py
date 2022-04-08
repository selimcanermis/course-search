from encodings import utf_8
import time
import pandas as pd # pip install pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
#import requests

#headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

option = ChromeOptions()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--disable-notifications")


PATH = (r'C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)
delay = 15 

home_url = "https://www.udemy.com/"
udemy_url = "https://www.udemy.com/courses/free/?lang=tr&p=1&sort=popularity"

driver.get(udemy_url)
time.sleep(10)
print(driver.title)
time.sleep(10)

with open('page_markup.html','w',encoding='utf_8') as file:
    file.write(driver.page_source)

sort_type = 'popularity'
for page_number in range(1,4):
    page_url = f'https://www.udemy.com/courses/free/?lang=tr&p={page_number}&sort={sort_type}'


rows = []











#request = requests.get(login_url, headers=headers_driver)

#* FREE COURSES
newest_url = "https://www.udemy.com/courses/free/?lang=tr&sort=newest"
recommended_url = "https://www.udemy.com/courses/free/?lang=tr&sort=recommended"
udemy_url = "https://www.udemy.com/courses/free/?lang=tr&p=1&sort=popularity"
popular_url2 = "https://www.udemy.com/courses/free/?lang=tr&p=2&sort=newest"

#page_number = 1
sort_type = 'popularity'
page_url = f'https://www.udemy.com/courses/free/?lang=tr&p={page_number}&sort={sort_type}'