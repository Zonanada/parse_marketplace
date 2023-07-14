from best_price_ozon import BestPriceOzon
from best_price_widberries import BestPriceWildberries
from multiprocessing import Process
# Влажный корм для кошек
# Сухой корм для кошек
# Влажный корм для собак
# Сухой корм для собак


def process_wildberries():
    best_price = BestPriceWildberries('whiskas', 'Сухой корм для кошек')
    print(best_price.best_price())

def process_ozon():
    best_price = BestPriceOzon('whiskas', 'Сухой корм для кошек')
    print(best_price.best_price())

if __name__ == "__main__":
    process_first = Process(target=process_wildberries)
    process_second = Process(target=process_ozon)
    process_first.start()
    process_second.start()
    process_first.join()
    process_second.join()

