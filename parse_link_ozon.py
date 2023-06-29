from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class GetLinksOzon:
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    def __init__(self, product_name):
        self.parse_link(f"https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={product_name}")

    def parse_link(self, url):
        self.browser.get(url)
        sleep(1)
        self.all_product = self.browser.find_element(By.XPATH, "//div[@data-widget='megaPaginator']").find_elements(By.CLASS_NAME, 'tile-hover-target')

    def get_links(self, visited):
        links = list()
        for index, url in enumerate(self.all_product[:-2]):
            if (index % 2):
                link = url.get_attribute('href').split('/?')[0]
                links.append(link)
                visited[link] = True
        self.browser.close()
        return links
 
# getlinks = GetLinksOzon('элато')
# visited = dict()
# getlinks.get_links(visited)




