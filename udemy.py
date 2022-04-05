from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
import requests
from bs4 import BeautifulSoup
import json
import time

headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


class Udemy:
    def __init__(self):
        option = ChromeOptions()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-notifications")

        PATH = (r'C:\Program Files\chromedriver.exe')
        driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)


        self.keyword = self.keywordInput()

        self.keyword = self.keyword.replace('İ', "i").lower()
        tr_alphabet = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
        self.keyword = self.keyword.translate(tr_alphabet)

        source = "https://www.udemy.com/"
        self.url = "https://www.udemy.com/courses/search/?src=ukw&q=python"
        request   = requests.get(self.url, headers=headers_driver)
        
        driver.get(self.url)
        time.sleep(30)

        soup = BeautifulSoup(request.content, "lxml")
        courses = soup.find('header', {'class':'search--header-container--2-Reh'})

        data_json = {"source": source, 'data' : []}

        try:
            print("in try block")
            print(courses)
            #print(soup.title)
            #print(soup.body)
            for c in courses.findAll("div", {"class":"popper--popper--2r2To"}):
                title2 = c.find("h3").text
                print(title2)
                print("in")

                """
                isim    = bak.find('span', class_='isim').text
                adres = bak.find('div', class_='col-lg-6').text
                tarif = (None if bak.find('span', class_='text-secondary font-italic') is None else bak.find('span', class_='text-secondary font-italic').text)
                tel  = bak.find('div', class_='col-lg-3 py-lg-2').text

                data_json['data'].append({
                    'isim'        : isim,
                    'adres'     : adres,
                    'tarif'     : tarif,
                    'telefon'   : tel
                })
                """
        except AttributeError:
            pass

    
    def keywordInput(self):
        #self.keywordI = input("Aranacak kelime: ")
        self.keywordI = "python"

        return self.keywordI

    

course = Udemy()

#course-card--main-content--2XqiY course-card--has-price-text--1c0ze


