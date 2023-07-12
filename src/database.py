import sqlite3
import os.path
import time

class Database:
    def __init__(self):
        have_database = self.is_have_database()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        if (have_database == False):
            self.cursor.execute("CREATE TABLE state_user (user_id INTEGER, state TEXT, category TEXT)")
            self.con.commit()
            self.cursor.execute("CREATE TABLE product (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, name TEXT, price INTEGER, grams INTEGER, price_100_gramm REAL, date INTEGER)")
            self.con.commit()

    def is_have_database(self):
        return os.path.exists('database.db')

    def set_state_user(self, user_id, state, category='none'):
        if (len(self.get_state_user(user_id))):
            self.cursor.execute(f"UPDATE state_user SET state = '{state}', category = '{category}' where user_id = {user_id}")
            self.con.commit()
        else:
            self.cursor.execute(f"insert into state_user (user_id, state, category) VALUES ({user_id}, '{state}', '{category}')")
            self.con.commit()

    def get_state_user(self, user_id):
        self.cursor.execute(f"SELECT state, category FROM state_user WHERE user_id = {user_id}")
        return self.cursor.fetchall()
    
    def add_product(self, link, name, price, grams, price_100_gramm):
        self.cursor.execute(f"insert into product (link, name, price, grams, price_100_gramm, date) VALUES ('{link}', '{name}', {price}, {grams}, {price_100_gramm}, {round(time.time())})")
        self.con.commit()

    def get_product(self, link):
        self.cursor.execute(f"SELECT * FROM product WHERE link = '{link}'")
        return self.cursor.fetchall()
    
    def __del__(self):
        self.con.close()