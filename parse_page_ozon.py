from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
from selenium.webdriver.chrome.options import Options
from database import Database

class ParsePage():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    db = Database()

    def __init__(self, product_url):
        self.product_url = product_url
        self.parse_page()
        # self.browser.close()
    
    def get_grams(self, name):
        gram = float()
        multiplay = 1

        result = re.search(r'[\d.|,]*\d+\s*кг', name)
        if (result != None):
            gram = self.str_to_float(result.group(0)) * 1000


        result = re.search(r'\d+\s*г', name)
        if (result != None):
            gram = self.str_to_float(result.group(0))



        result = re.search(r'\d+гр', name)
        if (result != None):
            gram = self.str_to_float(result.group(0))


        result = re.search(r'\d+г', name)
        if (result != None):
            gram = self.str_to_float(result.group(0))



        result = re.search(r'\d?.\dкг', name)
        if (result != None):
            gram = self.str_to_float(result.group(0)) * 1000



        result = re.search(r'\d+\s*шт', name)
        if (result != None):
            multiplay = self.str_to_float(result.group(0))


        result = re.search(r'(х|x)\s\d+', name)
        if (result != None):
            multiplay = self.str_to_float(result.group(0))

        return gram * multiplay

    def str_to_float(self, str):
        result = list()
        for num in range(len(str)):
            if (str[num].isdigit()):
                result.append(str[num])            # print(url)
            elif ((str[num] == ',' or str[num] == '.') and str[num-1].isdigit() and str[num+1].isdigit()):
                result.append('.')
        return float(''.join(result))

    def parse_page(self):
        self.browser.delete_all_cookies()
        self.browser.get(self.product_url)
        sleep(1)
        self.name = self.browser.find_element(By.XPATH, "//div[@data-widget='webProductHeading']").text
        parameters = self.browser.find_element(By.XPATH, "//div[@data-widget='webCharacteristics']").text
        try:
            self.grams = self.str_to_float(re.search(r'Вес товара, г\s\d+', parameters).group(0))
        except:
            self.grams = self.get_grams(self.name)
        webSale = self.browser.find_element(By.XPATH, "//div[@data-widget='webSale']").text.split('\n')
        self.price = self.str_to_float(webSale[0])
        # print(self.price)
                            
        self.price_for_100_gramm = round(self.price / (self.grams / 100), 1)


    def add_another_link(self, links:list, visited:dict):
        another_link = self.browser.find_elements(By.XPATH, "//a[@class='a2-a4 a2-a3']")
        for link in another_link:
            url = link.get_attribute('href').split('/?')[0]
            if ((url in visited) == False and (self.product_url in url) == False):
                visited[url] = True
                links.append(url)


    
    def get_data(self, data:dict()):
        self.db.add_product_ozon(self.product_url, self.name, self.price, self.grams, self.price_for_100_gramm)
        data[self.product_url] = {"name": self.name,
            "price": self.price, 
            "grams": self.grams,
            "price_for_100_gramm": self.price_for_100_gramm}
        

# parsePage = ParsePage('https://www.ozon.ru/product/suhoy-korm-holistik-elato-dlya-vzroslyh-kastrirovannyh-kotov-sterilizovannyh-i-maloaktivnyh-koshek-791936889/?advert=mrHGwH1VIshkEy2BvMBJhxbBwX8JjYZKpH1wqU8U07tsbMy9eH8Lfyy44G21P8CsLUGxTsAoKe69Sg38wFGYZYGnI1a0szKcS2i51KBQP7qTpGRzO422fgfaDby0FrcK4f3O3bDxBvOa60CWgoVasMU3QjgzseGXT2cIHQvf3px_LCAfRNk_DFVBNHKrEx_ciYu11ijauuZnCcmuvnigqdi7iVcjPuJhkFMeCIKDBMewu8GwLJIQqwYUjQxBpA8PVy7GAPiML2o0a5RsO85fJ5sIre7UKS-e6mTSkVN7AQxUqpScIu2-G-GEugELZGxjxJs2vk00qGSQlot-BC5SGA&avtc=1&avte=2&avts=1687957139&keywords=elato&sh=dfDfoT-uPg')