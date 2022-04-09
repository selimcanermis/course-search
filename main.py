from encodings import utf_8
from operator import iadd
import time
import pandas as pd # pip install pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
#import requests

#headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
"""
options = FirefoxOptions()
options.add_argument("--headless")
"""

PATH = (r'C:\Program Files\chromedriver.exe')
#PATH = (r'C:\Program Files\geckodriver.exe')

s = Service('C:\\Program Files\\chromedriver.exe')
driver = webdriver.Chrome(executable_path=PATH, options=options)
#driver = webdriver.Firefox(executable_path=PATH, options=options)
delay = 15 

home_url = "https://www.udemy.com/"
udemy_url = "https://www.udemy.com/courses/free/?lang=tr&p=1&sort=popularity"

driver.get(udemy_url)
#time.sleep(10)
#print(driver.title)
#time.sleep(10)


def extract_text(soup_obj, tag, attribute_name, attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text().strip() if soup_obj.find(tag, {attribute_name: attribute_value}) else ''
    return txt

course_rows = []

sort_type = 'popularity'
for page_number in range(1,2):
    page_url = f'https://www.udemy.com/courses/free/?lang=tr&p={page_number}&sort={sort_type}'
    driver.get(page_url)
    time.sleep(5)
    try:
        WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME,'course-list--container--3zXPS')))
    except TimeoutException:
        print('Loading exceeds delay time')
        break
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})
        #courses = course_list.find_all('a', {'class': 'udlite-custom-focus-visible browse-course-card--link--3KIkQ'})
        courses = course_list.find_all('div', {'class': 'course-card--container--1QM2W course-card--large--2aYkn'})
        print("girdim else")
        print(course_list)
        print(courses)

        for course in courses:
            print("girdim for")
            course_url = '{0}{1}'.format('https://www.udemy.com', course.find('a')['href'])
            course_title = course.select('div[class*="course-card--course-title"]')[0].text
            course_headline = extract_text(course, 'p', 'data-purpose', 'safely-set-inner-html:course-card:course-headline')            
            author = extract_text(course, 'div', 'data-purpose', 'safely-set-inner-html:course-card:visible-instructors')
            course_rating = extract_text(course, 'span', 'data-purpose', 'rating-number')
            number_of_ratings = extract_text(course, 'span', 'class', 'udlite-text-xs course-card--reviews-text--12UpL')[1:-1]
            course_detail = course.find_all('span', {'class':'course-card--row--1OMjg'})
            course_length = course_detail[0].text
            number_of_lectures = course_detail[1].text
            difficulity = course_detail[2].text

            course_rows.append(
                [course_url, course_title, course_headline, author, course_rating, number_of_ratings, course_length, number_of_lectures, difficulity]               
            )


print(course_rows)


driver.quit



"""
try:
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME,'course-list--container--3zXPS')))
    driver.save_screenshot("udemy.png")
except TimeoutException:
    print('Loading exceeds delay time')
    #break
#! html alınca else blogunu kaldır
else:
    with open('page_markup.html','w',encoding='utf_8') as file:
        file.write(driver.page_source)
finally:
    driver.quit
"""














#request = requests.get(login_url, headers=headers_driver)

#* FREE COURSES
newest_url = "https://www.udemy.com/courses/free/?lang=tr&sort=newest"
recommended_url = "https://www.udemy.com/courses/free/?lang=tr&sort=recommended"
udemy_url = "https://www.udemy.com/courses/free/?lang=tr&p=1&sort=popularity"
popular_url2 = "https://www.udemy.com/courses/free/?lang=tr&p=2&sort=newest"

page_number = 1
sort_type = 'popularity'
page_url = f'https://www.udemy.com/courses/free/?lang=tr&p={page_number}&sort={sort_type}'