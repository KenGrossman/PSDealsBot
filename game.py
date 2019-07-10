class Game:
    def __init__(self, saleStrings):
        # saleStrings should come in the form of
        # [0]{'SAVE 60%'} - Sale percent ***SOMETIMES NOT PROVIDED***
        # [0/1]{'FIFA 19'} - Name of sale item
        # [1/2]{'Full Game'} - ***SOMETIMES NOT PROVIDED***
        # [2/3]{'PS4'} - Platform
        # [3/4]{'$59.99'} - Normal Price
        # [4/5]{'$23.99'} - Sale Price ***SOMETIMES NOT PROVIDED***

        i = 0
        len(saleStrings) > 4
        self.newPrice = "Unavailable"

        ###[--OPTIONAL--]###
        #Check for 'SAVE XX%' string and case where title of game could contain the word 'SAVE'
        if "SAVE" in saleStrings[i] and len(saleStrings) > 4:
            self.discountString = saleStrings[i].strip()
            i+=1
        else:
            self.discountString = "NULL"

        #Set title
        self.title = saleStrings[i]
        i+=1

        #Check if expected number of strings exist
        if len(saleStrings) > 4:
            self.contentType = saleStrings[i]
            i+=1
        else:
            self.contentType = "NULL"

        #Set platform
        if saleStrings[i].startswith("PS"):
            self.platform = saleStrings[i]
            i+=1
        else:
            self.platform = "NULL"

        #Set oldPrice
        #We could instead make "Unavailable" values into NULL values for easier datawork later?
        if saleStrings[i].startswith("$") or saleStrings[i] == "Unavailable":
            self.oldPrice = saleStrings[i]
            i+=1
        else:
            self.oldPrice = "NULL"
        
        #This index may not exist
        try:
            self.newPrice = saleStrings[i]
        except:
            self.newPrice = "NULL"

    def print_game_string(self):
        print(self.discountString + ", " + self.title + ", " + self.contentType + ", " +
         self.platform + ", " + self.newPrice + ", " + self.oldPrice)

    def print_test_game_string(self):
        print(self.contentType + ", " + self.title + ", " + self.discountString + ", " +
         self.platform + ", " + self.newPrice + ", " + self.oldPrice)