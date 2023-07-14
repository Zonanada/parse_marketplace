from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


feed_type = {'Влажный корм для кошек': 'влажный%20корм%20для%20кошек%20',
             'Сухой корм для кошек': 'сухой%20корм%20для%20кошек%20',
             'Влажный корм для собак': 'влажный%20корм%20для%20собак%20',
             'Сухой корм для собак': 'сухой%20корм%20для%20собак%20'}

class GetLinksWilberries():
    all_product = list()

    def __init__(self, brand_name, type):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options)
        self.parse_link(f"https://www.wildberries.ru/catalog/0/search.aspx?search={feed_type[type]}{brand_name}")

    def parse_link(self, url):
        self.browser.get(url)
        sleep(5)
        try:
            self.browser.find_element(By.XPATH, "//h1[@class='not-found-search__title']")
        except:
            self.browser.execute_script("window.scrollTo(0, 1200)")
            self.all_product = self.browser.find_element(By.XPATH, "//div[@class='product-card-list']").find_elements(By.CSS_SELECTOR, "a")

    def get_links(self, visited):
        links = list()
        for id, product in enumerate(self.all_product[:20]):
            if (id % 2 == 0):
                url = product.get_attribute('href')
                links.append(url)
                visited[url] = True
        return links

    def __del__(self):
        self.browser.close()
