from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
from database import Database


class ParsePageOzon():
    data = dict()

    def __init__(self, links: list, visited: dict):
        self.visited = visited
        self.links = links
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options)
        self.db = Database()
        self.open_all_links()

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
                result.append(str[num])
            elif ((str[num] == ',' or str[num] == '.') and str[num-1].isdigit() and str[num+1].isdigit()):
                result.append('.')
        return float(''.join(result))

    def open_all_links(self):
        for link in self.links:
            self.parse_page(link)
            self.add_another_link(link)
            self.write_data(link)

    def parse_page(self, product_url):
        try:
            self.browser.delete_all_cookies()
            self.browser.get(product_url)
            print('parse page = ', product_url)
            sleep(2)
            self.name = self.browser.find_element(By.XPATH, "//div[@data-widget='webProductHeading']").text
            parameters = self.browser.find_element(By.XPATH, "//div[@data-widget='webCharacteristics']").text
            try:
                self.grams = self.str_to_float(
                    re.search(r'Вес товара, г\s\d+', parameters).group(0))
            except:
                self.grams = self.get_grams(self.name)    
        except:
            print('failed to load => ', product_url)

    def add_another_link(self, product_url):
        another_link = self.browser.find_elements(
            By.XPATH, "//a[@class='a2-a4 a2-a3']")
        for link in another_link:
            try:
                url = link.get_attribute('href').split('/?')[0]
                if ((url in self.visited) == False and (product_url in url) == False):
                    self.visited[url] = True
                    print('Append => ', url)
                    self.links.append(url)
            except:
                pass

    def write_data(self, product_url):
        self.db.add_product(
            product_url, self.name, self.price, self.grams, self.price_for_100_gramm)
        self.data[product_url] = {"name": self.name,
                                  "price": self.price,
                                  "grams": self.grams,
                                  "price_for_100_gramm": self.price_for_100_gramm}
    
    def get_data(self):
        return self.data
    
    def __del__(self):
        self.browser.close()
