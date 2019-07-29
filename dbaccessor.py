from sqlite3 import connect
from pathlib import Path
import time

class dbaccess():
    def prepPriceTable(self):
        #Update all endDates for sales to todays date if null
        self.conn.execute('UPDATE Price SET end_date = ? WHERE end_date IS NULL', (time.time(),))

    def updatePlatform(self, game):
        platformID = None

        #Grab platformID from Platform table
        self.conn.execute('SELECT id FROM Platform WHERE name = ?', (game.platform,))
        platformID = self.conn.fetchone()

        #If platformID does not exist in table add a new row then grab the new ID
        if platformID is None:
            self.conn.execute('INSERT INTO Platform (name) VALUES(?)', (game.platform,))
            self.gamedb.commit()
            self.conn.execute('SELECT id FROM Platform WHERE name = ?', (game.platform,))
            platformID = self.conn.fetchone()
    
        return platformID[0]

    def updateType(self, game):
        typeID = None
        
        #Grab typeID from Type table
        self.conn.execute('SELECT id FROM Type WHERE name = ?', (game.contentType,))
        typeID = self.conn.fetchone()

        #If typeID does not exist in table add a new row then grab the new ID
        if typeID is None:
            self.conn.execute('INSERT INTO Type (name) VALUES(?)', (game.contentType,))
            self.conn.execute('SELECT id FROM Type WHERE name = ?', (game.contentType,))
            typeID = self.conn.fetchone()
    
        return typeID[0]

    def updateGame(self, game, platformID, typeID):
        gameID = None

        #Grab gameID from Game table
        self.conn.execute('SELECT id FROM Game WHERE name = ? and type_id = ? and platform_ID = ?', (game.title, typeID, platformID,))
        gameID = self.conn.fetchone()

        #If gameID does not exist in table add a new row then grab the new ID
        #Newly added games will have a lowest ever price of today's price
        if gameID is None:
            self.conn.execute('INSERT INTO Game (name, lowest_price, platform_ID, type_ID) \
                VALUES(?, ?, ?, ?)', (game.title, game.newPrice, platformID, typeID,))
            self.conn.execute('SELECT id FROM Game WHERE name = ?', (game.title,))
            gameID = self.conn.fetchone()
        #If gameID already exists see if the newPrice is the lowestPrice ever and update table if so
        else:
            self.conn.execute('SELECT lowest_price FROM Game WHERE id = ?', (gameID[0],))
            lowest = self.conn.fetchone()[0]
            # print(lowest)

            if float(game.newPrice) < lowest:
                self.conn.execute('UPDATE Game SET lowest_price = ? WHERE id = ?', (game.newPrice, gameID,))

        return gameID[0]

    def updatePrice(self, game, gameID):
        # Add Prices to table as a new row
        self.conn.execute('INSERT INTO Price (game_ID, price, begin_date, end_date) \
            VALUES(?, ?, ?, NULL)', (gameID, game.newPrice, time.time(),))

    def findLowestPriceSales(self):
        #Grab all values collected today that have a price equal to the lowest recorded price
        self.conn.execute('SELECT * FROM Price INNER JOIN Game on Game.ID = Price.game_ID \
            WHERE Price.end_date IS NULL and Price.price = Game.lowest_price')
        data = self.conn.fetchall()
        return data

    def __init__(self, games):
        #Identify database path and connect to database
        self.dbpath = Path('./game.db')
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()

        #Set end date of all prices to today before grabbing new data
        self.prepPriceTable()

        #Set debug flag to print aditional details
        debug = False

        #Loop through all games updating each database table
        for game in games:
            platformID = self.updatePlatform(game)
            typeID = self.updateType(game)
            gameID = self.updateGame(game, platformID, typeID)
            self.updatePrice(game, gameID)

            if debug:
                print(game.title)
                print(platformID)
                print(typeID)
                print(gameID)