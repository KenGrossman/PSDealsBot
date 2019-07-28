from sqlite3 import connect
from pathlib import Path

class dbsetup():
    def __init__(self):
        #Identify database path
        self.dbpath = Path('./game.db')

        #Connect to database and setup tables
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()
        self.setupdb()

    def deletedb(self):
    	self.dbpath.unlink()

    def setupdb(self):
    	print('Creating Platform Table')
    	platformTableSQL = '''CREATE TABLE IF NOT EXISTS Platform (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL)'''
    	self.conn.execute(platformTableSQL)


    	print('Creating Type Table')
    	typeTableSQL = '''CREATE TABLE IF NOT EXISTS Type (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL)'''
    	self.conn.execute(typeTableSQL)

    	print('Creating game Table')
    	gameTableSQL = '''CREATE TABLE IF NOT EXISTS Game (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    lowest_price real NOT NULL,
                                    platform_id integer NOT NULL,
                                    type_id integer NOT NULL,
                                    FOREIGN KEY (platform_id) REFERENCES Platform (id),
                                    FOREIGN KEY (type_id) REFERENCES Type (id))'''
    	self.conn.execute(gameTableSQL)

    	print('Creating price Table')
    	priceTableSQL = '''CREATE TABLE IF NOT EXISTS Price (
                                    id integer PRIMARY KEY,
                                    game_id integer NOT NULL,
                                    price real NOT NULL,
                                    begin_date integer NOT NULL, 
                                    end_date integer,
                                    FOREIGN KEY (game_id) REFERENCES Game (id))'''
    	self.conn.execute(priceTableSQL)

    	#Commit changes and close connection
    	# self.gamedb.commit()
    	# self.gamedb.close()
    	print('Tables created successfully')