from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
from selenium.webdriver.chrome.options import Options
from database import Database


class ParsePageWildberries():
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
            try:
                self.parse_page(link)
                self.add_another_link(link)
                self.write_data(link)
            except:
                print('Error =>', link)

    def parse_page(self, product_url):
        self.browser.delete_all_cookies()
        self.browser.get(product_url)
        print('parse page = ', product_url)
        sleep(2)
        self.browser.execute_script("window.scrollTo(0, 1200)")
        sleep(0.5)
        havePrice = True
        try:
            self.price = self.str_to_float(self.browser.find_element(
                By.XPATH, "//ins[@class='price-block__final-price']").text)
        except:
            havePrice = False
        if havePrice:
            try:
                self.browser.find_element(
                    By.XPATH, "//button[contains(text(),'Развернуть характеристики')]").click()
            except:
                print('No characteristics!')
            self.name = self.browser.find_element(
                By.XPATH, "//h1[@data-link='text{:selectedNomenclature^goodsName}']").text
            self.price = self.str_to_float(self.browser.find_element(
                By.XPATH, "//ins[@class='price-block__final-price']").text)
            parameters = self.browser.find_elements(
                By.CLASS_NAME, "product-params__row")

            str_parameters = ""
            for param in parameters:
                str_parameters += param.text

            grams = re.search(
                r'Вес товара без упаковки \(г\) \d+', str_parameters)
            if (grams != None):
                self.grams = self.str_to_float(grams.group(0))
            else:
                try:
                    unit_weight = self.str_to_float(
                        re.search(r'Вес одного предмета \(г\) \d+', str_parameters).group(0))
                    count = self.str_to_float(
                        re.search(r'Количество предметов в упаковке \d+', str_parameters).group(0))
                    self.grams = unit_weight * count
                except:
                    self.grams = self.get_grams(self.name)

            self.price_for_100_gramm = round(
                self.price / (self.grams / 100), 1)

        else:
            print('No price!')

    def add_another_link(self, product_url):
        another_link = self.browser.find_elements(
            By.XPATH, "//a[@class='img-plug']")
        for link in another_link:
            try:
                url = link.get_attribute('href')
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
