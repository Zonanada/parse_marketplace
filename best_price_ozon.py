from parse_link_ozon import GetLinksOzon
from parse_page_ozon import ParsePage
from database import Database

class BestPriceOzon:
    pass

db = Database()
visited = dict()
getLinksOzon = GetLinksOzon('элато')
links = getLinksOzon.get_links(visited)
print(len(links))
data = dict()


for link in links:
    query = db.get_product_ozon(link)
    if (len(query) == 0):
        parsePage = ParsePage(link)
        parsePage.add_another_link(links, visited)
        parsePage.get_data(data)
    else:
        query = query[0]
        data[query[1]] = {"name": query[2],
            "price": query[3], 
            "grams": query[4],
            "price_for_100_gramm": query[5]}
print(len(links))
# print(data)
# print(len(data))

result = list()
for _ in range(5):
    min_price_link = str()
    min_price_100_gramm = 1000
    for link in data:
        if (data[link]['price_for_100_gramm'] < min_price_100_gramm and result.count(link) == 0 and ('собак' in data[link]['name']) == False):
            min_price_link = link
            min_price_100_gramm = data[link]['price_for_100_gramm']
    result.append(min_price_link)
for line in result:
    print(line)
    print(data[line])
    print('\n')



# print(data)