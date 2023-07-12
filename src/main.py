from best_price_ozon import BestPriceOzon
from best_price_widberries import BestPriceWildberries

best_price = BestPriceWildberries('elato', 'Сухой корм для кошек')
print(best_price.best_price())
best_price = BestPriceOzon('elato', 'Сухой корм для собак')
print(best_price.best_price())
