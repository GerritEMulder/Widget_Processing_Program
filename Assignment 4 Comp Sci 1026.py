__author__ = 'Gerrit Mulder'
# Name: Gerrit Mulder
# Course: Computer Science 1026
#
# In this program I calculate from a list of widgets
# If each widget can be built with the parts I have
# First the parts file is read in and processed
# Putting the name, price and quantity of each part into three list
# Then creates a master list (The database) of all the parts
# Then two dictionaries for the price and quantity of each part
# It then prints out the stock of each part before widget processing
# Next it opens the widgets file and starts processing it
# When it gets to a new widget it clears all variables for processing them
# Then reads all the parts needed for that one widget
# Next it checks if the widget can be built with the part in stock
# And if it can it reduces the related part stocks by what was used up
# Also calculating the cost of the widget and then prints out all the information
# If the widget can't be built it prints out that it can't be built and why it can't be built
# After all widgets have been processed it prints out the stock of each part after widget processing
# It ends by closing the parts and widgets files



# Parts class
class Parts:

    # The constructor for the class
    def __init__(self):
        self._partName = ""
        self._partPrice = ""
        self._partQuantity = ""

    # The getter and setter methods for this class
    def setName(self,name):
        self._partName = name
    def getName(self):
        return self._partName
    def setPrice(self,price):
        self._partPrice = price
    def getPrice(self):
        return self._partPrice
    def setQuantity(self,quantity):
        self._partQuantity = quantity
    def getQuantity(self):
        return self._partQuantity


# The main class of this program
# The PartInventory program
class PartInventory:

    # All the variables used between methods in this class
    partsInventory = []
    numberOfPartsPerPart = {}
    pricePerPart = {}
    partsNeeded = []

    # The constructor for the class
    def __init__(self):
        self._partQuantity = ""
        self._cost = ""

    # The main getter and setter methods for this class
    def inventory(self,part):
        PartInventory.partsInventory.append(part)
    def getInventory(self):
        return PartInventory.partsInventory
    def partQuantities(self,part,quantity):
        PartInventory.numberOfPartsPerPart[part] = quantity
    def getQuantity(self):
        return PartInventory.numberOfPartsPerPart
    def partPrices(self,part,price):
        PartInventory.pricePerPart[part] = price
    def getPrices(self):
        return PartInventory.pricePerPart

    # The method for removing parts from the database
    def removePart(self,part):
        PartInventory.partsInventory.remove(part)

    # This class calculates how much each batch of parts will cost and returns the results to the user
    def costOfWidget(self,part,numberOfParts):
        self._cost = float(numberOfParts) * float(PartInventory.pricePerPart[part])
        return self._cost

    # This method checks to make sure there are enough parts to make the widget
    # But if there isn't it returns a list stating either that there are
    # not enough of a part, or that a part isn't in the database of parts
    def processWidget(self,parts,numberOfParts,masterList):
        for i in range(0,len(parts)):
            if parts[i] not in masterList:
                part = parts[i]
                notInDatabaseString = "Part " + part + " is not in database of parts"
                PartInventory.partsNeeded.append(notInDatabaseString)
            elif float(PartInventory.numberOfPartsPerPart[parts[i]]) - float(numberOfParts[i]) < 0:
                notEnoughPartsString = "There are not enough of " + parts[i] + " to build widget"
                PartInventory.partsNeeded.append(notEnoughPartsString)
        return PartInventory.partsNeeded

    # This method calculates the amounts of parts left after using whatever is needed for building the widget
    # Then it returns the updated inventory
    def updateQuantity(self,part,amountNeeded):
        return float(PartInventory.numberOfPartsPerPart[part]) - float(amountNeeded)

    # This method clears the partsNeeded list
    def clearParts(self):
        PartInventory.partsNeeded = []


# The main method of the program
def main():

    # Opens up the parts file and then begins to read the first line
    partsFile = open("parts.txt", encoding = "ISO-8859-1")
    partsLine = partsFile.readline()
    partsList = partsLine.split()

    # Calling the Parts class and the PartInventory class
    parts = Parts()
    inventory = PartInventory()

    # While loop for looping through the parts file and inputting all the data
    while partsLine != "":

        # Sets and gets the part names, their price's and their quantities
        parts.setName(partsList[0])
        name = parts.getName()
        parts.setPrice(partsList[1])
        price = parts.getPrice()
        parts.setQuantity(partsList[2])
        quantity = parts.getQuantity()

        # Sets the parts into a master list and two dictionaries (one for price and one for quantity)
        # Then gets them
        inventory.inventory(name)
        masterList = inventory.getInventory()
        inventory.partPrices(name,price)
        priceList = inventory.getPrices()
        inventory.partQuantities(name,quantity)
        quantityList = inventory.getQuantity()

        # Reads the next line in the file
        partsLine = partsFile.readline()
        partsList = partsLine.split()

    # Prints a list of all the parts in the database and how many of each part there is in inventory
    print("_**__**__**__**__**_ List of parts before building widgets  _**__**__**__**__**_ \n")
    for key in sorted(quantityList):
        print("                                 %s: %s" % (key, quantityList[key]))
    print("\n")
    print("_**_" * 20)

    # Opens the widgets file and reads the first line
    widgetsFile = open("widgets.txt", encoding = "ISO-8859-1")
    widgetsLine = widgetsFile.readline()
    widgetLineList = widgetsLine.split()

    # Variables for the while loop
    widgetName = ""
    done = False

    # Print for showing that it has started to process the widgets
    print("\n\n _∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∫Widget Processing∫_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_ ")

    # Main while loop for processing each widget
    while done != True:

        # Checks to see the line it's processing is a new widget
        if widgetsLine[0] == "W":

            # When there is a new widget it gets the widget name
            # And resets all the variables used for processing widgets
            widgetName = (widgetLineList[0])
            partsNeededList = []
            amountNeededList =[]
            cost = 0
            canBuild = []
            inventory.clearParts()
            partsUsed = []

        # Checks to see if the line processing is a part
        elif widgetsLine[0] == "p":

            # String for outputting how much of each part was used
            partsUsedString = ("Used " + widgetLineList[1] + " of " + widgetLineList[0] + " in order to make " + widgetName)

            # Reads in the part name and how much will be used to create the widget
            partsUsed.append(partsUsedString)
            partsNeededList.append(widgetLineList[0])
            amountNeededList.append(widgetLineList[1])

        # Runs once it gets to the end of the widget
        else:

            # Runs the processWidget method to check if there are enough parts to build the widget
            canBuild = inventory.processWidget(partsNeededList,amountNeededList,masterList)

            # Checks if the check says it can build the widget
            if canBuild == []:

                # Cycles through all the parts
                for i in range(0,len(partsNeededList)):

                    # Gets the updated inventory of each part after they're used for building the widget
                    numberOfPartsLeft = inventory.updateQuantity(partsNeededList[i],amountNeededList[i])

                    # If any part has an inventory of zero it removes it from the database
                    if numberOfPartsLeft == 0:
                        inventory.removePart(partsNeededList[i])

                    # Updates the inventory of all parts used and gets the cost for each group of parts
                    inventory.partQuantities(partsNeededList[i],numberOfPartsLeft)
                    cost = cost + inventory.costOfWidget(partsNeededList[i],amountNeededList[i])

                # Prints out that that can be made, the cost of building the part,
                # And what parts were used in building it as well as how much of each part were used
                print("\n\nWidget: ",widgetName," can be built")
                print("The cost of building it is $",cost)
                for h in range(0,len(partsUsed)):
                    print(partsUsed[h])

            # If the widget can't be built it prints out that it can build it
            # It also prints out why the widget can't be built
            elif canBuild != []:
                print("\n\nWidget: ",widgetName," could not be built")
                for j in range(0,len(canBuild)):
                    print(canBuild[j])

        # Reads in the next line in the widget file
        widgetsLine = widgetsFile.readline()
        widgetLineList = widgetsLine.split()

        # Try and except clause for ending the loop
        # Once it reads through the whole widget file
        try:
            widgetsLine[0]
        except IndexError:
            done = True

    # Prints out that it's done processing the widgets
    print(" \n_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∫Widget Processing Done∫_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_∆_ \n")

    # Prints out the updated list of parts after all widgets that can be built are built
    print("\n_**__**__**__**__**_ List of parts after building widgets  _**__**__**__**__**_ \n")
    for key in sorted(quantityList):
        print("                                 %s: %s" % (key, quantityList[key]))
    print("\n")
    print("_**_" * 20)

    # Closes both files
    partsFile.close()
    widgetsFile.close()

# Runs the main method
main()
