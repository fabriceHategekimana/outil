import sqlite3
from sqlite3 import Error

CREATE_TABLE_LINKS="""CREATE TABLE links(subject text not null, link text not null, goal text not null);"""
CREATE_TABLE_EXP_RULES="""CREATE TABLE exp_rules(id integer primary key autoincrement, header text, premises text, conclusion text);"""
CREATE_TABLE_STATE_RULES="""CREATE TABLE state_rules(id integer primary key autoincrement, header text, premises text, conclusion text);"""
CREATE_TABLE_SQLITE_SEQUENCE="""CREATE TABLE sqlite_sequence(name,seq);"""

class Data(): 
    nom="rules.db"

    def __init__(self):
        #Create database if not exist
        self.createDbIfNotExist()
        #Connect database and create a pointer
        self.conn= sqlite3.connect(self.nom)
        self.c= self.conn.cursor()
        #Create table if not exist
        self.createTablesIfNotExist()

    def createDbIfNotExist(self):
        conn= None
        try:
            conn= sqlite3.connect(self.nom)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def createTablesIfNotExist(self):
        try:
           self.c.execute(CREATE_TABLE_LINKS) 
           self.c.execute(CREATE_TABLE_EXP_RULES) 
           self.c.execute(CREATE_TABLE_STATE_RULES) 
           self.c.execute(CREATE_TABLE_SQLITE_SEQUENCE) 
        except Error as e:
            print(e)

    def sqlQuery(self, sql):
        tab= []
        res= self.c.execute(sql)
        for ligne in res:
            tab.append(list(ligne))
        return tab

    def sqlModify(self, sql):
        res= self.c.execute(sql)
        self.conn.commit()
