from pathlib import Path
import random

def makeChange(denominations, change, changeString):
	for denomination, value in denominations.items():
		# print('Change {0} and denomination {1}'.format(change, denomination))
		amount = change // denomination
		change -= amount * denomination
		if amount > 0:
			if changeString != '':
				changeString += ','
			changeString += '{0} {1}'.format(amount, value)
	return changeString

def shuffleDenominationOrder(denominations):
	items = list(denominations.keys())
	random.shuffle(items)
	shuffledDenominations = {}
	for item in items:
		shuffledDenominations[item] = denominations[item]
	return shuffledDenominations


#Open inputFile and convert lines of text to a list
inputFile = Path('./inputfile.txt')
fileText = inputFile.read_text()
lines = fileText.split('\n')

#Locate and erase outputfile if it exists
outputFile = Path('./outputfile.txt')
if outputFile.exists():
	outputFile.unlink()

#Perform logic on each line from file
for line in lines:
	#Grab values remove decimals and convert to integer
	values = line.split(',')
	cost = int(values[0].replace('.', ''))
	paid = int(values[1].replace('.', ''))
	change = paid - cost

	changeString = ''
	denominations = {100: 'dollars', 25: 'quarters', 10: 'dimes', 5: 'nickels', 1: 'pennies'}

	#Randomly choose change denominations if evenly divisible by 3 
	if (change % 3 == 0): 
		denominations = shuffleDenominationOrder(denominations)

	changeString = makeChange(denominations, change, changeString)

	#Write values to file
	with open(outputFile, mode='a') as output:
		output.write(changeString + '\n')

	# outputFile.write_text(changeString)
	print(changeString)