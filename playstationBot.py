import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Game:
    def __init__(self, gameString):
        # gameString should come in the form of
        # [0]{'SAVE 60%'} - Sale percent
        # [1]{'FIFA 19'} - Name of sale item
        # [2]{'Full Game'} - ***SOMETIMES NOT PROVIDED***
        # [3/2]{'PS4'} - Device Type
        # [4/3]{'$59.99'} - Normal Price
        # [5/4]{'$23.99'} - Sale Price

        self.discountString = gameString[0]
        self.title = gameString[1]

        #Determine if optional content type string is provided
        x = 1
        if len(gameString) == 6:
            self.contentType = gameString[2]
            x = 0

        self.deviceType = gameString[3 - x]
        self.newPrice = gameString[4 - x]
        self.oldPrice = gameString[5 - x]

    # def printString(self, message):
    #     print(self.title + " is ")

# Setup URL
driver = webdriver.Chrome('/Users/kennygrossman/Projects/YoutubeBot/chromedriver')

# Open webpage
driver.get('https://store.playstation.com/en-us/grid/STORE-MSF77008-ALLDEALS/1?platform=ps4');
time.sleep(2)

print("---Saving this pages games---")
gameElements = driver.find_elements_by_css_selector(".__desktop-presentation__grid-cell__base__0ba9f")

for game in gameElements:
    print(game.get_property("outerText").split("\n"))
    gameStrings = game.get_property("outerText").split("\n")
    game = Game(gameStrings)