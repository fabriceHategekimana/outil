import sqlite3

class Data(): 
    nom="data/rules.db"

    def __init__(self):
        self.conn= sqlite3.connect(self.nom)
        self.c= self.conn.cursor()

    def sqlQuery(self, sql):
        tab= []
        res= self.c.execute(sql)
        for ligne in res:
            tab.append(list(ligne))
        return tab

    def sqlModify(self, sql):
        res= self.c.execute(sql)
        self.conn.commit()
