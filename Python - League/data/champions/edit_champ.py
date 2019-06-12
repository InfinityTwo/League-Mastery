###Start of shared code
import os #imports libraray "os"
wd = os.getcwd() #sets current work directory to variable
champDatabaseFile = wd + "\\data\\champions\\champions_database.txt" #sets champions_database location to variable
newInstanceMastery = wd + "\\data\\new_instance\\Mastery.txt"

def addNamesToList(championList): #Function to read from champions_database.txt and add name to list
    with open(champDatabaseFile, "r") as champions_database: #Adding elements to List
        for i in champions_database:
            championList.append(i.strip())
    return championList

def writeToTXTFile(championList): #Function to write to champions_database.txt and re-write the file
    open(champDatabaseFile, "w").close() #delete file content
    with open(champDatabaseFile, "w") as champions_database: #re-writing to database
        for i in range(len(championList)):
            if i != (len(championList) - 1): #compare if index is the last in length of champion list
                champions_database.write(championList[i] + "\n")
            else:
                champions_database.write(championList[i]) #if it is, don't write it with \n

def addNamesToList2(championList): #Function to read from Mastery.txt in new_instance and add name to list
    with open(newInstanceMastery, "r") as champions_database: #Adding elements to List
        for i in champions_database:
            i = i.strip()
            i = i.split(", ")
            championList.append(i[0])
    return championList

def writeToTXTFile2(championList): #Function to write to Mastery.txt in new_instance and re-write the file
    open(champDatabaseFile, "w").close() #delete file content
    with open(newInstanceMastery, "w") as champions_database: #re-writing to database
        for i in range(len(championList)):
            if i != (len(championList) - 1): #compare if index is the last in length of champion list
                champions_database.write(championList[i] + ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n")
            else:
                champions_database.write(championList[i] + ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0") #if it is, don't write it with \n
###End of shared code



###Start of Add champion name code
def checkPosition(champName, championList): #Function to check Position to add Name
    [i.lower() for i in championList] #makes the list all lowercase
    champName.lower() #makes the name lowercase
    for i in range(len(championList)):
        if str(championList[i]) > str(champName):
            return i
        if str(championList[i]) == "":
            return i

def checkDuplicate(champName, championList):#Function to check if name already exists
    for i in championList:
        if str(i) == str(champName):
            return True
    return False

def moveNamesAdd(championList, position): #Function to move all elements to the right by one space after where the new element should be added
	for i in range(len(championList)-position):
		championList[len(championList) - (i + 1)] = championList[len(championList) - (i + 2)]

def addChampSubMain(champName, championList): #function to invoke it twice
    if not checkDuplicate(champName, championList): #Check if name already exists
        position = checkPosition(champName, championList) #find position
        if championList[position] != "": #check if it's last position. If not, move everything to the right
            championList.append(championList[len(championList) - 1])
            moveNamesAdd(championList, position)
        championList[position] = champName #adding name to list
        return "1" #return success
    return "0" #return failure - duplicate found


def addChamp(champName): #Main code to add champion name
    #championList = [] #List
    #championList = addNamesToList(championList)
    #if addChampSubMain(champName, championList):
    #    writeToTXTFile(championList)
    championList = [] #List
    championList = addNamesToList2(championList)
    if addChampSubMain(champName, championList):
        writeToTXTFile2(championList)

###End of Add champion name code



###Start of Remove champion name code
def checkNamePos(champName, championList): #Function to heck which position of the list the name is at
    for i in range(len(championList)):
        if str(championList[i]) == champName:
            return i
    return -1

def moveNamesDelete(championList, condition): #Function to move the elements after the deleted name one to the left
    for i in range(len(championList) - condition):
        if i == (len(championList) - condition - 1):
            championList[i+condition] = ""
            break
        if championList[i+condition] == "":
            break
        else:
            championList[i + condition] = championList[i + condition + 1]

def removeNameSubMain(champName, championList): #Split from main code to call this twice
    position = checkNamePos(champName, championList) #check name position
    if position != -1:
        moveNamesDelete(championList, position)


def removeName(champName): #main code
    championList = [] #List
    championList = addNamesToList(championList) #add name to list
    removeNameSubMain(champName, championList)
    del championList[-1]
    writeToTXTFile(championList)
    championList = [] #List
    championList = addNamesToList2(championList) #add name to list
    removeNameSubMain(champName, championList)
    del championList[-1]
    writeToTXTFile2(championList)
    return 1
###End of Remove champion name code



###Used for immediate testing. Uncomment to test. Recomment after testing
#addChamp(input())
#removeName(input())
###End of immediate testing