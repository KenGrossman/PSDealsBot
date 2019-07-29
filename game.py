import re

class Game:
    def __init__(self, saleStrings):
        '''
        saleStrings usually come in the form of:
        [0]{'SAVE 60%'} - Sale percent ***SOMETIMES NOT PROVIDED***
        [1]{'FIFA 19'} - Name of sale item
        [2]{'Full Game'} - ***SOMETIMES NOT PROVIDED***
        [3]{'PS4'} - Platform
        [4]{'$59.99'} - Normal Price
        [5]{'$23.99'} - Sale Price ***SOMETIMES NOT PROVIDED***
        '''

        self.onSale = True

        try:
            #Check top of list for 'SAVE XX%' using Regex...throw exception if match is not found
            if re.match('^SAVE ([1-9][0-9]|[0-9])%', saleStrings[0]):
                self.discountString = saleStrings.pop(0).strip()
            else:
                self.onSale = False
                assert(self.onSale)

            #Set title from top of list
            self.title = saleStrings.pop(0)

            #Grab salePrice from end of list
            lastElement = saleStrings.pop()
            if lastElement.startswith('$'):
                self.newPrice = lastElement.replace('$', '')

            #Grab oldPrice from end of list
            lastElement = saleStrings.pop()
            if lastElement.startswith('$'):
                self.oldPrice = lastElement.replace('$', '')

            #Grab platform from end of list
            lastElement = saleStrings.pop()
            self.platform = lastElement

            #If there is a remaining element it will be the type
            if saleStrings:
                self.contentType = saleStrings.pop()
            else:
                self.contentType = 'NULL'
        except Exception as e:
            print(e)
            print('Item is not on sale and will be skipped')

    def print_game_string(self):
        print(self.discountString + ", " + self.title + ", " + self.contentType + ", " +
         self.platform + ", " + self.newPrice + ", " + self.oldPrice)