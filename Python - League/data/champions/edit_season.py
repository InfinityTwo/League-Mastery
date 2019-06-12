configIndex = 0
with open("config.cfg", "r") as config:
    for i in config:
        if configIndex == 1:
            seasonValue = i
            break
        configIndex += 1

def writeToCurrentSeason(totalString, seasonFile):
    open(seasonFile, "w").close() #delete all contents of file
    with open(seasonFile, "w") as currentSeasonFileWrite: #open file
        currentSeasonFileWrite.write(totalString) #write whole text to file

def editSeason(name, associatedValue, valueChange, seasonFile): #main function to edit current season Values. Four parameters. 1: Champion Name, 2: Mastery Associated Number, 3: By how much is the value of the mastery supposed to change, 4: file path
    isNameEqual = False #variables used later
    frontFullString = ""
    backFullString = ""
    fullString = ""
    backString = ""
    with open(seasonFile, "r") as seasonFileVar: #open file
        for i in seasonFileVar: #iterate through file
            j = i #store the line as j
            iStripped = i.strip() #stripped version of the line, stored into iStripped
            iSplit = iStripped.split(", ") #split version of iStripped with ",.", stored into iSplit
            if iSplit[0] == name: #compared if the name of the champion on the line is the name of the champion passed on
                isNameEqual = True #if so, set variable to True
                frontString = ", ".join(iSplit[:associatedValue]) + ", "
                #frontString = iStripped[:int(len(name) - 1 + int(associatedValue) * 3)] #front part of the line before the edited value is stored into frontString
                if associatedValue != 16: #check if the value passed is the last in the line/the 16th number
                    backString = ", " + ", ".join(iSplit[associatedValue + 1:]) + "\n" #if not, store the remaining string into backString
                currentValue = iSplit[int(associatedValue)] #retrieve the stored value that is about to be changed
                fullString = frontString + str(int(int(currentValue) + int(valueChange))) + backString #the whole line that will be re-written
            elif isNameEqual == False: #if haven't found the line to change, store the line into frontFullString
                frontFullString += j
            elif isNameEqual == True: #if found the line to change, store the remaining lines into backFullString
                backFullString += j
    totalString = frontFullString + fullString + backFullString #the text to be re-written in the whole file
    writeToCurrentSeason(totalString, seasonFile) #invoking function, passing on totalString and seasonFile
    return 1 #return 1 as success if needed

def readSeasonLine(name, seasonFile):
    with open(seasonFile, "r") as seasonFileVar: #open file
        for i in seasonFileVar: #iterate through file
            iSplit = i.strip().split(", ") #stripped and split ",." version of the line, stored into iSplit
            if iSplit[0] == name: #compared if the name of the champion on the line is the name of the champion passed on
                iSplit[1] = " " + iSplit[1]
                iSplit[-2] = iSplit[-2] + " "
                return iSplit #returns the line as a list if successful
        return -1 #returns -1 as failure