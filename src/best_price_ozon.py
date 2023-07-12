from parse_link_ozon import GetLinksOzon
from parse_page_ozon import ParsePageOzon
from multiprocessing import Pool

animal = {'Влажный корм для кошек': 'собак',
             'Сухой корм для кошек': 'собак',
             'Влажный корм для собак': 'кошек',
             'Сухой корм для собак': 'кошек'}

class BestPriceOzon():
    result = list()
    data = list()
    def __init__(self, brand_name, type):
        self.type = type
        self.visited = dict()
        getLinksOzon = GetLinksOzon(brand_name, type)
        self.links = getLinksOzon.get_links(self.visited)
        del getLinksOzon
        print(len(self.links))
        if (self.links):
            data = self.parse_pages(self.links)


    def parse_pages(self, links):
        parsePage = ParsePageOzon(links, self.visited)
        self.data = parsePage.get_data()

    def best_price(self):
        for _ in range(5):
            min_price_link = str()
            min_price_100_gramm = 1000
            for link in self.data:
                if (self.data[link]['price_for_100_gramm'] < min_price_100_gramm and self.result.count(link) == 0 and (animal[self.type] in self.data[link]['name']) == False):
                    min_price_link = link
                    min_price_100_gramm = self.data[link]['price_for_100_gramm']
            if (len(min_price_link)):
                self.result.append(min_price_link)
        return self.get_result()

    def get_result(self):
        if (len(self.result) == 0):
            return "\nЛучшее предложение Ozon:\nНет результата по вашему запросу!\nВозможно опечатка!"
        result = "\nЛучшее предложение Ozon:\n"
        
        for index, url in enumerate(self.result):
            result += f"{index+1}) {self.data[url]['price_for_100_gramm']} руб/100гр. {self.data[url]['name']}, {self.data[url]['price']} за {self.data[url]['grams']} грамм\n"
            result += f"Ссылка: {url}\n"
        return result
            


