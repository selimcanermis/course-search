from encodings import utf_8
from operator import iadd
import time
from numpy import sort
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

#headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
PATH = (r'C:\Program Files\chromedriver.exe')
delay = 15 

class Udemy:
    def __init__(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')


        #s = Service('C:\\Program Files\\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=PATH, options=options)
        self.home_url = "https://www.udemy.com/"

        self.course_rows = []

        sort_type =  self.selectSortType()
        self.scrap(sort_type, driver)
        driver.quit

    def scrap(self, sort_type, driver):
        for page_number in range(1,3):
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
                courses = course_list.find_all('div', {'class': 'course-card--container--1QM2W course-card--large--2aYkn'})

                for course in courses:
                    course_url = '{0}{1}'.format('https://www.udemy.com', course.find('a')['href'])
                    course_title = course.find('a').text
                    course_headline = course.find("p",{"class": "udlite-text-sm course-card--course-headline--2DAqq"}).text.strip()
                    author = course.find("div", {"class": "course-card--instructor-list--nH1OC"}).text.strip()
                    course_rating = course.find_all("span", {"class": "udlite-sr-only"})[1].text.strip()
                    number_of_ratings = course.find("span", {"class": "udlite-heading-sm star-rating--rating-number--2o8YM"}).text.strip()
                    #print(number_of_ratings)
                    course_detail = course.find_all('span', {'class':'course-card--row--29Y0w'})
                    course_length = course_detail[0].text
                    number_of_lectures = course_detail[1].text
                    difficulity = course_detail[2].text         

                    self.course_rows.append(
                        [course_url, course_title, course_headline, author, course_rating, number_of_ratings, course_length, number_of_lectures, difficulity]               
                    )

        columns = ["url","Course Title","Course Headline","Author","Course Rating","Rating","Course Length","Number of Lessons","Difficulity"]
        df = pd.DataFrame(data=self.course_rows, columns=columns)
        #df.to_csv('Udemy Free Courses.csv', index=False, sep='\t', encoding='utf-8')
        df.to_excel(f'Udemy Free Courses - ({sort_type}).xlsx', index=False)
        print(df)


    def selectSortType(self):
        self.sort_type = input("1-Recommended\n2-Popularity\n3-Newest\n4-Highest Rated\n0-Exit\n\nPlease select one: ")
        if (self.sort_type=="1"):
            self.sort_type = "recommended"
        elif (self.sort_type=="2"):
            self.sort_type = "popularity"
        elif (self.sort_type=="3"):
            self.sort_type = "newest"
        elif (self.sort_type=="4"):
            self.sort_type = "highest-rated"
        else:
            sort_type = "exit"
        return self.sort_type 

udemy_course = Udemy()

#! MENU SCRIPT YAZILACAK

#! FREE COURSE

#! KELLİMEYE GÖRE ARAMA YAPILACAK

#! TR - ENG - ALL SEÇMELİ OLACAK