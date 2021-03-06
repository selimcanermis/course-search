from ast import keyword
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

        lang = self.selectLanguage()
        price = self.getIsFree()
        if (price=="free"):
            sort_type =  self.selectSortType()
            page_number_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&p=1&sort={sort_type}'
            pageNumber = self.getPageNumber(driver, page_number_url)
            self.freeScrap(price, lang, pageNumber, sort_type, driver)
            driver.quit
        else:
            keyword = self.getKeyword()
            sort_type =  self.selectSortType(price)
            page_number_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&p=1&q={keyword}&sort={sort_type}&src=ukw'
            pageNumber = self.getPageNumber(driver, page_number_url)
            self.searchScrap(price, lang, pageNumber, sort_type, keyword, driver)
            driver.quit

        #page_number_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&p=1&q={keyword}&sort={sort_type}&src=ukw'
        #driver.get(page_number_url)
        #time.sleep(30)
        

    def getPageNumber(self, driver, page_number_url):
        driver.get(page_number_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #* Sayfa say??s?? 3 taneden fazla ise son sayfa span tagi i??inde yaz??l??yor.
        if(soup.find('span', {'class': 'udlite-heading-sm pagination--page--1H0A2'})):
            pageNumber = soup.find('span', {'class': 'udlite-heading-sm pagination--page--1H0A2'}).text
        #* Sayfa say??s?? 3 taneden fazla de??ilse span tagi olmuyor onun yerine a tagleri oluyor.
        elif(soup.find('div', {'class': 'pagination--container--39ouY'})):
            pageNumber = soup.find('div', {'class': 'pagination--container--39ouY'}).find_all('a')
            pageNumber= int(len(pageNumber))-2
        #* Sayfa say??s?? 1 taneyse direkt pagination divi ortadan kalk??yor.
        else:
            pageNumber = 1
        driver.quit
        
        if(int(pageNumber)<=10):
            return pageNumber
        else:
            #* e??er sayfa say??s?? 10'dan fazlaysa 3 als??n
            pageNumber = "2"
            return pageNumber

    def freeScrap(self, price, lang, pageNumber, sort_type, driver):
        for page_number in range(1,int(pageNumber)+1):
            page_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&p={page_number}&sort={sort_type}'
            print("url ald??m")
            driver.get(page_url)
            print("url girdim")
            time.sleep(4)
            try:
                print("denedim")
                WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME,'course-list--container--3zXPS')))
            except TimeoutException:
                print('Loading exceeds delay time')
                break
            else:
                print("elsedeyim")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})
                courses = course_list.find_all('div', {'class': 'course-card--container--1QM2W course-card--large--2aYkn'})
                result_number = soup.find('span', {'class':'udlite-heading-md filter-panel--item-count--2JGx3'}).text


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

        self.freeRegister(self.course_rows, lang, sort_type)

    def searchScrap(self, price, lang, pageNumber, sort_type, keyword, driver):
        kursay??s?? = 0
        print(pageNumber)
        for page_number in range(1,int(pageNumber)+1):
            print("girdim")
            print("page number: ", page_number)
            print("keyword: ", keyword)
            time.sleep(4)
            if (page_number==1):
                page_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&q={keyword}&sort={sort_type}&src=ukw'
            else:
                #page_url = f'https://www.udemy.com/courses/{price}/?lang={lang}&p={page_number}&q={keyword}&sort={sort_type}&src=ukw'
                page_url = f'https://www.udemy.com/courses/search/?lang={lang}&p={page_number}&q={keyword}&sort={sort_type}&src=ukw'
                f'https://www.udemy.com/courses/search/?lang=tr&p=2&q=sql&sort=popularity&src=ukw'
            print("url ald??m")
            print(page_url)
            driver.get(page_url)
            print("url girdim")
            time.sleep(5)
            print("bekledim")
            try:
                print("try deniyorum")
                WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME,'course-list--container--3zXPS')))
                print("try dedim durdum")
            except TimeoutException:
                print('Loading exceeds delay time')
                break
            else:
                print("elsedeyim")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})
                #courses = course_list.find_all('div', {'class': 'course-card--main-content--2XqiY course-card--has-price-text--1c0ze'})
                courses = course_list.find_all('div', {'class': 'popper--popper--2r2To'})
                #result_number = soup.find('span', {'class':'udlite-heading-md filter-panel--item-count--2JGx3'}).text


                for course in courses[:-1]:
                    course_url = '{0}{1}'.format('https://www.udemy.com', course.find('a')['href'])
                    course_title = course.find('a').text
                    course_headline = course.find("p",{"class": "udlite-text-sm course-card--course-headline--2DAqq"}).text.strip()
                    author = course.find("div", {"class": "course-card--instructor-list--nH1OC"}).text.strip()
                    course_rating = course.find_all("span", {"class": "udlite-sr-only"})[1].text.strip()
                    if( course.find("span", {"class": "udlite-heading-sm star-rating--rating-number--2o8YM"})):
                        number_of_ratings = course.find("span", {"class": "udlite-heading-sm star-rating--rating-number--2o8YM"}).text.strip()
                    else:
                        number_of_ratings = "0"
                    course_detail = course.find_all('span', {'class':'course-card--row--29Y0w'})
                    course_length = course_detail[0].text
                    number_of_lectures = course_detail[1].text
                    difficulity = course_detail[2].text

                    #* E??er g??ncel fiyat?? varsa al yoksa - ver
                    if(course.find("div", {"class": "price-text--price-part--2npPm course-card--discount-price--1bQ5Q udlite-heading-md"})):
                        current_price = course.find("div", {"class": "price-text--price-part--2npPm course-card--discount-price--1bQ5Q udlite-heading-md"})
                        if(current_price.find_all("span")[2]):
                            current_price = current_price.find_all("span")[2].text.strip()
                        else:
                            current_price = "Ucretsiz"
                    else:
                        current_price = "-"
                    
                    #* E??er indirimsiz, orijinal fiyat?? varsa al yoksa null ver
                    if(course.find("div", {"class": "price-text--price-part--2npPm price-text--original-price--1sDdx course-card--list-price--3RTcj udlite-text-sm"})):
                        orijinal_price = course.find("div", {"class": "price-text--price-part--2npPm price-text--original-price--1sDdx course-card--list-price--3RTcj udlite-text-sm"})
                        orijinal_price = orijinal_price.find_all("span")[2].text.strip()
                    else:
                        orijinal_price = "-"

                    kursay??s?? +=1
                    print(kursay??s??)
                    print(course_url)
                    print(course_title)
                    print(course_headline)
                    print(author)
                    print(course_rating)
                    print(number_of_ratings)
                    print(course_detail)
                    print(course_length)
                    print(number_of_lectures)
                    print(difficulity)
                    print(current_price)
                    print(orijinal_price)
                    print("-"*50)  


                    current_price_int = current_price[1:]
                    current_price_int = current_price_int.replace(',','.')
                    #print(current_price)
                    print('*'*50)

                    self.course_rows.append(
                        [course_url, course_title, course_headline, author, course_rating, number_of_ratings, course_length, number_of_lectures, difficulity, current_price, orijinal_price]               
                    )
                    print("fordan ????kamad??m kald??m be")
                    print(len(courses))
                print("fordan ????kt??m babac??m")
                print("kurs boyutu")
                print(len(courses))

        self.searchRegister(self.course_rows, lang, sort_type, keyword)

    def freeRegister(self, course_rows, lang, sort_type):
        free_columns = ["url","Course Title","Course Headline","Author","Course Rating","Rating","Course Length","Number of Lessons","Difficulity"]
        df = pd.DataFrame(data=self.course_rows, columns=free_columns)
        df.to_excel(f'Udemy Free ({lang}) - ({sort_type}).xlsx', index=False)
        print(df)
        print("Ba??ar??yla kaydedildi.")

    def searchRegister(self,course_rows, lang, sort_type, keyword):
        search_columns = ["url","Course Title","Course Headline","Author","Course Rating","Rating","Course Length","Number of Lessons","Difficulity","Current Price","Orijinal Price"]
        df = pd.DataFrame(data=self.course_rows, columns=search_columns)
        df.to_excel(f'Udemy-{keyword}-({lang})-({sort_type}).xlsx', index=False)
        print(df)
        print("Ba??ar??yla kaydedildi.")

    def selectSortType(self, price):
        if (price=="free"):
            self.sort_type = input("1-Recommended\n2-Popularity\n3-Newest\n4-Highest Rated\n0-Exit\n\nPlease select one: ")
        else:
            self.sort_type = input("1-Recommended\n2-Most Reviewed\n3-Newest\n4-Highest Rated\n0-Exit\n\nPlease select one: ")
        if (self.sort_type=="1"):
            self.sort_type = "recommended"
        elif (self.sort_type=="2"):
            self.sort_type = "most-reviewed"
        elif (self.sort_type=="2" and self.price=="free"):
            self.sort_type = "popularity"
        elif (self.sort_type=="3"):
            self.sort_type = "newest"
        elif (self.sort_type=="4"):
            self.sort_type = "highest-rated"
        else:
            self.sort_type = "exit"
        return self.sort_type

    def selectLanguage(self):
        self.lang = input("1-T??rk??e\n2-English\n0-Exit\n\nPlease select one: ")
        if(self.lang=="1"):
            self.lang = "tr"
        elif(self.lang=="2"):
            self.lang = "en"
        else:
            self.lang = "exit"
        return self.lang

    def getKeyword(self):
        self.keyword = input("Please enter a word: ")
        #self.keyword = keyword.replace(" ","+")

        return self.keyword

    def getIsFree(self):
        param = input("1- Free Courses\n2- Search Courses\n3- Exit\n\nPlease select one: ")
        if(param=="1"):
            self.price = "free"
        elif(param=="2"):
            self.price = "search"
        else:
            self.price = 0

        return self.price



class Patika:
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
        self.home_url = "https://app.patika.dev/paths"

        self.course_rows = []

        self.Scrap(driver)
        driver.quit()

    def Scrap(self, driver):
        page_url = f'https://app.patika.dev/paths'
        print("url ald??m")
        driver.get(page_url)
        print("url girdim")
        time.sleep(10)
        try:
            print("denedim")
            WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME,'courses-list')))
        except TimeoutException:
            print('Loading exceeds delay time')
        else:
            print("elsedeyim")
            # button = driver.find_elemnt_by_class_name('mt-4 path-list').find_all('p')[0]
            button = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div[2]/div/div[1]/div[4]/p[1]")
            button.click()
            print("t??klad??m")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            course_list = soup.find('div', {'class': 'courses-list'})
            courses = course_list.find_all('div', {'class': 'styles__SecondaryBox-sc-1y0wwe4-3 cttSQa course-box'})

            for course in courses:
                course_url = '{0}{1}'.format('https://app.patika.dev', course.find('a')['href'])
                print(course_url)
                course_title = course.find_all('h3')[1].text
                print(course_title)
                course_detail = course.find_all('p', {'class':'mb-2 about-course'})
                course_length = course_detail[0].text

                self.course_rows.append(
                    [course_url, course_title, course_length]               
                )

        self.patikaRegister(self.course_rows)

    def patikaRegister(self, course_rows):
        patika_columns = ["url","Course Title","Course Length"]
        df = pd.DataFrame(data=self.course_rows, columns=patika_columns)
        df.to_excel(f'Patika-Courses.xlsx', index=False)
        print(df)
        print("Ba??ar??yla kaydedildi.")
        print("Patika Dev Course Kayitlari")




# udemy_course = Udemy()

patika_course = Patika()





#! PAGE NUMBER RESULT/15 ??EKL??NDE DE BULUNAB??L??R

#! MENU SCRIPT YAZILACAK

#* YA??ADIK KRAL ONU DA YA??ADIK
#TODO FREE COURSE

#! KELL??MEYE G??RE ARAMA YAPILACAK
#! KEL??MEYE G??RE ARAMADA F??YAT SATIRI DA EKLENECEK
#? ESK?? F??YAT (??ND??R??M ??NCES??) D??KKATE ALINACAK MI?????
#! KEL??MEYE G??RE ARAMADA 10.000+ SONU?? D??ND??R??YOR 89+ SAYFA !!!!!
#! TOP 50 YAPILAB??L??R


#* YA??ADIK KRAL ONU DA YA??ADIK
#TODO TR - ENG - ALL SE??MEL?? OLACAK


"""
#! HEPS?? (DEFAULT) EN ALAKALI SIRALAMA ??LE SIRALANMI??TIR.
#? tek kelime arama
#* taslak url 
#* https://www.udemy.com/courses/search/?src=ukw&q={aranan}

aranan kelime (python) url
https://www.udemy.com/courses/search/?src=ukw&q=python

aranan kelime (java) url
https://www.udemy.com/courses/search/?src=ukw&q=java

aranan kelime (ingilizce) url
https://www.udemy.com/courses/search/?src=ukw&q=ingilizce

#? iki kelime arama
#* taslak url 
#* https://www.udemy.com/courses/search/?src=ukw&q={aranan+kelime}
aranan kelime (python django) url
https://www.udemy.com/courses/search/?src=ukw&q=python+django

aranan kelime (java programming) url
https://www.udemy.com/courses/search/?src=ukw&q=java+programming

#? ???? kelime arama
#* taslak url 
#* https://www.udemy.com/courses/search/?src=ukw&q={aranan+????+kelime}

aranan kelime (ingilizce yds kursu)
https://www.udemy.com/courses/search/?src=ukw&q=ingilizce+yds+kursu


#! EN FAZLA YORUM ALAN SIRALAMASI
https://www.udemy.com/courses/search/?q=python&sort=most-reviewed&src=ukw
#* https://www.udemy.com/courses/search/?q={aranan}&sort={most-reviewed}&src=ukw
https://www.udemy.com/courses/search/?q=python+django&sort=most-reviewed&src=ukw
#* https://www.udemy.com/courses/search/?q={aranan+kelime}&sort={most-reviewed}&src=ukw
#! EN ALAKALI SIRALAMASI
https://www.udemy.com/courses/search/?q=python&sort=relevance&src=ukw
#* https://www.udemy.com/courses/search/?q={aranan}&sort={relevance}&src=ukw
#! EN Y??KSEK PUAN ALAN SIRALAMASI
https://www.udemy.com/courses/search/?q=python&sort=highest-rated&src=ukw
#* https://www.udemy.com/courses/search/?q={aranan}&sort={highest-rated}&src=ukw
#! EN Y??KSEK PUAN ALAN SIRALAMASI
https://www.udemy.com/courses/search/?q=python&sort=newest&src=ukw
#* https://www.udemy.com/courses/search/?q={aranan}&sort={newest}&src=ukw


#! EN SON D??L DE SE????LM???? HAL?? SON URL
https://www.udemy.com/courses/search/?lang=tr&q=python+django&sort=most-reviewed&src=ukw
#* https://www.udemy.com/courses/search/?lang={tr}&p=2&q={aranan+kelime}&sort={sort_type}&src=ukw

'https://www.udemy.com/courses/free/?lang={lang}&p={page_number}&sort={sort_type}'

"""


"""
-FREE
    \--TR
        \---recommended
        \---popularity
        \---highest-rated
        \---newest
    \--EN
        \---recommended
        \---popularity
        \---highest-rated
        \---newest
-SEARCH
    \--TR
        \---relevance
        \---most-reviewed
        \---highest-rated
        \---newest
    \--EN
        \---recommended
        \---most-reviewed
        \---highest-rated
        \---newest
"""