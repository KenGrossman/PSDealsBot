from sqlite3 import connect
from pathlib import Path
import time

class dbaccess():
    def updatePlatform(self, game):
        #See if platform exist as a row in table
        platformID = None

        self.conn.execute('SELECT id FROM Platform WHERE name = ?', (game.platform,))
        platformID = self.conn.fetchone()
        if platformID is None:
            self.conn.execute('INSERT INTO Platform (name) VALUES(?)', (game.platform,))
            self.gamedb.commit()
            self.conn.execute('SELECT id FROM Platform WHERE name = ?', (game.platform,))
            platformID = self.conn.fetchone()
    
        return platformID[0]

    def updateType(self, game):
        typeID = None
        
        self.conn.execute('SELECT id FROM Type WHERE name = ?', (game.type,))
        typeID = self.conn.fetchone()
        if typeID is None:
            self.conn.execute('INSERT INTO Type (name) VALUES(?)', (game.type,))
            self.conn.execute('SELECT id FROM Type WHERE name = ?', (game.type,))
            typeID = self.conn.fetchone()
    
        return typeID[0]

    def updateGame(self, game, platformID, typeID):
        gameID = None

        self.conn.execute('SELECT id FROM Game WHERE name = ? and type_id = ? and platform_ID = ?', (game.title, typeID, platformID,))
        gameID = self.conn.fetchone()

        print('game.newPrice: {0}'.format(game.newPrice))
        print('platformID: {0}'.format(platformID))
        print('gameID: {0}'.format(gameID))

        if gameID is None:
            self.conn.execute('INSERT INTO Game (name, lowest_price, platform_ID, type_ID) \
                VALUES(?, ?, ?, ?)', (game.title, game.newPrice, platformID, typeID,))
            self.conn.execute('SELECT id FROM Game WHERE name = ?', (game.title,))
            gameID = self.conn.fetchone()
        else:
            self.conn.execute('SELECT lowest_price FROM Game WHERE id = ?', (gameID[0],))
            lowest = self.conn.fetchone()[0]
            print(lowest)

            if float(game.newPrice) < lowest:
                self.conn.execute('UPDATE Game SET lowest_price = ? WHERE id = ?', (game.newPrice, gameID,))

        return gameID[0]

        # try:
        #     self.conn.execute('SELECT id FROM Game WHERE name = {0}'.format(game.title))
        #     gameID = self.conn.fetchone()
        # except:
        #     print('game exception')
        #     self.conn.execute('INSERT INTO Game (name, lowest_price, platform_ID, type_ID) \
        #         VALUES({0}, {1}, {2}, {3})'.format(game.title, game.newPrice, platformID, typeID))
        #     self.conn.execute('SELECT id FROM Game WHERE name = {0}'.format(game.title))
        #     gameID = self.conn.fetchone()
        # else:
        #     self.conn.execute('SELECT lowest_price FROM Game WHERE id = {0}'.format(gameID))
        #     lowest = self.conn.fetchone()
        #     if game.newPrice < lowest:
        #         self.conn.execute('UPDATE Game SET lowest_price = {0} WHERE id = {1}'.format(game.newPrice, gameID))
        # finally:
        #     return gameID

    def updatePrice(self, game, gameID):
        # Add Prices to table
        self.conn.execute('INSERT INTO Price (game_ID, price, begin_date, end_date) \
            VALUES(?, ?, ?, NULL)', (gameID, game.newPrice, time.time(),))

    def findLowestPriceSales(self):
        self.conn.execute('SELECT * FROM Price INNER JOIN Game on Game.ID = Price.game_ID \
            WHERE Price.end_date IS NULL and Price.price = Game.lowest_price')

        data = self.conn.fetchall()
        return data

    def prepPriceTable(self):
        #Update all endDates for sales to todays date if null
        self.conn.execute('UPDATE Price SET end_date = ? WHERE end_date IS NULL', (time.time(),))

    def __init__(self, games):
        #Identify database path
        self.dbpath = Path('./game.db')

        #Connect to database and setup tables
        self.gamedb = connect(self.dbpath, isolation_level=None)
        self.conn = self.gamedb.cursor()

        #Set end date of all prices to today before grabbing new data
        self.prepPriceTable()

        for game in games:
            print(game.title)
            platformID = self.updatePlatform(game)
            print(platformID)
            typeID = self.updateType(game)
            print(typeID)
            gameID = self.updateGame(game, platformID, typeID)
            print(gameID)
            self.updatePrice(game, gameID)