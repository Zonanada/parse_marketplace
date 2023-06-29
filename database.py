import sqlite3
import os.path
import time


class Database:
    def __init__(self):
        have_database = self.is_have_database()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        if (have_database == False):
            self.cursor.execute("CREATE TABLE product_ozon (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, name TEXT, price INTEGER, grams INTEGER, price_100_gramm REAL, date INTEGER)")
            self.con.commit()

    def is_have_database(self):
        return os.path.exists('database.db')

    def add_product_ozon(self, link, name, price, grams, price_100_gramm):
        self.cursor.execute(f"insert into product_ozon (link, name, price, grams, price_100_gramm, date) VALUES ('{link}', '{name}', {price}, {grams}, {price_100_gramm}, {round(time.time())})")
        self.con.commit()

    def get_product_ozon(self, link):
        self.cursor.execute(f"SELECT * FROM product_ozon WHERE link = '{link}'")
        return self.cursor.fetchall()
    
# db = Database()
# db.add_product_ozon('aefvsfdgb', 'Сухой корм Elato Holistic для взрослых кошек с ягненком и олениной, 1,5кг', 1983, 1500, 132.2)
# print(db.get_product_ozon('aefvsfdgb'))