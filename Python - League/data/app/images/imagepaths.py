from tkinter import PhotoImage
defaultImageLocation = ".\\data\\app\\images\\"

#mastery part
championBorderImage = PhotoImage(file = defaultImageLocation + "mastery tab\\champion_row_border.png")
championBorderImageHighlight = PhotoImage(file = defaultImageLocation + "mastery tab\\champion_row_border_highlight.png")

#add part
addNewChampionLevelIMG = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Champion Level.png")
addNewChampionLevelIMGHighlight = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Champion Level Highlight.png")
addNewMasteryIMG = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Mastery.png")
addNewMasteryIMGHighlight = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Mastery Highlight.png")
addNewRankedIMG = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Ranked.png")
addNewRankedIMGHighlight = PhotoImage(file = defaultImageLocation + "add new tab\\Add New Ranked Highlight.png")

#select champion part
selectChampionEnterImage = PhotoImage(file = defaultImageLocation + "add new tab\\select champion\\Arrow.png")
selectChampionUnselectedImage = PhotoImage(file = defaultImageLocation + "add new tab\\select champion\\empty champion.png")
selectChampionSelectedLane = PhotoImage(file = defaultImageLocation + "add new tab\\select champion\\Selected Lane.png")
selectChampionTextImage = PhotoImage(file = defaultImageLocation + "add new tab\\select champion\\Choose your champion text.png")

#select mastery part
selectMasteryConfirmSelectionImageBlocked = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Confirm Selection Blocked.png")
selectMasteryConfirmSelectionImage = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Confirm Selection.png")
selectMasteryConfirmSelectionImageHighlight = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Confirm Selection Highlight.png")
selectMasteryCircleImage = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Circle.png")
selectMasteryCircleImageHighlight = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Circle Selected.png")
selectMasteryCentreImage = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Mastery Centre.png")
selectMasteryFinishCentreImage = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Finish Centre.png")
selectMasteryFinishAgainImage = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Finish Add Again.png")
selectMasteryConnectorRingImage = {}
selectMasteryConnectorCentreImage = {}
selectMasteryProgress = {}
for j in range(8):
    selectMasteryConnectorCentreImage[j] = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Connector Centre " + str(j) + ".png")
    if j < 6:
        selectMasteryConnectorRingImage[j] = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Connector Ring " + str(j) + ".png")
        if j < 3:
            selectMasteryProgress[j] = PhotoImage(file = defaultImageLocation + "add new tab\\mastery\\Mastery Progress " + str(j + 1) + ".png")

#global header part
headerLineImage = PhotoImage(file = defaultImageLocation + "global\\header\\Header Line.png")
headerMasteryImage = PhotoImage(file = defaultImageLocation + "global\\header\\Mastery.png")
headerMasterySelectedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Mastery Selected.png")
headerMasteryHighlightedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Mastery Highlight.png")
headerRankedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Ranked.png")
headerRankedSelectedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Ranked Selected.png")
headerRankedHighlightedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Ranked Highlight.png")
headerAddNewImage = PhotoImage(file = defaultImageLocation + "global\\header\\Add New.png")
headerAddNewSelectedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Add New Selected.png")
headerAddNewHighlightedImage = PhotoImage(file = defaultImageLocation + "global\\header\\Add New Highlight.png")

#lanes
lanesImage = {}
lanesImage[0] = PhotoImage(file = defaultImageLocation + "ranked tab\\lanes\\Top.png")
lanesImage[1] = PhotoImage(file = defaultImageLocation + "ranked tab\\lanes\\Jungle.png")
lanesImage[2] = PhotoImage(file = defaultImageLocation + "ranked tab\\lanes\\Middle.png")
lanesImage[3] = PhotoImage(file = defaultImageLocation + "ranked tab\\lanes\\Bottom.png")
lanesImage[4] = PhotoImage(file = defaultImageLocation + "ranked tab\\lanes\\Support.png")