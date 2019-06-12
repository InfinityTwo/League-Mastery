#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#config initialization----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with open("config.cfg", "r") as configFile:
    configIndex = 0
    configList = []
    for line in configFile:
        if (configIndex + 2) % 3 == 0:
            configList.append(line.strip())
        configIndex += 1

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#imports------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from tkinter import *
from data.champions.edit_champ import *
from data.champions.edit_season import *
from data.app.colours.colours import *
import subprocess
import sys
import os
import functools
import time
import pip

#attempt to install pyautogui
installingPyautogui = 0
while True:
    try:
        import pyautogui
    except ImportError:
        if installingPyautogui == 0:
            os.startfile(os.getcwd() + "\\data\\app\\install\\pyautogui.bat")
            installingPyautogui = 1
    else:
        break

import pyautogui

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#check current season-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
defaultSeasonReadIndex = 0 #index for read file
defaultSeasonNumber = 9 #to be updated as app is updated
with open("config.cfg", "r") as config: #read line 2 of config file to check for an updated number
    for i in config:
        if defaultSeasonReadIndex == 1:
            defaultSeasonNumber = i.strip()
            break
        defaultSeasonReadIndex += 1

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#file paths---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
currentSeasonFilePath = wd + "\\localdata\\Season " + defaultSeasonNumber + "\\Mastery.txt"
masteryGradesPath = wd + "\\data\\champions\\mastery\\grades\\grades_database.txt"
champImagePath = wd + "\\data\\champions\\images 40x40\\"
champImagePath120x120 = wd + "\\data\\champions\\images 120x120\\"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#root---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
#root.attributes("-alpha", 0.99) #99% opacity
root.resizable(0, 0) #unresizable window

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#imports part 2 (only can be done after root)---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from data.app.images.imagepaths import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#screen size stuff, dynamic calculations----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#the following two lines are unrequired but kept for in case the app becomes resizable
screenX = str(int(int(root.winfo_screenwidth()) * 5/6))
screenY = str(int(int(root.winfo_screenheight()) * 5/6))
#edit the following two lines if window needs to be smaller
screenX = str(1280)
screenY = str(720)
intScreenX = int(screenX)
intScreenY = int(screenY)
geometryDisplay = screenX + "x" + screenY #setting variable for the size of the window
root.geometry(geometryDisplay) #setting size of window

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#main Frame---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
mainFrame = Frame(root, bg = colour87Black, width = intScreenX, height = intScreenY)
mainFrame.pack(fill = BOTH)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#header image selector functions------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def headerMasteryImageSelector():
    if selectedTab == "Mastery":
        return headerMasterySelectedImage
    return headerMasteryImage

def headerRankedImageSelector():
    if selectedTab == "Ranked":
        return headerRankedSelectedImage
    return headerRankedImage

def headerAddNewImageSelector():
    if selectedTab == "Add New":
        return headerAddNewSelectedImage
    return headerAddNewImage

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#hide all function--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def hideALL():
    mainMasteryFrame.pack_forget()
    addFrame.pack_forget()
    selectChampionFrame.pack_forget()
    selectMasteryLetterFrame.pack_forget()
    selectMasteryProgressBar.place_forget()
    selectMasteryFinishFrame.pack_forget()
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#mastery tab--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#frames for mastery
#main Mastery Frame
mainMasteryFrame = Frame(mainFrame, bg = colour87Black, width = intScreenX, height = intScreenY)
mainMasteryFrame.pack(fill = BOTH)

#top Frame
TopFrame = Frame(mainMasteryFrame, bg = colour87Black, width = intScreenX + 4, height = intScreenY * 1/14 + 2, bd = 0, highlightbackground = colourActuallyWhite, relief = GROOVE)
TopFrame.place(x = -2, y = -2)

#2nd top Frame
secondFromTopFrame = Frame(mainMasteryFrame, bg = colour91Black, width = intScreenX + 4, height = intScreenY * 1/14 + 2, bd = 0, highlightbackground = colourActuallyWhite, relief = GROOVE)
secondFromTopFrame.place(x = -2, rely = 10/112)

#footer Frame
footerFrame = Frame(mainMasteryFrame, bg = colour91Black, width = intScreenX + 4, height = intScreenY * 11/228 + 2, bd = 0, highlightbackground = colourActuallyWhite, relief = GROOVE)
footerFrame.place(x = -2, rely = 102/112)

#mastery body
def scrollingMain(event): #event to scroll scrollbar? Not sure
    masteryCanvas.configure(scrollregion = masteryCanvas.bbox("all"))

def masteryScrollWheel(event): #event for scroll wheel to scroll scrollbar
    masteryCanvas.yview("scroll", int(event.delta/-90), "units")

masteryCanvas = Canvas(mainMasteryFrame, bg = colour87Black, width = intScreenX, height = 131/192 * intScreenY, relief = FLAT, bd = -2) #mastery canvas, under mainMasteryFrame
masteryCanvas.place(x = -2, rely = 20/100)
masteryFrame = Frame(masteryCanvas, bg = colour87Black, width = intScreenX, height = intScreenY) #mastery frame, under masteryCanvas
masteryScrollbar = Scrollbar(masteryCanvas) #mastery scrollbar
masteryScrollbar.config(bg = colour87Black, troughcolor = colour87Black, activebackground = colour87Black, activerelief = FLAT)
#masteryScrollbar.place(x = intScreenX - 16, y = 0, height = 131/192 * intScreenY) #uncomment for ugly scrollbar on the right

#display champions, image behind champion, mastery counts and champion image by reading text file - needed for next line after continuation
#dictionaries & variables for this section
champDict = {}
champDictBackgroundIMG = {}
champDictColour = {}
champEachMasteryDict = {}
champImageDict = {}
j = {}
totalGamesPlayedDict = {}
averageMasteryDict = {}
championImageDict = {}
totalGamesPerMastery = [0] * 15
masteryChampionLineStr = ""
championCount = -1 #index
masteryRowHeightInpx = 88 #changable variable for height
totalGamesPlayed = 0
averageMastery = 0
grandTotalGamesPlayed = 0
totalAverageMastery = 0

#main code for mastery begins
currentSeasonFile = open(currentSeasonFilePath, "r") #open file
for i in currentSeasonFile: #loop to save each champion to champDict and champDictColour
    championCount += 1
    i = i.strip()
    i = i.split(", ")
    icopy = i
    j[championCount] = i[0]
    if i[-1] == "4": #to assign mastery colour to champion names
        champDictColour[championCount] = 4
    elif i[-1] == "5":
        champDictColour[championCount] = 5
    elif i[-1] == "6":
        champDictColour[championCount] = 6
    elif i[-1] == "7":
        champDictColour[championCount] = 7
    else:
        champDictColour[championCount] = 1


def championMasteryColourDecider(i, value): #function to return which colour for champion mastery
    if champDictColour[i] == 4: #Yellow for L4
        return colourYellow
    elif champDictColour[i] == 5: #Red for L5
        return colourLightRed
    elif champDictColour[i] == 6: #Purple for L6
        return colourLightPurple
    elif champDictColour[i] == 7: #Light Blue for L7
        return colourLightBlue
    else: #White for the rest
        if value == 1:
            return colourLeagueText
        return colourActuallyWhite

def masteryValueCheck(averageMastery): #function to return the associated string for value (1 -> S+) (give 1 to get S+)
    with open(masteryGradesPath, "r") as masteryGradesFile:
        for m in masteryGradesFile:
            if int((m.strip().split(", "))[1]) == averageMastery:
                return (m.strip().split(", "))[0]
        return ""

def masteryValueCheckReverse(masteryValue): #function to return the associated value for string (S+ -> 1) (give S+ to get 1)
    with open(masteryGradesPath, "r") as masteryGradesFile:
        for m in masteryGradesFile:
            if (m.strip().split(", "))[0] == masteryValue:
                return int((m.strip().split(", "))[1])
        return ""

def masteryBarHighlight(wID): #change all the things to highlight
    champDictBackgroundIMG[wID].config(image = championBorderImageHighlight)
    champEachMasteryDict[wID].config(bg = colour88Black)
    champImageDict[wID].config(bg = colour88Black)
    champDict[wID].config(bg = colour88Black)
    totalGamesPlayedDict[wID].config(bg = colour88Black)
    averageMasteryDict[wID].config(bg = colour88Black)

def masteryBarUnHighlight(wID): #change back all the things to default
    champDictBackgroundIMG[wID].config(image = championBorderImage)
    champEachMasteryDict[wID].config(bg = colour89Black)
    champImageDict[wID].config(bg = colour89Black)
    champDict[wID].config(bg = colour89Black)
    totalGamesPlayedDict[wID].config(bg = colour89Black)
    averageMasteryDict[wID].config(bg = colour89Black)

def getBGWidgetID(winfo):
    if winfo == "":
        return 0
    winfo = int(winfo) - 1 #-1 is important due to label naming convention
    while winfo % 6 != 0:
        winfo -= 1
    return int(winfo/6)

def changeNew(event): #event handler for highlight
    masteryBarHighlight(getBGWidgetID(event.widget.winfo_name().strip("!label")))

def changeNormal(event): #event handler for unhighlight
    masteryBarUnHighlight(getBGWidgetID(event.widget.winfo_name().strip("!label")))

def championIDCheck(championName):
    for i in range(len(j)):
        if j[i] == championName:
            return i
    return -1

#main code for mastery tab (for initializing)
for i in range(championCount+1): #displaying champion names (champDict), rounded rect behind names (champDictBackgroundIMG), each mastery count (champEachMasteryDict), champion images, total games Label
    masteryChampionLine = readSeasonLine(j[i], currentSeasonFilePath) #invoke function to get the line of the specific champion
    masteryChampionLineStr = "" #empty string to store string later

    championImageDict[i] = PhotoImage(file = champImagePath + j[i] + ".png")

    for k in range(1, len(masteryChampionLine) - 1): #loop through the 15 masteries and apply ljust accordingly, each time adding the mastery count to masteryChampionLineStr
        if int(masteryChampionLine[k]) == 0: #for values of 0, replace with a space to not show 0
            masteryChampionLineStr += "".ljust(int(1/100 * intScreenX + 2))
        elif int(masteryChampionLine[k]) < 10: #for values of 1 digit...
            masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX))
        elif int(masteryChampionLine[k]) < 100: #for values of 2 digits...
            masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX) - 2)
        else: #for values of other digits...
            masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX) - 4)
        if k == 15: #when k == 15,
            #total games & average mastery section
            totalGamesPlayed = 0 #set total games to 0
            averageMastery = 0 #set average mastery to 0
            for l in range(1, len(masteryChampionLine) - 1): #loop through the 15 masteries
                grandTotalGamesPlayed += int(masteryChampionLine[l].strip()) #add total games played for each champ to grand total for all champs
                totalGamesPlayed += int(masteryChampionLine[l].strip()) #add each game in each mastery to total games
                averageMastery += (int(masteryChampionLine[l].strip()) * l) #add value of each game in each mastery to average mastery
            if totalGamesPlayed == 0: #if it's still 0, then set it as ""
                totalGamesPlayed = ""
            if averageMastery == 0: #if it's still 0, then set it as ""
                averageMastery = ""
            else: #if not, divide average mastery by total games played and add average mastery to total average mastery
                totalAverageMastery += averageMastery
                averageMastery = round(averageMastery / totalGamesPlayed)
        totalGamesPerMastery[k-1] += int(masteryChampionLine[k]) #add the count of each mastery to each index respectively

    #rounded rect behind names (champDictBackgroundIMG)
    champDictBackgroundIMG[i] = Label(masteryFrame, bg = colour87Black, image = championBorderImage)
    champDictBackgroundIMG[i].place(relx = 8/480, y = i * masteryRowHeightInpx)

    #champion images
    champImageDict[i] = Label(masteryFrame, bg = colour89Black, image = championImageDict[i])
    champImageDict[i].place(relx = 12/480, y = i * masteryRowHeightInpx + 15)

    #champion names (champDict)
    champDict[i] = Label(masteryFrame, bg = colour89Black, fg = championMasteryColourDecider(i, 0), font = ("BeaufortforLOL-Bold", 13), text = j[i])
    champDict[i].place(relx = 30/480, y = i * masteryRowHeightInpx + masteryRowHeightInpx/4)

    #each mastery count (champEachMasteryDict)
    champEachMasteryDict[i] = Label(masteryFrame, bg = colour89Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15), text = masteryChampionLineStr)
    champEachMasteryDict[i].place(relx = 75/480, y = i * masteryRowHeightInpx + masteryRowHeightInpx/4.5)

    #total games Label
    totalGamesPlayedDict[i] = Label(masteryFrame, bg = colour89Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15), text = totalGamesPlayed, anchor = "center", width = 5)
    totalGamesPlayedDict[i].place(relx = 390/480, y = i * masteryRowHeightInpx + masteryRowHeightInpx/4.5)

    #average master Label
    averageMasteryDict[i] = Label(masteryFrame, bg = colour89Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15), text = str(masteryValueCheck(averageMastery)), anchor = "center", width = 5)
    averageMasteryDict[i].place(relx = 432/480, y = i * masteryRowHeightInpx + masteryRowHeightInpx/4.5)

    #binds
    champEachMasteryDict[i].bind("<Enter>", changeNew)
    champEachMasteryDict[i].bind("<Leave>", changeNormal)
    champImageDict[i].bind("<Enter>", changeNew)
    champImageDict[i].bind("<Leave>", changeNormal)
    champDict[i].bind("<Enter>", changeNew)
    champDict[i].bind("<Leave>", changeNormal)
    totalGamesPlayedDict[i].bind("<Enter>", changeNew)
    totalGamesPlayedDict[i].bind("<Leave>", changeNormal)
    averageMasteryDict[i].bind("<Enter>", changeNew)
    averageMasteryDict[i].bind("<Leave>", changeNormal)
    champDictBackgroundIMG[i].bind("<Enter>", changeNew)
    champDictBackgroundIMG[i].bind("<Leave>", changeNormal)
    champImageDict[i].bind("<MouseWheel>", masteryScrollWheel)
    averageMasteryDict[i].bind("<MouseWheel>", masteryScrollWheel)
    totalGamesPlayedDict[i].bind("<MouseWheel>", masteryScrollWheel)
    champEachMasteryDict[i].bind("<MouseWheel>", masteryScrollWheel)
    champDictBackgroundIMG[i].bind("<MouseWheel>", masteryScrollWheel)
    champDict[i].bind("<MouseWheel>", masteryScrollWheel)

def masteryMainCode2(): #second same function as above but cleaner for invoking after initializing
    global masteryChampionLine, masteryChampionLineStr, totalGamesPlayed, averageMastery, grandTotalGamesPlayed, totalAverageMastery, champEachMasteryDict, totalGamesPlayedDict, averageMasteryDict, totalGamesPerMastery
    grandTotalGamesPlayed += 1
    for i in range(championCount+1): #finding the champion by iterative search
        if j[i] == selectedChampion:
            masteryChampionLineStr = "" #empty string to store string later
            masteryChampionLine = readSeasonLine(j[i], currentSeasonFilePath) #invoke function to get the line of the specific champion

            for k in range(1, len(masteryChampionLine) - 1): #loop through the 15 masteries and apply ljust accordingly, each time adding the mastery count to masteryChampionLineStr
                if int(masteryChampionLine[k]) == 0: #for values of 0, replace with a space to not show 0
                    masteryChampionLineStr += "".ljust(int(1/100 * intScreenX + 2))
                elif int(masteryChampionLine[k]) < 10: #for values of 1 digit...
                    masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX))
                elif int(masteryChampionLine[k]) < 100: #for values of 2 digits...
                    masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX) - 2)
                else: #for values of other digits...
                    masteryChampionLineStr += masteryChampionLine[k].ljust(int(1/100 * intScreenX) - 4)
                if k == 15: #when k == 15,
                    #total games & average mastery section
                    totalGamesPlayed, averageMastery = 0, 0 #set total games and average mastery to 0
                    #averageMastery = 0 #set average mastery to 0
                    for l in range(1, len(masteryChampionLine) - 1): #loop through the 15 masteries
                        totalGamesPlayed += int(masteryChampionLine[l].strip()) #add each game in each mastery to total games
                        averageMastery += (int(masteryChampionLine[l].strip()) * l) #add value of each game in each mastery to average mastery
                    if totalGamesPlayed == 0: #if it's still 0, then set it as ""
                        totalGamesPlayed = ""
                    if averageMastery == 0: #if it's still 0, then set it as ""
                        averageMastery = ""
                    else: #if not, divide average mastery by total games played and add average mastery to total average mastery
                        totalAverageMastery += masteryValueCheckReverse(finalMasteryFrontString + finalMasteryBackString)
                        averageMastery = round(averageMastery / totalGamesPlayed)
            totalGamesPerMastery[masteryValueCheckReverse(finalMasteryFrontString + finalMasteryBackString) - 1] += 1 #add the count of changed mastery to the specific index
            #refreshing the labels with updated text
            champEachMasteryDict[i].config(text = masteryChampionLineStr) 
            totalGamesPlayedDict[i].config(text = totalGamesPlayed)
            averageMasteryDict[i].config(text = str(masteryValueCheck(averageMastery)))

#footer
#grand total mastery average
def totalAverageMasteryFunction(totalAverageMastery, grandTotalGamesPlayed):
    if grandTotalGamesPlayed != 0:
        totalAverageMastery /= grandTotalGamesPlayed
        totalAverageMastery = masteryValueCheck(round(totalAverageMastery))
    return totalAverageMastery
totalAverageMasteryLabel = Label(footerFrame, text = totalAverageMasteryFunction(totalAverageMastery, grandTotalGamesPlayed), bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15))
totalAverageMasteryLabel.place(relx = 437/480, rely = 0.05)

#Total Count Label
totalCountLabel = Label(footerFrame, text = "Total Count", bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15))
totalCountLabel.place(relx = 14/480, rely = 0.05)

#grand total games played Label
grandTotalGamesPlayedLabel = Label(footerFrame, text = grandTotalGamesPlayed, bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15))
grandTotalGamesPlayedLabel.place(relx = 396/480, rely = 0.05)

#totalGamesPerMastery Label
def totalGamesPerMasteryCountFunction():
    global totalGamesPerMasteryString
    global totalGamesPerMasteryLabel
    totalGamesPerMasteryString = ""
    for n in range(15):
        if int(totalGamesPerMastery[n]) < 10: #for values of 1 digit...
            totalGamesPerMasteryString += str(totalGamesPerMastery[n]).ljust(int(1/100 * intScreenX))
        elif int(totalGamesPerMastery[n]) < 100: #for values of 2 digits...
            if int(totalGamesPerMastery[n + 1]) < 10:
                totalGamesPerMasteryString += str(totalGamesPerMastery[n]).ljust(int(1/100 * intScreenX))
            else:
                totalGamesPerMasteryString += str(totalGamesPerMastery[n]).ljust(int(1/100 * intScreenX) - 2)     
        else: #for values of other digits...
            totalGamesPerMasteryString += str(totalGamesPerMastery[n]).ljust(int(1/100 * intScreenX) - 4)
    totalGamesPerMasteryLabel = Label(footerFrame, bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 15), text = totalGamesPerMasteryString)
    totalGamesPerMasteryLabel.place(relx = 76/480, rely = 0.05)
totalGamesPerMasteryCountFunction()
currentSeasonFile.close()
#end of footer

#mastery tab backend continuation
masteryCanvas.create_window((0, 0), window = masteryFrame, anchor = "nw", width = intScreenX, height = (championCount+1) * masteryRowHeightInpx) #a window of frame inside the canvas used to store any widgets
masteryCanvas.configure(yscrollcommand = masteryScrollbar.set) #enable scrolling?
masteryScrollbar.config(command = masteryCanvas.yview)

masteryFrame.bind("<Configure>", scrollingMain) #enable scrolling?
masteryFrame.bind("<MouseWheel>", masteryScrollWheel) #scrolling with scrollwheel bind

#mastery header
ljustValue = int(1/160 * intScreenX) #text spacing values. Dynamic
masteryTitle = Label(secondFromTopFrame, text = "CHAMPION", bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 19))
masteryTitleS = Label(secondFromTopFrame, text = "S+".ljust(ljustValue) + "S".ljust(ljustValue) + "S-".ljust(ljustValue), bg = colour91Black, fg = colourLightPurple, font = ("BeaufortforLOL-Bold", 18))
masteryTitleA = Label(secondFromTopFrame, text = "A+".ljust(ljustValue) + "A".ljust(ljustValue) + "A-".ljust(ljustValue), bg = colour91Black, fg = colourLightRed, font = ("BeaufortforLOL-Bold", 18))
masteryTitleB = Label(secondFromTopFrame, text = "B+".ljust(ljustValue) + "B".ljust(ljustValue) + "B-".ljust(ljustValue), bg = colour91Black, fg = colourOrange, font = ("BeaufortforLOL-Bold", 18))
masteryTitleC = Label(secondFromTopFrame, text = "C+".ljust(ljustValue) + "C".ljust(ljustValue) + "C-".ljust(ljustValue), bg = colour91Black, fg = colourYellow, font = ("BeaufortforLOL-Bold", 18))
masteryTitleD = Label(secondFromTopFrame, text = "D+".ljust(ljustValue) + "D".ljust(ljustValue) + "D-".ljust(ljustValue), bg = colour91Black, fg = colour25Black, font = ("BeaufortforLOL-Bold", 18))
masteryTitleTotal = Label(secondFromTopFrame, text = "Total\nGames", bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", int(intScreenX * 0.01)))
masteryTitleAvgScore = Label(secondFromTopFrame, text = "Average\nRating", bg = colour91Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", int(intScreenX * 0.01)))
masteryTitle.place(relx = 11/480, rely = 0.17)
masteryTitleS.place(relx = 75/480, rely = 0.18)
root.update_idletasks()
masterySWidth = int(masteryTitleS.winfo_width() * (480/intScreenX))
masteryTitleA.place(relx = (72 + masterySWidth)/480, rely = 0.18)
masteryTitleB.place(relx = (74 + 2 * masterySWidth)/480, rely = 0.18)
masteryTitleC.place(relx = (74 + 3 * masterySWidth)/480, rely = 0.18)
masteryTitleD.place(relx = (74 + 4 * masterySWidth)/480, rely = 0.18)
masteryTitleTotal.place(relx = 391/480, rely = 0.01)
masteryTitleAvgScore.place(relx = 431/480, rely = 0.01)

def showMastery():
    mainMasteryFrame.pack(fill = BOTH)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Add Mastery Finish under add things tab---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
selectMasteryFinishFrame = Frame(mainFrame, bg = colour87Black, width = intScreenX, height = intScreenY, bd = 0)

def selectMasteryFinishFramePack():
    selectMasteryFinishFrame.pack(fill = BOTH)

selectMasteryFinishCentre = Label(selectMasteryFinishFrame, bg = colour87Black, image = selectMasteryFinishCentreImage)
selectMasteryFinishAgain = Label(selectMasteryFinishFrame, bg = colour87Black, image = selectMasteryFinishAgainImage, cursor = "hand2")
selectMasteryFinishIcon = Label(selectMasteryFinishFrame, bg = colour87Black)
selectMasteryFinishText = Label(selectMasteryFinishFrame, width = 15, font = ("BeaufortforLOL-Bold", 20), anchor = "center", bg = colour87Black, fg = colourLeagueText)
selectMasteryFinishMasteryText = Label(selectMasteryFinishFrame, width = 2, font = ("BeaufortforLOL-Bold", 20), anchor = "center", bg = colour87Black, fg = colourLeagueText)
selectMasteryFinishMasteryCount = Label(selectMasteryFinishFrame, width = 15, font = ("BeaufortforLOL-Bold", 12), anchor = "center", bg = colour87Black, fg = colourLeagueText, text = "(+1)")

def selectMasteryFinishConfig():
    global someImage2
    someImage2 = PhotoImage(file = champImagePath120x120 + j[selectChampionClickedID] + ".png")
    selectMasteryFinishIcon.config(image = someImage2)
    selectMasteryFinishText.config(text = (j[selectChampionClickedID]).upper())
    selectMasteryFinishMasteryText.config(text = finalMasteryFrontString + finalMasteryBackString)

def selectMasteryFinish():
    selectMasteryFinishConfig()
    selectMasteryProgressBar.place(relx = 435/1280, rely = 0.085)
    selectMasteryProgressBar.config(image = selectMasteryProgress[2])

def addAgainCheckX(): #0 for home, 1 for again
    cursorX = selectMasteryLetterFrame.winfo_pointerx() - selectMasteryLetterFrame.winfo_rootx()
    if cursorX < 551:
        return 0
    return 1

def addAgainClick(event):
    if addAgainCheckX() == 0:
        masteryClickNE() #mastery click
    else:
        showSelectChampionMasteryNE()

selectMasteryFinishCentre.place(relx = 458/1280, rely = 250/720)
selectMasteryFinishAgain.place(relx = 497/1280, rely = 573/720)
selectMasteryFinishIcon.place(relx = 573/1280, rely = 282/720)
selectMasteryFinishText.place(relx = 512/1280, rely = 212/720)
selectMasteryFinishMasteryText.place(relx = 618/1280, rely = 404/720)
selectMasteryFinishMasteryCount.place(relx = 565/1280, rely = 440/720)

selectMasteryFinishAgain.bind("<ButtonRelease-1>", addAgainClick)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Choose Mastery Letter under add things tab-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#frames
selectMasteryLetterFrame = Frame(mainFrame, bg = colour87Black, width = intScreenX, height = intScreenY, bd = 0)

#variables and dictionaries
circlesTop = {}
circlesBottom = {}
masteryLettersDict = {}
masteryLetters2Dict = {}
masteryLettersDropDownDict = {}
masteryConnectorRing = {}
masteryConnectorCentre = {}
masterySelected = None
masterySelectedSign = 1
finalMasteryFrontString = ""
finalMasteryBackString = ""

#functions and event handlers
def masteryIDCheck(): #function to check which mastery letter was clicked via coordinates
    cursorX = selectMasteryLetterFrame.winfo_pointerx() - selectMasteryLetterFrame.winfo_rootx()
    cursorY = selectMasteryLetterFrame.winfo_pointery() - selectMasteryLetterFrame.winfo_rooty()
    if cursorY > 350:
        if cursorX < 700:
            return 0
        else:
            return 4
    elif cursorX < 600:
        return 1
    elif cursorX > 700:
        return 3
    return 2

def signIDCheck(): #function to check which mastery sign was clicked via coordinates
    cursorX = selectMasteryLetterFrame.winfo_pointerx() - selectMasteryLetterFrame.winfo_rootx()
    if cursorX < 600:
        return 0
    elif cursorX > 700:
        return 2
    return 1

def connectorPlace(ID): #function to place the correct centre connector with a given id
    if ID == 0:
        masteryConnectorCentre[0].place(relx = 499/1280, rely = 376/720)
    elif ID == 1:
        masteryConnectorCentre[1].place(relx = 551/1280, rely = 298/720)
    elif ID == 2:
        masteryConnectorCentre[2].place(relx = 628/1280, rely = 271/720)
    elif ID == 3:
        masteryConnectorCentre[3].place(relx = 685/1280, rely = 296/720)
    elif ID == 4:
        masteryConnectorCentre[4].place(relx = 702/1280, rely = 376/720)
    elif ID == 5:
        masteryConnectorCentre[5].place(relx = 546/1280, rely = 425/720)
    elif ID == 6:
        masteryConnectorCentre[6].place(relx = 628/1280, rely = 425/720)
    else:
        masteryConnectorCentre[7].place(relx = 685/1280, rely = 425/720)

def showMasteryToAddString(value): #function to show the selected mastery. Value is to check if the sign selected is None or +/-. 1 for None.
    global finalMasteryFrontString, finalMasteryBackString
    if masterySelectedSign == 0: #set the correct sign into finalMasteryBackString
        finalMasteryBackString = "+"
    elif masterySelectedSign == 2:
        finalMasteryBackString = "-" 
    else:
        finalMasteryBackString = ""
    if masterySelected != None: #to check if any mastery alphabet was selected
        finalMasteryFrontString = masteryValueCheck(masterySelected * 3 + 2) #set finalMasteryFrontString to the correct alphabet
        if value == 1: #display correct string depending on the selected sign
            finalMasteryTextLabel.config(text = finalMasteryFrontString)
        else:
            finalMasteryTextLabel.config(text = finalMasteryFrontString + finalMasteryBackString)
        #final text colours
        if finalMasteryFrontString == "S":
            finalMasteryTextLabel.config(fg = colourLightPurple)
        elif finalMasteryFrontString == "A":
            finalMasteryTextLabel.config(fg = colourLightRed)
        elif finalMasteryFrontString == "B":
            finalMasteryTextLabel.config(fg = colourOrange)
        elif finalMasteryFrontString == "C":
            finalMasteryTextLabel.config(fg = colourYellow)
        else:
            finalMasteryTextLabel.config(fg = colour25Black)

def masteryChooseSelect(event): #event handler for clicking the 5 masteries
    masteryDropdownID = masteryIDCheck() #get which alphabet was clicked
    global masterySelected
    if masterySelected != None: #deselect previous
        circlesTop[masterySelected].config(image = selectMasteryCircleImage)
        masteryConnectorCentre[masterySelected].place_forget()
    masterySelected = masteryDropdownID #set it to the new alphabet id
    #select new
    circlesTop[masterySelected].config(image = selectMasteryCircleImageHighlight)
    connectorPlace(masterySelected)
    showMasteryToAddString(0)
    masteryConfirmSelection.config(image = selectMasteryConfirmSelectionImage, cursor = "hand2")
    masteryConfirmSelection.bind("<Enter>", lambda e: masteryConfirmSelection.config(image = selectMasteryConfirmSelectionImageHighlight))
    masteryConfirmSelection.bind("<Leave>", lambda e: masteryConfirmSelection.config(image = selectMasteryConfirmSelectionImage))
    masteryConfirmSelection.bind("<ButtonRelease-1>", masteryConfirmSelectionClicked)

def masterySignSelect(event): #event handler to click on the 3 signs
    masteryDropdownID2 = signIDCheck() #get which sign was clicked
    global masterySelectedSign
    #deselect previous
    circlesBottom[masterySelectedSign].config(image = selectMasteryCircleImage)
    masteryConnectorCentre[masterySelectedSign + 5].place_forget()
    #set it to the new sign id
    masterySelectedSign = masteryDropdownID2
    #select new
    circlesBottom[masterySelectedSign].config(image = selectMasteryCircleImageHighlight)
    connectorPlace(masterySelectedSign + 5)
    if masterySelectedSign != 1:
        showMasteryToAddString(0)
    else:
        showMasteryToAddString(1)

def masteryChooseHighlight(event): #event handler for highlighting the 5 masteries
    masteryDropdownID = masteryIDCheck()
    if masteryDropdownID != masterySelected:
        circlesTop[masteryDropdownID].config(image = selectMasteryCircleImageHighlight)

def masteryChooseUnHighlight(event): #event handler for unhighlighting the 5 masteries
    masteryDropdownID = masteryIDCheck()
    if masteryDropdownID != masterySelected:
        circlesTop[masteryDropdownID].config(image = selectMasteryCircleImage)

def masterySignHighlight(event): #event handler for highlighting the 3 signs
    masteryDropdownID2 = signIDCheck()
    if masteryDropdownID2 != masterySelectedSign:
        circlesBottom[masteryDropdownID2].config(image = selectMasteryCircleImageHighlight)

def masterySignUnHighlight(event): #event handler for unhighlighting the 3 signs
    masteryDropdownID2 = signIDCheck()
    if masteryDropdownID2 != masterySelectedSign:
        circlesBottom[masteryDropdownID2].config(image = selectMasteryCircleImage)

def masteryConfirmSelectionClicked(event): #event handler for clicking mastery confirm
    if finalMasteryFrontString == "": #end the event handler if the user has not clicked on any masteries
        return
    editSeason(selectedChampion, masteryValueCheckReverse(finalMasteryFrontString + finalMasteryBackString), 1, currentSeasonFilePath) #write to the current file
    hideALL()
    masteryMainCode2() #update mastery page
    totalGamesPerMasteryCountFunction() #update mastery total
    grandTotalGamesPlayedLabel.config(text = grandTotalGamesPlayed, cursor = "hand2") #update text
    totalAverageMasteryLabel.config(text = totalAverageMasteryFunction(totalAverageMastery, grandTotalGamesPlayed)) #update text
    selectMasteryFinishFramePack()
    selectMasteryFinish()
    #masteryClickNE() #mastery click


#main code for this section
for masteryLetterIndex2 in range(5): #for loop separated from next for loop for layering
    circlesTop[masteryLetterIndex2] = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryCircleImage, cursor = "hand2")
    circlesTop[masteryLetterIndex2].bind("<Enter>", masteryChooseHighlight)
    circlesTop[masteryLetterIndex2].bind("<Leave>", masteryChooseUnHighlight)
    circlesTop[masteryLetterIndex2].bind("<ButtonRelease-1>", masteryChooseSelect)
    if masteryLetterIndex2 < 3:
        circlesBottom[masteryLetterIndex2] = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryCircleImage, cursor = "hand2")
        circlesBottom[masteryLetterIndex2].bind("<Enter>", masterySignHighlight)
        circlesBottom[masteryLetterIndex2].bind("<Leave>", masterySignUnHighlight)
        circlesBottom[masteryLetterIndex2].bind("<ButtonRelease-1>", masterySignSelect)

for masteryLetterIndex in range(8):
    #Connector to centre
    masteryConnectorCentre[masteryLetterIndex] = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryConnectorCentreImage[masteryLetterIndex])
    if masteryLetterIndex == masterySelectedSign + 5: #initialize which sign is selected by default
        circlesBottom[masterySelectedSign].config(image = selectMasteryCircleImageHighlight)
        connectorPlace(masteryLetterIndex)
    if masteryLetterIndex< 6: #Connector Rings
        masteryConnectorRing[masteryLetterIndex] = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryConnectorRingImage[masteryLetterIndex])
        if masteryLetterIndex < 5: #S to D
            #labels
            masteryLettersDict[masteryLetterIndex] = Label(selectMasteryLetterFrame, bg = colour87Black, text = masteryValueCheck((masteryLetterIndex + 1) * 3 - 1), font = ("BeaufortforLOL-Bold", 20), fg = colourLeagueText, cursor = "hand2", anchor = "center")
            #fg colouring
            if masteryValueCheck((masteryLetterIndex + 1) * 3 - 1) == "S":
                masteryLettersDict[masteryLetterIndex].config(fg = colourLightPurple)
            elif masteryValueCheck((masteryLetterIndex + 1) * 3 - 1) == "A":
                masteryLettersDict[masteryLetterIndex].config(fg = colourLightRed)
            elif masteryValueCheck((masteryLetterIndex + 1) * 3 - 1) == "B":
                masteryLettersDict[masteryLetterIndex].config(fg = colourOrange)
            elif masteryValueCheck((masteryLetterIndex + 1) * 3 - 1) == "C":
                masteryLettersDict[masteryLetterIndex].config(fg = colourYellow)
            else:
                masteryLettersDict[masteryLetterIndex].config(fg = colour25Black)
            #binds
            masteryLettersDict[masteryLetterIndex].bind("<Enter>", masteryChooseHighlight)
            masteryLettersDict[masteryLetterIndex].bind("<Leave>", masteryChooseUnHighlight)
            masteryLettersDict[masteryLetterIndex].bind("<ButtonRelease-1>", masteryChooseSelect)
            if masteryLetterIndex < 3: #+, None, -
                #labels
                masteryLetters2Dict[masteryLetterIndex] = Label(selectMasteryLetterFrame, bg = colour87Black, font = ("BeaufortforLOL-Bold", 20), fg = colourLeagueText, cursor = "hand2", anchor = "center", width = 1)
                if masteryLetterIndex == 0:
                    masteryLetters2Dict[masteryLetterIndex].config(text = "+")
                elif masteryLetterIndex == 1:
                    masteryLetters2Dict[masteryLetterIndex].config(bg = colour87Black)
                elif masteryLetterIndex == 2:
                    masteryLetters2Dict[masteryLetterIndex].config(text = "-")
                #binds
                masteryLetters2Dict[masteryLetterIndex].bind("<Enter>", masterySignHighlight)
                masteryLetters2Dict[masteryLetterIndex].bind("<Leave>", masterySignUnHighlight)
                masteryLetters2Dict[masteryLetterIndex].bind("<ButtonRelease-1>", masterySignSelect)


#labels, placing and binds
masteryConfirmSelection = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryConfirmSelectionImageBlocked, anchor = "center")
masteryCentre = Label(selectMasteryLetterFrame, bg = colour87Black, image = selectMasteryCentreImage)

#placings. Individuals as each are at different places. No equations were really found to simplify it
masteryConnectorRing[0].place(relx = (466.5 + 7)/1280, rely = (237 + 66)/720)
masteryConnectorRing[1].place(relx = (466.5 + 83)/1280, rely = (237 + 3)/720)
masteryConnectorRing[2].place(relx = (466 + 203)/1280, rely = (237 + 2)/720)
masteryConnectorRing[3].place(relx = (466.5 + 313)/1280, rely = (237 + 63)/720)
masteryConnectorRing[4].place(relx = (466.5 + 84)/1280, rely = (237 + 279)/720)
masteryConnectorRing[5].place(relx = (466.5 + 202.5)/1280, rely = (237 + 281)/720)
masteryCentre.place(relx = 580/1280, rely = 343/720)
circlesTop[0].place(relx = 437/1280, rely = 356/720)
circlesTop[1].place(relx = 493.5/1280, rely = 248.5/720)
circlesTop[2].place(relx = 606.5/1280, rely = 209.5/720)
circlesTop[3].place(relx = 726.5/1280, rely = 248.5/720)
circlesTop[4].place(relx = 783.5/1280, rely = 356/720)
circlesBottom[0].place(relx = 493.5/1280, rely = 465.5/720)
circlesBottom[1].place(relx = 606.5/1280, rely = 514.5/720)
circlesBottom[2].place(relx = 726.5/1280, rely = 465.5/720)
masteryLettersDict[0].place(relx = (437 + 21)/1280, rely = (356 + 9)/720)
masteryLettersDict[1].place(relx = (493.5 + 19)/1280, rely = (248.5 + 9)/720)
masteryLettersDict[2].place(relx = (606.5 + 20)/1280, rely = (209.5 + 10)/720)
masteryLettersDict[3].place(relx = (726.5 + 19)/1280, rely = (248.5 + 9)/720)
masteryLettersDict[4].place(relx = (783.5 + 20)/1280, rely = (356 + 10)/720)
masteryLetters2Dict[0].place(relx = (493.5 + 20.5)/1280, rely = (465.5 + 8)/720)
masteryLetters2Dict[2].place(relx = (726.5 + 21)/1280, rely = (465.5 + 8)/720)
masteryConfirmSelection.place(relx = 0.38, rely = 627/720)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Select Champion under add things tab-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def showSelectChampionFrame(): #function to place the frame for select champion
    selectChampionFrame.pack(fill = BOTH) #delete

def placeSelectChampionLeftIcons(): #function to place these stuff as they are in root
    selectChampionUnselectedChampion.place(relx = 620/1280, rely = 140/720)
    selectChampionSelectedChampionText.place(relx = 587.5/1280, rely = 180/720)
    
#labels
selectChampionUnselectedChampion = Label(selectMasteryLetterFrame, bg = colour87Black, bd = 0, image = selectChampionUnselectedImage, cursor = "hand2")
selectChampionSelectedChampionText = Label(selectMasteryLetterFrame, bg = colour87Black, bd = 0, width = 15, anchor = "center", font = ("BeaufortforLOL-Bold", 10), fg = colourLeagueText)

finalMasteryTextLabel = Label(selectMasteryLetterFrame, bg = colour87Black, font = ("BeaufortforLOL-Bold", 25), fg = colourLeagueText, width = 2, anchor = "center")

#keeping track of which add new was selected
selectedAddNew = None
def showSelectShared():
    hideALL()
    placeSelectChampionLeftIcons()
    showSelectChampionFrame()

def showSelectChampionLevel(event):
    global selectedAddNew
    selectedAddNew = "Level"
    showSelectShared()
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")

def showSelectChampionMastery(event):
    global selectedAddNew
    selectedAddNew = "Mastery"
    showSelectShared()
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")
    selectMasteryProgressBar.place(relx = 435/1280, rely = 0.085)
    selectMasteryProgressBar.config(image = selectMasteryProgress[0])

def showSelectChampionMasteryNE(): #non-event
    global selectedAddNew
    selectedAddNew = "Mastery"
    showSelectShared()
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")
    selectMasteryProgressBar.place(relx = 435/1280, rely = 0.085)
    selectMasteryProgressBar.config(image = selectMasteryProgress[0])

def showSelectChampionRanked(event):
    global selectedAddNew
    selectedAddNew = "Ranked"
    showSelectShared()
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")

selectChampionUnselectedChampion.bind("<ButtonRelease-1>", showSelectChampionMastery)

#select champions tab v2
#dictionaries & variables
selectChampionChampionsDict = {}
selectChampionChampionsLabelDict = {}
selectChampionChampionsImageDict = {}
selectChampionChampionsImagePathDict = {}
selectChampionSort = {}
selectedChampion = None #variable to keep track of which champion is selected
selectedLane = -1

#early event handlers
def selectChampionSortClicked(event):
    global selectedLane
    laneID = int(event.widget.winfo_name().strip("!label")) - 8
    if selectedLane != laneID:
        selectChampionSortUnderline.place(relx = (463 + laneID * 80)/1280, rely = 247/720)
        selectedLane = laneID
    else:
        selectChampionSortUnderline.place_forget()
        selectedLane = -1
    selectChampionSearchBoxPressedShared("")

#Widgets
selectChampionFrame = Frame(mainFrame, bg = colour87Black, width = intScreenX, height = intScreenY, bd = 0)
selectChampionDropdownFrame = Frame(selectChampionFrame, bg = colour87Black, width = 435, height = 300)
selectChampionCanvas = Canvas(selectChampionDropdownFrame, bg = colour87Black, width = 439, height = 270, relief = FLAT, bd = -2)
selectChampionDropdownFrameInner = Frame(selectChampionCanvas, bg = colour87Black, width = 400, height = 300)

selectChampionSearchBoxBGHighlight = Label(selectChampionFrame, bg = colourLeagueText, width = 62, height = 3, bd = 3)
selectChampionSearchBoxBG = Label(selectChampionFrame, cursor = "xterm", bg = colour90Black, width = 62, height = 3)

selectChampionSearchBox = Entry(selectChampionFrame, bg = colour90Black, fg = colourActuallyWhite, bd = 0, font = ("BeaufortforLOL-Bold", 20), width = 28, insertbackground = colourActuallyWhite)
selectChampionScrollbar = Scrollbar(selectChampionCanvas, bg = colour87Black, troughcolor = colour87Black, activebackground = colour87Black, activerelief = FLAT) #mastery scrollbar

selectMasteryProgressBar = Label(mainFrame, bg = colour87Black, image = selectMasteryProgress[0])
selectChampionInputPrompt = Label(selectChampionFrame, cursor = "xterm", bg = colour90Black, fg = colour64Black, text = "Search Champions here...", font = ("BeaufortforLOL-Bold", 16))
selectChampionEnter = Label(selectChampionFrame, cursor = "xterm", bg = colour90Black, image = selectChampionEnterImage)
selectChampionNotFound = Label(selectChampionFrame, bg = colour90Black, fg = colourActuallyWhite, height = 2, text = "Nothing found :(", width = 36, font = ("BeaufortforLOL-Bold", 16))

selectChampionText = Label(selectChampionFrame, bg = colour87Black, image = selectChampionTextImage)

selectChampionSortUnderline = Label(selectChampionFrame, bg = colour87Black, image = selectChampionSelectedLane)

for i in range(5): #lanes chooser widgets, placements and binds (all combined to avoid multiple loops)
    selectChampionSort[i] = Label(selectChampionFrame, bg = colour87Black, image = lanesImage[i], cursor = "hand2")
    selectChampionSort[i].place(relx = (465 + i * 80)/1280, rely = 222/720)
    selectChampionSort[i].bind("<ButtonRelease-1>", selectChampionSortClicked)

#placements
selectChampionSearchBoxBG.place(relx = 418/1280, rely = 270/720)
selectChampionSearchBox.place(relx = 427/1280, rely = 278/720)
selectChampionDropdownFrame.place(relx = 420/1280, rely = 324/720)
selectChampionCanvas.place(x = -2, y = -2)
selectChampionDropdownFrameInner.place(x = 12, y = 2)
selectChampionInputPrompt.place(relx = 428/1280, rely = 280/720)
selectChampionEnter.place(relx = 825/1280, rely = 288/720)
selectChampionText.place(relx = 227/1280, rely = 168/720)
#selectChampionScrollbar.place(x = 420, y = 0, height = 300)

#getting lanes of each champion
with open("data\\champions\\champions_database.txt", "r") as champDatabase:
    championLanes = []
    for line in champDatabase:
        championLanes.append(line.strip().split(", ")[1])

#functions
def scrollingChampions(event): #event for scroll scrollbar? Not sure
    selectChampionCanvas.configure(scrollregion = selectChampionCanvas.bbox("all"))

def selectChampionScrollWheel(event): #event for scroll wheel to scroll scrollbar
    global selectChampionChampionsDict
    if len(selectChampionChampionsDict) > 4:
        selectChampionCanvas.yview("scroll", int(event.delta/-90), "units")

def selectChampionSearchBoxLeave(event): #unselect input box
    selectChampionSearchBox.select_clear

def search(list1, userInput): #search algorithm
    global selectedLane, championLanes
    if userInput == "" and selectedLane == -1: #empty input with no filter, returns empty string
        return ""
    list2, list3 = [], []
    if userInput == "":
        for i in range(len(list1)): #iterates through champion list
            if int(championLanes[i]) == selectedLane: #if filter is matched, append champion to list 2
                if list1[i][0:len(userInput)].upper() == userInput.upper(): #if it matches the first part, add to list 2
                    list2.append("".ljust(15) + list1[i])
                elif userInput.upper() in list1[i].upper(): #if not but is part of the name, add to list 3
                    list3.append("".ljust(15) + list1[i])
        return list2 + list3  
    for i in range(len(list1)): #iterates through champion list
        if selectedLane == -1 or int(championLanes[i]) == selectedLane: #if no filter or when filter is matched, executes following codes
            if list1[i][0:len(userInput)].upper() == userInput.upper(): #if it matches the first part, add to list 2
                list2.append("".ljust(15) + list1[i])
            elif userInput.upper() in list1[i].upper(): #if not but is part of the name, add to list 3
                list3.append("".ljust(15) + list1[i])
    return list2 + list3 #returns list 2 with list 3

#event handlers for clicking entry box, highlight and unhighlight dropdown
def selectChampionClickLabel(event):
    frontID = selectChampionChampionsLabelDict[0].winfo_name().strip("!label")
    selectChampionClickShared(frontID, event.widget)

def selectChampionClickImage(event):
    frontID = selectChampionChampionsImageDict[0].winfo_name().strip("!label")
    selectChampionClickShared(frontID, event.widget)

def selectChampionHighlightLabel(event):
    frontID = selectChampionChampionsLabelDict[0].winfo_name().strip("!label")
    selectChampionHighlight(frontID, event.widget)

def selectChampionHighlightImage(event):
    frontID = selectChampionChampionsImageDict[0].winfo_name().strip("!label")
    selectChampionHighlight(frontID, event.widget)

def selectChampionUnHighlightLabel(event):
    frontID = selectChampionChampionsLabelDict[0].winfo_name().strip("!label")
    selectChampionUnHighlight(frontID, event.widget)

def selectChampionUnHighlightImage(event):
    frontID = selectChampionChampionsImageDict[0].winfo_name().strip("!label")
    selectChampionUnHighlight(frontID, event.widget)

#getting which dropdown it is
def getactualID(eWidget, frontID):
    widgetID = eWidget.winfo_name().strip("!label")
    if frontID == "": #separated as not mutually exclusive
        frontID = 1
    if widgetID == "":
        widgetID = 1
    return int(widgetID) - int(frontID)

#redirected after event handlers
def selectChampionClickShared(frontID, eWidget):
    global someImage, selectedChampion, selectChampionClickedID
    #click away, similar to clicking out of box
    selectChampionClickAway()
    #everything else
    actualID = getactualID(eWidget, frontID)
    selectChampionClickedID = championIDCheck(selectChampionChampionsDict[actualID].strip())
    someImage = PhotoImage(file = champImagePath + j[selectChampionClickedID] + ".png") #set this to a variable as it needs to be global
    selectChampionUnselectedChampion.config(image = someImage) #change the left image to the champion selected
    selectChampionSelectedChampionText.config(text = j[selectChampionClickedID], fg = championMasteryColourDecider(selectChampionClickedID, 1)) #show the name of the champion clicked
    selectMasteryProgressBar.config(image = selectMasteryProgress[1])
    selectedChampion = j[selectChampionClickedID]
    selectChampionFrame.pack_forget()
    finalMasteryTextLabel.place(relx = 618/1280, rely = 0.5)
    if selectedAddNew == "Level":
        pass
    elif selectedAddNew == "Mastery":
        selectMasteryLetterFrame.pack(fill = BOTH)
    elif selectedAddNew == "Ranked":
        pass

def selectChampionHighlight(frontID, eWidget):
    actualID = getactualID(eWidget, frontID)
    selectChampionChampionsImageDict[actualID].config(bg = colour88Black)
    selectChampionChampionsLabelDict[actualID].config(bg = colour88Black)
    
def selectChampionUnHighlight(frontID, eWidget):
    actualID = getactualID(eWidget, frontID)
    selectChampionChampionsImageDict[actualID].config(bg = colour90Black)
    selectChampionChampionsLabelDict[actualID].config(bg = colour90Black)

def selectChampionSearchBoxPressedShared(key): #search champion dynamic search algorithm
    global selectChampionChampionsDict, selectChampionChampionsLabelDict, selectChampionChampionsImageDict, selectChampionChampionsImagePathDict
    backspaceTrue = False
    if key == -1:
        backspaceTrue = True
        key = ""
    #delete past labels
    selectChampionNotFound.place_forget()
    for i in range(len(selectChampionChampionsLabelDict)):
        selectChampionChampionsLabelDict[i].destroy()
        selectChampionChampionsImageDict[i].destroy()
    selectChampionChampionsLabelDict, selectChampionChampionsDict, selectChampionChampionsImageDict, selectChampionChampionsImagePathDict = {}, {}, {}, {}
    
    #invoking search algorithm
    if key != "":
        searchList = search(j, selectChampionSearchBox.get() + key)
    elif backspaceTrue == True:
        searchList = search(j, selectChampionSearchBox.get()[0:-1])
    else:
        searchList = search(j, selectChampionSearchBox.get()[0:len(selectChampionSearchBox.get())])
    #what is going to be displayed
    if searchList != "": #as long as there is filter and/or user input, execute this
        for i in range(len(searchList)):
            selectChampionChampionsDict[i] = searchList[i]
            selectChampionChampionsLabelDict[i] = Label(selectChampionDropdownFrameInner, bg = colour90Black, width = 36, height = 2, text = selectChampionChampionsDict[i], font = ("BeaufortforLOL-Bold", 16), fg = colourActuallyWhite, anchor = "w", cursor = "hand2")
    else:
        for i in range(len(j)):
            selectChampionChampionsDict[i] = j[i]
            selectChampionChampionsLabelDict[i] = Label(selectChampionDropdownFrameInner, bg = colour90Black, width = 36, height = 2, text = "".ljust(15) + selectChampionChampionsDict[i], font = ("BeaufortforLOL-Bold", 16), fg = colourActuallyWhite, anchor = "w", cursor = "hand2")
    
    if searchList == []:
        selectChampionNotFound.place(relx = 418/1280, rely = 324/720)
    else:
        #displaying it
        for i in range(len(selectChampionChampionsDict)):
            selectChampionChampionsImagePathDict[i] = PhotoImage(file = champImagePath + selectChampionChampionsDict[i].strip() + ".png")
            selectChampionChampionsImageDict[i] = Label(selectChampionDropdownFrameInner, image = selectChampionChampionsImagePathDict[i], bg = colour90Black, cursor = "hand2")
            #placements
            selectChampionChampionsImageDict[i].place(x = 10, y = (i * 59 + 10))
            selectChampionChampionsLabelDict[i].place(x = 2, y = (i * 59 + 2))
            #binds
            selectChampionChampionsLabelDict[i].bind("<ButtonRelease-1>", selectChampionClickLabel)
            selectChampionChampionsImageDict[i].bind("<ButtonRelease-1>", selectChampionClickImage)
            selectChampionChampionsLabelDict[i].bind("<MouseWheel>", selectChampionScrollWheel)
            selectChampionChampionsImageDict[i].bind("<MouseWheel>", selectChampionScrollWheel)
            selectChampionChampionsLabelDict[i].bind("<Enter>", selectChampionHighlightLabel)
            selectChampionChampionsImageDict[i].bind("<Enter>", selectChampionHighlightImage)
            selectChampionChampionsLabelDict[i].bind("<Leave>", selectChampionUnHighlightLabel)
            selectChampionChampionsImageDict[i].bind("<Leave>", selectChampionUnHighlightImage)

    #height of scrolling area
    if len(selectChampionChampionsDict) > 4:
        selectChampionCanvas.itemconfig(1, height = int(59 * len(selectChampionChampionsDict)))
    else:
        selectChampionCanvas.yview_moveto(0.0)
        selectChampionCanvas.itemconfig(1, height = int(59 * 5))

#other event handlers
selectChampionSearchBoxPressedShared("") #to show all champions

def selectChampionSearchBoxPressed(key): #event handler for key press
    selectChampionSearchBoxPressedShared(key.char)

def selectChampionSearchBoxPressedBS(key): #event handler for backspace
    selectChampionSearchBoxPressedShared(-1)

def selectChampionClickAway():
    selectChampionSearchBox.config(insertontime = 0)
    selectChampionSearchBoxBGHighlight.place_forget()
    if selectChampionSearchBox.get() == "":
        selectChampionInputPrompt.place(relx = 428/1280, rely = 280/720)
        selectChampionEnter.place(relx = 825/1280, rely = 288/720)

def selectChampionEntryClick():
    selectChampionEnter.place_forget()
    selectChampionInputPrompt.place_forget()
    selectChampionSearchBoxBGHighlight.place(relx = 417/1280, rely = 269/720)
    selectChampionSearchBox.config(insertontime = 450)

def selectChampionSearchBoxEnter(event): #select input box
    selectChampionEntryClick()

def selectChampionSearchBoxClick(event):
    selectChampionEntryClick()
    pyautogui.click()

def selectChampionFrameClick(event):
    selectChampionClickAway()

#windows and config
selectChampionCanvas.create_window((0, 0), window = selectChampionDropdownFrameInner, anchor = "nw", width = intScreenX, height = int(59 * len(selectChampionChampionsDict))) #a window of frame inside the canvas used to store any widgets
selectChampionCanvas.configure(yscrollcommand = selectChampionScrollbar.set) #enable scrolling?
selectChampionScrollbar.config(command = selectChampionCanvas.yview)

#binds
#selectChampionSearchBoxBG.bind("<ButtonRelease-1>", selectChampionSearchBoxClick)
selectChampionSearchBox.bind("<ButtonRelease-1>", selectChampionSearchBoxEnter)
selectChampionInputPrompt.bind("<ButtonRelease-1>", selectChampionSearchBoxClick)
selectChampionEnter.bind("<ButtonRelease-1>", selectChampionSearchBoxClick)
selectChampionSearchBox.bind("<Key>", selectChampionSearchBoxPressed)
selectChampionSearchBox.bind("<BackSpace>", selectChampionSearchBoxPressedBS)
selectChampionFrame.bind("<ButtonRelease-1>", selectChampionFrameClick)
selectChampionCanvas.bind("<MouseWheel>", selectChampionScrollWheel)
selectChampionDropdownFrameInner.bind("<Configure>", scrollingChampions)
selectChampionDropdownFrameInner.bind("<MouseWheel>", selectChampionScrollWheel) #scrolling with scrollwheel bind


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#add things tab-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#add things frame
addFrame = Frame(mainFrame, bg = colour87Black, width = intScreenX, height = intScreenY)

def showAdd():
    addFrame.pack(fill = BOTH)

#add things widgets creation
addBackgroundLeftLabel = Label(addFrame, bg = colour87Black, image = addNewChampionLevelIMG, bd = 0)
addBackgroundCenterLabel = Label(addFrame, bg = colour87Black, image = addNewMasteryIMG, bd = 0)
addBackgroundRightLabel = Label(addFrame, bg = colour87Black, image = addNewRankedIMG, bd = 0)

#add things clicked event handlers
def addClick(event):
    hideALL() #hide everything
    showAdd() #show the add new tab
    global selectedTab 
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")
    selectedTab = "Add New"
    #show the right image for each tab
    headerMastery.config(image = headerMasteryImageSelector())
    headerRanked.config(image = headerRankedImageSelector())
    headerAddNew.config(image = headerAddNewImageSelector())

def masteryClickNE(): #non-event mastery Click
    hideALL() #hide everything
    showMastery() #show the mastery tab
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")
    global selectedTab
    selectedTab = "Mastery"
    #show the right image for each tab
    headerMastery.config(image = headerMasteryImageSelector())
    headerRanked.config(image = headerRankedImageSelector())
    headerAddNew.config(image = headerAddNewImageSelector())

def masteryClick(event):
    hideALL() #hide everything
    showMastery() #show the mastery tab
    global selectedTab
    selectChampionUnselectedChampion.config(image = selectChampionUnselectedImage)
    selectChampionSelectedChampionText.config(text = "")
    selectedTab = "Mastery"
    #show the right image for each tab
    headerMastery.config(image = headerMasteryImageSelector())
    headerRanked.config(image = headerRankedImageSelector())
    headerAddNew.config(image = headerAddNewImageSelector())

#add things config

#add things widget place
addBackgroundLeftLabel.place(relx = 0, rely = 60/720)
addBackgroundCenterLabel.place(relx = 427/1280, rely = 60/720)
addBackgroundRightLabel.place(relx = 854/1280, rely = 60/720)

#add things highlight & unhighlight events handlers
def addLevelHighlightFunction(event):
    addBackgroundLeftLabel.config(image = addNewChampionLevelIMGHighlight, cursor = "hand2") #BG

def addLevelUnHighlightFunction(event):
    addBackgroundLeftLabel.config(image = addNewChampionLevelIMG)

def addMasteryHighlightFunction(event):
    addBackgroundCenterLabel.config(image = addNewMasteryIMGHighlight, cursor = "hand2") #BG

def addMasteryUnHighlightFunction(event):
    addBackgroundCenterLabel.config(image = addNewMasteryIMG)

def addRankedHighlightFunction(event):
    addBackgroundRightLabel.config(image = addNewRankedIMGHighlight, cursor = "hand2") #BG

def addRankedUnHighlightFunction(event):
    addBackgroundRightLabel.config(image = addNewRankedIMG)

#add things binds
addBackgroundLeftLabel.bind("<Enter>", addLevelHighlightFunction)
addBackgroundCenterLabel.bind("<Enter>", addMasteryHighlightFunction)
addBackgroundRightLabel.bind("<Enter>", addRankedHighlightFunction)

addBackgroundLeftLabel.bind("<Leave>", addLevelUnHighlightFunction)
addBackgroundCenterLabel.bind("<Leave>", addMasteryUnHighlightFunction)
addBackgroundRightLabel.bind("<Leave>", addRankedUnHighlightFunction)

addBackgroundLeftLabel.bind("<ButtonRelease-1>", showSelectChampionLevel)
addBackgroundCenterLabel.bind("<ButtonRelease-1>", showSelectChampionMastery)
addBackgroundRightLabel.bind("<ButtonRelease-1>", showSelectChampionRanked)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#global header------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
globalHeaderFrame = Frame(root, width = intScreenX, height = 60) #frame above everything else for the tabs above
globalHeaderFrame.place(x = 0, y = 0)
selectedTab = "Mastery" #a string to know which tab the user is on
tabStartingIndentation = 111/1280 #an integer that can be changed

#check indentation for the season number on top left based on number of digits. Supports up to 2 digits
def seasonNumberIndentation():
    if int(defaultSeasonNumber) < 10:
        return 0.03
    else:
        return 0.022

#event handlers for the tabs when leaving highlight
def headerMasteryImageSelectorLeaveEvent(event):
    if selectedTab == "Mastery":
        headerMastery.config(image = headerMasterySelectedImage)
    else:
        headerMastery.config(image = headerMasteryImage)

def headerRankedImageSelectorLeaveEvent(event):
    if selectedTab == "Ranked":
        headerRanked.config(image = headerRankedSelectedImage)
    else:
        headerRanked.config(image = headerRankedImage)

def headerAddNewImageSelectorLeaveEvent(event):
    if selectedTab == "Add New":
        headerAddNew.config(image = headerAddNewSelectedImage)
    else:
        headerAddNew.config(image = headerAddNewImage)

#labels
headerLine = Label(globalHeaderFrame, bg = colour87Black, image = headerLineImage, bd = 0)
headerSeasonNumber = Label(globalHeaderFrame, bg = colour87Black, text = "S" + defaultSeasonNumber, fg = colourLeagueText, font = ("BeaufortforLOL-Bold", 20))
headerMastery = Label(globalHeaderFrame, bg = colour87Black, image = headerMasteryImageSelector(), bd = 0, cursor = "hand2")
headerRanked = Label(globalHeaderFrame, bg = colour87Black, image = headerRankedImageSelector(), bd = 0, cursor = "hand2")
headerAddNew = Label(globalHeaderFrame, bg = colour87Black, image = headerAddNewImageSelector(), bd = 0, cursor = "hand2")

#place labels
headerLine.place(x = 0, y = 0)
headerSeasonNumber.place(relx = seasonNumberIndentation(), rely = 0.16)
headerMastery.place(relx = tabStartingIndentation, y = 0)
headerRanked.place(relx = tabStartingIndentation + 0.09375 * 1, y = 0)
headerAddNew.place(relx = tabStartingIndentation + 0.09375 * 2, y = 0)

#event handler to change image when highlighting
def headerMasteryEnterEvent(event):
    headerMastery.config(image = headerMasteryHighlightedImage)

def headerRankedEnterEvent(event):
    headerRanked.config(image = headerRankedHighlightedImage)

def headerAddNewEnterEvent(event):
    headerAddNew.config(image = headerAddNewHighlightedImage)

#binds
headerMastery.bind("<Enter>", headerMasteryEnterEvent)
headerMastery.bind("<Leave>", headerMasteryImageSelectorLeaveEvent)
headerRanked.bind("<Enter>", headerRankedEnterEvent)
headerRanked.bind("<Leave>", headerRankedImageSelectorLeaveEvent)
headerAddNew.bind("<Enter>", headerAddNewEnterEvent)
headerAddNew.bind("<Leave>", headerAddNewImageSelectorLeaveEvent)
headerMastery.bind("<ButtonRelease-1>", masteryClick)
headerAddNew.bind("<ButtonRelease-1>", addClick)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#app version--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
appVersion = Label(root, text="v0.1", bg = colour87Black, fg = colourActuallyWhite, font = ("BeaufortforLOL-Bold", 8), anchor = "e", width = 10)
appVersion.place(relx = 1213/1280, rely = 1/720)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#end of code--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
mainloop()