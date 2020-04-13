import sqlite3
import os
import json
import unittest

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_cuisines(data, cur, conn):
    cur.execute("DROP TABLE IF EXISTS Cuisines")
    cur.execute("CREATE TABLE Cuisines (food TEXT PRIMARY KEY, cuisine TEXT)")
    for cuisine in data.keys():
        for food in data[cuisine]:
            cur.execute("INSERT INTO Cuisines (food, cuisine) VALUES (?,?)", (food, cuisine))
    conn.commit()

def main():
    f = open("food_data.json")
    d = json.load(f)
    cur, conn = setUpDatabase('stabiao.db')
    create_cuisines(d, cur, conn)
    f.close()

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'stabiao.db')
        self.cur = self.conn.cursor()
        f = open("food_data.json")
        self.data = json.load(f)
        f.close()
    def test_table(self):
        for country in self.data.keys():
            self.cur.execute("SELECT food FROM Cuisines WHERE cuisine = \"{}\"".format(country))
            foods = self.cur.fetchall()
            for food in foods:
                self.assertTrue(food[0] in self.data[country])
        

    

if __name__ == "__main__":
    main()
    unittest.main(verbosity=3)