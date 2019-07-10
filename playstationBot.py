import time
import game as g
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Setup URL
driver = webdriver.Chrome('/Users/kennygrossman/Projects/Bots/Drivers/chromedriver')

# Open webpage
driver.get('https://store.playstation.com/en-us/grid/STORE-MSF77008-ALLDEALS/1?platform=ps4');
time.sleep(2)

#Create empty list for game objects
games = []
hasNextPage = True

while(hasNextPage):
	#Get page number
	pageNumber = driver.find_elements_by_css_selector("paginator-control__page-number--selected")
	#print("---Saving page {0}---".format(pageNumber.get_property("innerText")))
	print("---Saving page---")

	#Create list of gameElements on page
	gameElements = driver.find_elements_by_css_selector(".__desktop-presentation__grid-cell__base__0ba9f")

	#Create game object list
	for game in gameElements:
	    saleStrings = game.get_property("outerText").split("\n")
	    print(saleStrings)
	    games.append(g.Game(saleStrings))

	#Determine if next page button is enabled
	nextButton = driver.find_element_by_class_name("paginator-control__next")
	buttonClasses = nextButton.get_attribute( "class" ).split( ' ' )
	hasNextPage = "paginator-control__arrow-navigation--disabled" not in buttonClasses
	print(hasNextPage)

	if hasNextPage:
		nextButton.click()
		time.sleep(2)

#Cycle through game object to verify print output
for game in games:
    game.print_game_string()

#Close window
driver.quit()