import requests
from bs4 import BeautifulSoup
import json

headers_driver = {'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


class Udemy:
    def __init__(self):
        self.keyword = self.keywordInput()

        self.keyword = self.keyword.replace('İ', "i").lower()
        tr_alphabet = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
        self.keyword = self.keyword.translate(tr_alphabet)

        source = "https://www.udemy.com/"
        self.url = f"https://www.udemy.com/courses/search/?src=ukw&q=python"
        request   = requests.get(self.url, headers=headers_driver)

        soup = BeautifulSoup(request.content, "lxml")
        courses = soup.find('div', {'class':'course-directory--container--5ZPhr'})

        data_json = {"source": source, 'data' : []}

        try:
            print("in try block")
            print(courses)
            print(soup.title)
            for c in courses.findAll("div", {"class":"course-card--main-content--2XqiY course-card--has-price-text--1c0ze"}):
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
        self.keywordI = input("Aranacak kelime: ")

        return self.keywordI

    

course = Udemy()

#course-card--main-content--2XqiY course-card--has-price-text--1c0ze


