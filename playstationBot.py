import time
import game as g
import dbsetup
import dbaccessor
from pathlib import Path
from selenium import webdriver


def convertElementsToGames(elements, games):
	for element in elements:
		saleStrings = element.get_property("outerText").split("\n")
		print(saleStrings)

	game = g.Game(saleStrings)

	#Append game only if on sale
	if game.onSale:
		games.append(game)


def connectToDatabase(games):
	#Check if database exists and if not create database
	dbPath = Path('./game.db')
	if not dbPath.is_file():
		print('Creating database...')
		dbsetup.dbsetup()

	#Update database using games list
	print('Updating database...')
	db = dbaccessor.dbaccess(games)

	#Find and display all games that are currently the lowest price acording to database
	#~~~NOTE: On first run all games will be at the lowest recorded price~~~
	lowestEver = db.findLowestPriceSales()
	for row in lowestEver:
		print(row)


def clickableNavButton(button):
	buttonClasses = button.get_attribute( "class" ).split( ' ' )
	clickable = "paginator-control__arrow-navigation--disabled" not in buttonClasses
	print(clickable)
	return clickable


def mainLoop():
	#Path to brower driver... make sure to place a driver into the folder
	#Drivers can be found at https://www.seleniumhq.org/download/
	driverPath = Path('./Drivers/chromedriver')

	# Setup Driver and navigate to webpage
	driver = webdriver.Chrome(driverPath)
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
		convertElementsToGames(gameElements, games)

		#Determine if next page button is enabled
		nextButton = driver.find_element_by_class_name("paginator-control__next")
		hasNextPage = clickableNavButton(nextButton)

		if hasNextPage:
			nextButton.click()

	#Close window
	driver.quit()

	#Update database
	connectToDatabase(games)


if __name__== "__main__":
	mainLoop()