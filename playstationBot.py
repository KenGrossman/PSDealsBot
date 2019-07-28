import time
import game as g
import dbsetup
import dbaccessor
from pathlib import Path
from selenium import webdriver

def convertElementsToGames(elements):
	for element in elements:
	    saleStrings = element.get_property("outerText").split("\n")
	    print(saleStrings)
	    games.append(g.Game(saleStrings))

def clickableNavButton(button):
	buttonClasses = button.get_attribute( "class" ).split( ' ' )
	clickable = "paginator-control__arrow-navigation--disabled" not in buttonClasses
	print(clickable)
	return clickable

# Setup Driver and navigate to webpage
driver = webdriver.Chrome('/Users/kennygrossman/Projects/Bots/Drivers/chromedriver')
driver.get('https://store.playstation.com/en-us/grid/STORE-MSF77008-ALLDEALS/1?smcid=pdc%3Aen-us%3Aprimary%20nav%3Amsg-games%3Abuy-games')

#Create empty list for game objects
games = []
hasNextPage = True

while(hasNextPage):
	#Get page number
	pageNumber = driver.find_element_by_class_name("paginator-control__page-number--selected")
	print("---Saving page {0}---".format(pageNumber.get_property("innerText")))

	#Create list of web elements and covert into game objects
	gameElements = driver.find_elements_by_css_selector(".__desktop-presentation__grid-cell__base__0ba9f")
	convertElementsToGames(gameElements)

	#Determine if next page button is enabled
	nextButton = driver.find_element_by_class_name("paginator-control__next")
	hasNextPage = clickableNavButton(nextButton)

	if hasNextPage:
		nextButton.click()

#Close window
driver.quit()

#Check if database exists and if not create database
dbPath = Path('./game.db')
if not dbPath.is_file():
	print('Creating database...')
	dbsetup.dbsetup()

print('Updating database...')
db = dbaccessor.dbaccess(games)
lowestEver = db.findLowestPriceSales()

for row in lowestEver:
	print(row)

# print(lowestEver)