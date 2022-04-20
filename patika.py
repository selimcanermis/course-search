PATH = (r'C:\Program Files\chromedriver.exe')
delay = 15

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
        self.home_url = "https://www.udemy.com/"
