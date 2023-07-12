from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

feed_type = {'Влажный корм для кошек': 'vlazhnye-korma-dlya-koshek-12350',
             'Сухой корм для кошек': 'suhie-korma-dlya-koshek-12349',
             'Влажный корм для собак': 'vlazhnye-korma-dlya-sobak-12304',
             'Сухой корм для собак': 'suhie-korma-dlya-sobak-12303'}

class GetLinksOzon:
    def __init__(self, brand_name, type):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options)
        self.parse_link(f"https://www.ozon.ru/category/{feed_type[type]}/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={brand_name}")

    def parse_link(self, url):
        self.browser.get(url)
        sleep(3)
        self.all_product = self.browser.find_element(By.XPATH, "//div[@data-widget='megaPaginator']").find_elements(By.CLASS_NAME, 'tile-hover-target')

    def get_links(self, visited):
        links = list()
        for index, url in enumerate(self.all_product[:20]):
            if (index % 2): 
                link = url.get_attribute('href').split('/?')[0]
                # print('get link = ', link)
                links.append(link)
                visited[link] = True
        # self.browser.close()
        return links
    
    def __del__(self):
        self.browser.close()
 
# getlinks = GetLinksOzon('элато')
# visited = dict()
# print(getlinks.get_links(visited))

