#imports#
from tkinter import * # used for GUI
import sqlite3 # used for DB's
import os
from os.path import isfile # used to check if DB exists
from PIL import ImageTk,Image # pillow - for image processing
import random # used for generation of random numbers
##

loggedIn = False

pot = 0

allBotHands = [ [], [], [] ] # Lists for everyone's hands: list 0 = player, list 1 = bot 1, list 2 = bot 2, list 3 = bot 3.
playerHand = []
communityHand = []

numOfCards = 51 # 51 and not 52 because indexing starts at 0

dealer = random.randint(0,3) # makes player, bot 1, bot 2, or bot 3 dealer
if dealer == 3: # if dealer is bot 3 then
    whoseTurn = 0 # it is player's turn
else: # if dealer is anyone other than bot 3
    whoseTurn = dealer + 1 # it is bot 1, 2, or 3's turn

currentRound = 1 # game starts at round 1
roundOneExecuted = False # no rounds have been executed because game just started
roundTwoExecuted = False
roundThreeExecuted = False
roundFourExecuted = False
roundFiveExecuted = False
roundSixExecuted = False
roundSevenExecuted = False
roundEightExecuted = False
roundNineExecuted = False
roundTenExecuted = False
roundElevenExecuted = False

showingRaiseMenu = False
showingCombineMenu = False

#code to allow user to move menu starts here#
#taken from google#
lastClickXTimer = 0
lastClickYTimer = 0

def SaveLastClickPosTimer(event):
    global lastClickXTimer, lastClickYTimer
    lastClickXTimer, lastClickYTimer = event.x, event.y

def DraggingTimer(event):
    draggedWidget= str(event.widget) # find what type of widget was draggged/pressed
    if draggedWidget[-9:] == "scrollbar" or draggedWidget[2:8] == "button": # if last 9 chars of pressedWidget are scrollbar or 6 are button then
        pass # dont drag window
    else: # if didnt drag scrollbar, drag window
        x, y = event.x - lastClickXTimer + main.winfo_x(), event.y - lastClickYTimer + main.winfo_y()
        main.geometry("+%s+%s" % (x, y))

#code to allow user to move menu ends here#


#window config#
main = Tk()
main.overrideredirect(False)
main.geometry("200x157")
main.eval('tk::PlaceWindow . center') # centers window upon startup
playerMadeDecision = BooleanVar(value=False) # used to make window wait for user to press button on command panel
##


#pixel used to make text appear on buttons#
pixel = PhotoImage(width=1, height=1)
##


#bind mouse button to move program on screen#
main.bind('<Button-1>', SaveLastClickPosTimer)
main.bind('<B1-Motion>', DraggingTimer)
##


# Procedure to print every player's hand and community cards starts here #

def PrintAllHands():
    print()
    print(f"\nCommunity hand {communityHand}\n")
    for x in range(3):
        print(f"Bot {x+1} {allBotHands[x]}")
    print(f"\nPlayer {playerHand}")
    print(f"\nNumber of cards left in deck: {numOfCards}")

# Procedure to print every player's hand and community cards ends here #


#procedure to exit program#
def Exit():
    main.destroy()
##


#menu to menu subroutines start here#

def ClearWindowOrFrame(windowOrFrame):
    for widget in windowOrFrame.winfo_children(): # retrieve every widget from window/frame one by one.
        widget.destroy() # destroy this widget

def MainMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    #decide which menu to show#
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowGameMenu()
    elif n == 2:
        SureYN()
    ##
def AccountMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()
    elif n == 1:
        MakeWindowRegisterMenu()
    elif n == 2:
        MakeWindowLogInMenu()
    elif n == 3:
        MakeWindowDelAccMenu()

def RegisterMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowMainMenu()

def LogInMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowMainMenu()

def AreYouSureMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()

def DelAccountMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()

def GameMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()
    elif n == 1:
        MakeWindowHelpMenu()
    elif n == 2:
        MakeWindowGame()
    elif n == 3:
        MakeWindowAccountStats()

def HelpMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowGameMenu()

#menu to menu subroutines end here#


#are-you-sure window code starts here#

def SureYN():

    #window config#
    main.geometry("200x70")
    ##

    #labels#
    #Tx = Text#
    TxAreYouSure = Label(main, text="ARE YOU SURE?", font=("Rockwell", 18))
    TxAreYouSure.pack()
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtYes = Button(main, text="YES",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=82,
                    borderwidth=0, bg="light grey",
                    command=Exit)
    BtYes.place(x=8, y=33)

    BtNo = Button(main, text="NO",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=82,
                    borderwidth=0, bg="light grey",
                    command=lambda:AreYouSureMenuToAnotherMenu(0))
    BtNo.place(x=105, y=33)
    ##

#are-you-sure window code ends


#help window code starts here#

def MakeWindowHelpMenu():

    #window config#
    main.geometry("460x520")
    ##

    #scrollbar code#
    #Fr = Frame, Ca = Canvas, Sb = Scrollbar#
    FrHelp = Frame(main, width=430, height=450)
    FrHelp.place(x=10, y=10)

    CaHelp = Canvas(FrHelp, width=420, height=450)
    SbHelp = Scrollbar(FrHelp, orient="vertical", command=CaHelp.yview)
   
    FrScrollableHelpText = Frame(CaHelp)
    FrScrollableHelpText.bind("<Configure>", lambda e: CaHelp.configure(scrollregion=CaHelp.bbox("all")))
   
    CaHelp.create_window((0, 0), window=FrScrollableHelpText, anchor="nw")
    CaHelp.configure(yscrollcommand=SbHelp.set)
   
    CaHelp.pack(side=LEFT, fill=BOTH, expand=True)
    SbHelp.pack(side=RIGHT, fill="y")
    ##

    with open("HelpText.txt") as file:
        helpText = file.read()

    Label(FrScrollableHelpText, text=helpText, font=("Rockwell", 10), justify="left").pack()
    ##

    #buttons#
    #Bt = Button#
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=30, width=430,
                    borderwidth=0, bg="light grey",
                    command=lambda:HelpMenuToAnotherMenu(0))
    BtBack.place(x=13, y=475)
    ##

#help window code ends here#


#make list of cards in png format starts here#

def CreateListOfCards():
    with open("ListOfCards.txt") as file:
        return file.read().splitlines()

#make list of cards in png format ends here#


# Player coin management starts here #

def GetPlayerCoins():
    statsDbName = (f"Stats({accountUsername}).db")
    con = sqlite3.connect(statsDbName)
    cursor = con.cursor()

    cursor.execute(f"SELECT currentMoney FROM tblStats_{accountUsername}")
    for row in cursor:
        playerCoins = row[0]

    return playerCoins

def DeductCoinsFromPlayer(numberOfCoins, TxPlayerCoins):

    playerCoins = GetPlayerCoins()

    playerCoins -= numberOfCoins # deduct coins (blind)
    TxPlayerCoins.config(text=f"{accountUsername}'s coins: {playerCoins}") # update player coins widget

    # update current coins in stats database
    statsDbName = (f"Stats({accountUsername}).db") # defining name of this account's stats database file
    con = sqlite3.connect(statsDbName) # making connection to database
    cursor = con.cursor() # creating a cursor for this connection
    
    cursor.execute(f"UPDATE tblStats_{accountUsername} SET currentMoney = {playerCoins}")
    con.commit()

# Player coin management ends here #


# Generation of player and bot cards starts here #

def UpdatePlayerCardButtonsWithList(cardButtons):

    # make all cards have no image # 
    for card in range(len(cardButtons)):
        cardButtons[card].image = ""
    ##

    #make image for hole card#
    for card in range(len(playerHand)): # go through every card in player hand and make image for the card
        cardImageFile = Image.open(f"Playing Cards/{playerHand[card]}")
        resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        cardButtons[card].image = actualCardImage
        cardButtons[card].config(image=actualCardImage)
    ##
def PlacePlayerCardImage(actualCardImage, cardButtons):
    #cardButtons[0] is BtCardOne, ...[1] is BtCardTwo, and so on...

    if len(playerHand) == 1: # if player already has 1 card then
        cardButtons[0].image = actualCardImage # for garbage collection
        cardButtons[0].config(image=actualCardImage) # place the first card onto card screen
    elif len(playerHand) == 2: # if player already has 2 cards then
        cardButtons[1].image = actualCardImage
        cardButtons[1].config(image=actualCardImage) # place the second card onto card screen
    elif len(playerHand) == 3: # if player already has 3 cards then
        cardButtons[2].image = actualCardImage
        cardButtons[2].config(image=actualCardImage) # place the third card onto card screen
    elif len(playerHand) == 4: # if player already has 4 cards then
        cardButtons[3].image = actualCardImage
        cardButtons[3].config(image=actualCardImage) # place the fourth card onto card screen
    elif len(playerHand) == 5: # if player already has 5 cards then
        cardButtons[4].image = actualCardImage
        cardButtons[4].config(image=actualCardImage) # place the fifth card onto card screen

def GeneratePlayerCard(cardButtons):
    global numOfCards

    #get random card#
    randomCardNum = random.randint(0, numOfCards)
    cardImagePNGtext = cardsList[randomCardNum]
    cardsList.pop(randomCardNum)
    numOfCards -= 1
    ##

    #make image for hole card#
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    ##

    playerHand.append(cardImagePNGtext) # add card to player's hand
    PlacePlayerCardImage(actualCardImage, cardButtons)

def GenerateCardForAllBots():
    global numOfCards, allBotHands

    #give every bot a card#
    for bot in range(3):
        if (currentRound == 2) or (currentRound > 2 and len(allBotHands[bot]) > 0): # if its round 2 or bot hasn't folded then give card
            randomCardNum = random.randint(0, numOfCards)
            cardImagePNGtext = cardsList[randomCardNum]
            cardsList.pop(randomCardNum)
            numOfCards -= 1
            allBotHands[bot].append(cardImagePNGtext) # add card to bot hand

def GenerateCommunityCard(communityCardList):
    global numOfCards, communityHand

    #get random card#
    randomCardNum = random.randint(0, numOfCards)
    cardImagePNGtext = cardsList[randomCardNum]
    cardsList.pop(randomCardNum)
    numOfCards -= 1
    ##

    #make image for hole card#
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((55, 83), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    ##

    communityHand.append(cardImagePNGtext) # add card to community's hand

    if len(communityHand) == 1:
        communityCardList[0].image = actualCardImage
        communityCardList[0].config(image=actualCardImage)
    elif len(communityHand) == 2:
        communityCardList[1].image = actualCardImage
        communityCardList[1].config(image=actualCardImage)
    elif len(communityHand) == 3:
        communityCardList[2].image = actualCardImage
        communityCardList[2].config(image=actualCardImage)

# Generation of player and bot cards ends here #




# Calculation of hand strengths starts here #

def CheckForPairOrKinds(whatToCheckFor, botHand, pair, twoPair, threeOfAKind, fourOfAKind):

    botHandValues = MakeHandIntoListOfValues(botHand)
    print(f"bot hand values {botHandValues}")
    numberOfPairs = 0
    valuesOfPairs = []

    for value in range(14, 1, -1): # start at 15, go down to 0, going down by 1 every time, 15, 14, 13, ...
        if botHandValues.count(value) == whatToCheckFor: # if there are _ of any value then
            if whatToCheckFor == 2: # if checking for pair
                pair = True # set pair to true
                valueOfPair = value # set value of pair
                numberOfPairs += 1
                valuesOfPairs.append(value)
                if numberOfPairs == 2:
                    twoPair = True
                    valueOfTwoPair = max(valuesOfPairs)
            elif whatToCheckFor == 3:
                threeOfAKind = True
                valueOfThreeOfAKind = value
            elif whatToCheckFor == 4:
                fourOfAKind = True
                valueOfFourOfAKind = value
                #
    
    if whatToCheckFor == 2 and pair and not twoPair: # if checking for pair and have pair, then
        return pair, valueOfPair # return True and value of pair
    elif whatToCheckFor == 2 and twoPair: # if checking for two pair and have two pair
        return twoPair, valueOfTwoPair # return True and value of two pair
    elif whatToCheckFor == 3 and threeOfAKind: # if checking for three of a kind and have it, then
        return threeOfAKind, valueOfThreeOfAKind # return True and value of three of a kind
    elif whatToCheckFor == 4 and fourOfAKind: # if checking for four of a kind and have it, then
        return fourOfAKind, valueOfFourOfAKind # return True and value of four of a kind
    else:
        return False, 0

def IsStraight(hand): # check if bot has straight

    handValues = MakeHandIntoListOfValues(hand) # make a list like [1, 12, 3, 6, 8] instead of ["1_of...", "12_of...", ...]
    handValuesSet = list(set(handValues))
    handValuesSet.sort() # sort the list smallest to biggest
    sectionOfHandValues = []
    limit = 5
    if len(handValuesSet) >= limit:
        for x in range(limit - 1):
            sectionOfHandValues = handValuesSet[-5-x:len(handValuesSet)-x] # check adjacent 5 cards throughout whole list for straight
            for i in range(limit - 1):
                if sectionOfHandValues[i] != sectionOfHandValues[i+1] - 1: # if not straight
                    return False
            return True # if straight return true

def CheckForFlush(hand):
    botHandString = '\t'.join(hand) # used to count number of occurrances of pattern in string (like diamonds or hearts...)

    numberOfDiamonds = botHandString.count("diamonds")
    numberOfHearts = botHandString.count("hearts")
    numberOfSpades = botHandString.count("spades")
    numberOfClubs = botHandString.count("clubs")

    if numberOfDiamonds >= 5:
        return True
    elif numberOfHearts >= 5:
        return True
    elif numberOfSpades >= 5:
        return True
    elif numberOfClubs >= 5:
        return True
    else:
        return False

def MakeHandIntoListOfValues(hand):
    handValues = [] # i.e 1, 2, 3, 4, 5...

    for card in range(len(hand)):
        valueOfCard = hand[card][0:2] # get value of card e.g. "1_", or "12", etc.
        if valueOfCard[1] == "_": # if value is one digit ("1_", or "2_", etc.)
            valueOfCard = valueOfCard[0] # make value one digit ("1", or "2", etc.)
        handValues.append(int(valueOfCard)) # add value of card to list of values

    return handValues  

def CalculateHandStrength(hand):

    royalFlush, straightFlush, fourOfAKind, fullHouse, flush, straight, threeOfAKind, twoPair, pair = False, False, False, False, False, False, False, False, False

    botHandString = '\t'.join(hand) # used to count number of occurrances of pattern in string (like diamonds or hearts...)

    # check for straight
    if IsStraight(hand):
        straight = True
    ##
           
    # check for flush #
    try:
        flush = CheckForFlush(hand) # if has flush, return suit of flush and True
    except: # if not flush then 
        flush = False
    ##

    # check for straight flush #
    if flush and straight:
        # check for royal flush #
        if "10" in botHandString and "11" in botHandString and "12" in botHandString and "13" in botHandString and "14" in botHandString:
            return 10
        ##
        return 9
    ##

    if not straightFlush:

        # check for four of a kind #
        fourOfAKind, valueOfFourOfAKind = CheckForPairOrKinds(4, hand, pair, twoPair, threeOfAKind, fourOfAKind)
        ##

        if fourOfAKind:
            return 8, valueOfFourOfAKind

    if not fourOfAKind:

        # check for pair #
        pair, valueOfPair = CheckForPairOrKinds(2, hand, pair, twoPair, threeOfAKind, fourOfAKind) # values returned are 0 if there is no pair or two pair
        ##

        # check for two pair #
        twoPair, valueOfTwoPair = CheckForPairOrKinds(2, hand, pair, twoPair, threeOfAKind, fourOfAKind) # values returned are 0 if there is no pair or two pair
        ##

        # check for three of a kind #
        threeOfAKind, valueOfThreeOfAKind = CheckForPairOrKinds(3, hand, pair, twoPair, threeOfAKind, fourOfAKind)
        ##

        # check for full house #
        if pair and threeOfAKind:
            return 7
        ##   

        if flush:
            return 6

        if straight:
            return 5

        if threeOfAKind:
            return 4, valueOfThreeOfAKind

        if twoPair:
            return 3, valueOfTwoPair

        if pair:
            return 2, valueOfPair

    # check for high #
    if not royalFlush and not straightFlush and not straight and not flush and not fourOfAKind and not fullHouse and not threeOfAKind and not twoPair and not pair:
        return 1
    ##

# Calculation of hand strengths ends here #


# Player betting options start here #

def Call(TxPlayerCoins, TxPot, FrScrollableText, button):
    playerMadeDecision.set(True)

    DeductCoinsFromPlayer(lastBet, TxPlayerCoins)
    UpdatePot(lastBet, TxPot)
    UpdateFeedback(lastBet, FrScrollableText, False, False)
    IncreaseWhoseTurn()

    button["state"] = "disabled"

def Check(FrScrollableText):
    playerMadeDecision.set(True)
    BtCheck["state"] = "disabled"
    UpdateFeedback(0, FrScrollableText, False, False)
    IncreaseWhoseTurn() # carry out check process

def CommitRaise(EnRaise, TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension):
    global lastBet

    raiseValue = EnRaise.get()
    if raiseValue == "": # to prevent error when user enters nothing for raise
        raiseValue = 0
    raiseValue = int(raiseValue) # convert raisevalue to int for subroutine at end of this subroutine and if statement
    print(f"player attempted to raise by: {raiseValue}")

    playerCoins = GetPlayerCoins()
    if playerCoins >= raiseValue and raiseValue > lastBet:
        lastBet = raiseValue
        DeductCoinsFromPlayer(raiseValue, TxPlayerCoins)
        UpdatePot(raiseValue, TxPot),
        UpdateFeedback(raiseValue, FrScrollableText, False, False)
        ClearWindowOrFrame(FrCommandPanelExtension)
        IncreaseWhoseTurn()
        playerMadeDecision.set(True)

def ShowRaiseMenu(TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension):

    BtCloseRaiseMenu = Button(FrCommandPanelExtension, text="CANCEL RAISE", font=("Rockwell", 10),
                        compound="c", image=pixel, height=50, width=108, borderwidth=0, 
                        command=lambda:ClearWindowOrFrame(FrCommandPanelExtension))
    BtCloseRaiseMenu.place(x=5,y=130)

    TxRaiseBy = Label(FrCommandPanelExtension, text="RAISE BET BY", font=("Rockwell", 12), background="dark grey")
    TxRaiseBy.place(x=5,y=5)

    EnRaise = Entry(FrCommandPanelExtension, width=18)
    EnRaise.place(x=5,y=30)

    BtCommitRaise = Button(FrCommandPanelExtension, text="COMMIT RAISE", font=("Rockwell", 10),
                        compound="c", image=pixel, height=50, width=108, borderwidth=0, 
                        command=lambda:CommitRaise(EnRaise, TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension))
    BtCommitRaise.place(x=5,y=60)

# Player betting options end here #


# Bot betting code starts here #

def ReturnPercentageInteger():
    integer = random.randint(1,100)
    return integer

def CalculateNextBotBet():

    previousBotChecked = False
    if previousRoundLastBet == lastBet: # if nobody has made a bet this round,
        previousBotChecked = True

    if len(allBotHands[whoseTurn - 1]) == 0:
        return -2 # this stops the bot from betting if they have already folded

    botHandStrength = botHandsStrengths[whoseTurn - 1] # if whoseTurn is 1, use bot 1's hand
    if type(botHandStrength) == tuple: 
        # bothandstrength can be a tuple if pair, 2pair, 4ofkind, 3ofkind 
        # so take first number in tuple to find strength i.e (2, 6), then its pair.
        botHandStrength = botHandStrength[0] 

    if botHandStrength == 1: # only high card
        chance = ReturnPercentageInteger()
        if chance >= 25: # 75% chance that they call
            print(f"bot {whoseTurn} with strength {botHandStrength} CALLED with chance {chance}") # debug purposes
            return 1.0 # 1.0x means call
        else: # 25% chance they will check/fold
            if previousBotChecked: # try checking
                print(f"bot {whoseTurn} with strength {botHandStrength} CHECKED with chance {chance}") # debug purposes
                return 0 # 0 means check
            else:
                print(f"bot {whoseTurn} with strength {botHandStrength} FOLDED with chance {chance}") # debug purposes
                return -1 # make bot one fold. try to add check before fold. if cant check then fold.
        
    elif botHandStrength == 2:
        chance = ReturnPercentageInteger()
        if chance >= 30: # 70% chance that they call
            print(f"bot {whoseTurn} with strength {botHandStrength} CALLED with chance {chance}") # debug purposes
            return 1.0 
        else: # 30% chance they raise by 1.2x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 1.2x with chance {chance}") # debug purposes
            return 1.2 # 1.2 means raise by 1.2x

    elif botHandStrength == 3:
        chance = ReturnPercentageInteger()
        if chance >= 35: # 65% chance that they raise by 1.5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 1.5x with chance {chance}") # debug purposes
            return 1.5
        else: # 35% chance they raise by 2x
            print(f"bot {whoseTurn}with strength {botHandStrength} RAISED by 2.0x with chance {chance}") # debug purposes
            return 2.0 

    elif botHandStrength == 4:
        chance = ReturnPercentageInteger()
        if chance >= 30: # 70% chance that they raise by 2.5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.5x with chance {chance}") # debug purposes
            return 2.5
        else: # 30% chance they will raise by 2x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.0x with chance {chance}") # debug purposes
            return 2.0 
    
    elif botHandStrength == 5:
        chance = ReturnPercentageInteger()
        if chance >= 25: # 75% chance that they raise by 3x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.0x with chance {chance}") # debug purposes
            return 3.0 
        else: # 25% chance they will raise by 2.5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.5x with chance {chance}") # debug purposes
            return 2.5 
    
    elif botHandStrength == 6:
        chance = ReturnPercentageInteger()
        if chance >= 20: # 80% chance that they raise by 3x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.5x with chance {chance}") # debug purposes
            return 3.5 
        else: # 25% chance they will raise by 3x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.0x with chance {chance}") # debug purposes
            return 3.0 

    elif botHandStrength == 7:
        chance = ReturnPercentageInteger()
        if chance >= 15: # 85% chance that they raise by 4x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 4.0x with chance {chance}") # debug purposes
            return 4.0
        else: # 15% chance they will raise by 3.5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.5x with chance {chance}") # debug purposes
            return 3.5 
    
    elif botHandStrength == 8:
        chance = ReturnPercentageInteger()
        if chance >= 10: # 90% chance that they raise by 4.5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 4.5x with chance {chance}") # debug purposes
            return 4.5
        else: # 15% chance they will raise by 4x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 4.0x with chance {chance}") # debug purposes
            return 4.0 
    
    elif botHandStrength == 9:
        chance = ReturnPercentageInteger()
        if chance >= 5: # 95% chance that they raise by 5x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 5.0x with chance {chance}") # debug purposes
            return 5.0
        else: # 5% chance they will raise by 4x
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 4.0x with chance {chance}") # debug purposes
            return 4.0 

def MakeBotBet(TxPot, FrScrollableText):
    global lastBet

    if currentRound == 1:
        UpdatePot(10, TxPot)
        UpdateFeedback(10, FrScrollableText, False, False)
        IncreaseWhoseTurn() # if it was just bot 1's turn, its bot 2's turn, etc.
        lastBet = 10
    else:
        UpdateBotHandStrengthsList() # make bots reavaluate their hand
        nextBetMultiplier = CalculateNextBotBet() # make bots calculate their next bet
        if nextBetMultiplier == 0:
            print(f"bot: {whoseTurn - 1} checked")
        if not len(allBotHands[whoseTurn - 1]) == 0: # if current bot has cards in his hand
            if nextBetMultiplier == 1.0: # 1.0 means call
                UpdatePot(lastBet, TxPot)
                UpdateFeedback(lastBet, FrScrollableText, False, False)
            elif nextBetMultiplier == -1: # -1 means fold
                allBotHands[whoseTurn - 1].clear() # clear bot's hand
                UpdateFeedback(lastBet, FrScrollableText, True, False)
            elif nextBetMultiplier == -2:
                print(f"no bet made by bot {whoseTurn - 1}, nextbetmultiplier = -2") # do nothing if bot previously folded
            elif nextBetMultiplier == 0: # 0 means check
                UpdateFeedback(0, FrScrollableText, False, False)
            else: # anything other than 1.0 and -1 is raise
                UpdatePot(round(lastBet * nextBetMultiplier, 0), TxPot)
                UpdateFeedback(round(lastBet * nextBetMultiplier, 0), FrScrollableText, False, False)
                lastBet = round(lastBet * nextBetMultiplier, 0)
        IncreaseWhoseTurn()

# Bot betting code ends here #


# Combination of player's hand starts here #

def GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard):

    if "spades" in firstChosenCard:
        firstChosenCardSuit = "spades"
    elif "clubs" in firstChosenCard:
        firstChosenCardSuit = "clubs"
    elif "hearts" in firstChosenCard:
        firstChosenCardSuit = "hearts"
    elif "diamonds" in firstChosenCard:
        firstChosenCardSuit = "diamonds"

    if "spades" in secondChosenCard:
        secondChosenCardSuit = "spades"
    elif "clubs" in secondChosenCard:
        secondChosenCardSuit = "clubs"
    elif "hearts" in secondChosenCard:
        secondChosenCardSuit = "hearts"
    elif "diamonds" in secondChosenCard:
        secondChosenCardSuit = "diamonds"

    return firstChosenCardSuit, secondChosenCardSuit

def CommitCombine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global showingCombineMenu, roundSixExecuted

    playerHand.remove(firstChosenCard) # remove combo card 1
    playerHand.remove(secondChosenCard) # remove combo card 2
    playerHand.append(cardImagePNGtext) # add combined card

    cardButtons[cardTwo].image = "" # remove image of card

    #create combined card image#
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    ##

    #change image of combined card in card screen#
    cardButtons[cardOne].image = actualCardImage
    cardButtons[cardOne].config(image=actualCardImage)
    ##

    UpdatePlayerCardButtonsWithList(cardButtons)

    ClearWindowOrFrame(FrCommandPanelExtension)
    showingCombineMenu = False

    print("PLAYER combined cards")
    IncreaseWhoseTurn()
    if currentRound == 6:
        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                        TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif currentRound == 9:
        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                        TxPlayerCoins, TxPot, cardButtons, communityCardList)

def SelectTwoCardsToCombine(EnCardOne, EnCardTwo, EnOperation, TxResultCard, BtCommitCombine):
    global cardImagePNGtext, cardOne, cardTwo, firstChosenCard, secondChosenCard

    cardOne = EnCardOne.get()
    cardOne = int(cardOne) - 1
    cardTwo = EnCardTwo.get()
    cardTwo = int(cardTwo) - 1
    operation = EnOperation.get()

    firstChosenCard = playerHand[cardOne]
    secondChosenCard = playerHand[cardTwo]

    firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

    valuesInPlayerHand = MakeHandIntoListOfValues(playerHand)
    biggerCardOfTheTwo = max(valuesInPlayerHand[cardOne], valuesInPlayerHand[cardTwo])
    smallerCardOfTheTwo = min(valuesInPlayerHand[cardOne], valuesInPlayerHand[cardTwo])

    if operation == "+" and valuesInPlayerHand[cardOne] + valuesInPlayerHand[cardTwo] < 15:
        number = valuesInPlayerHand[cardOne] + valuesInPlayerHand[cardTwo]

    elif operation == "-" and biggerCardOfTheTwo - smallerCardOfTheTwo > 0:
        number = biggerCardOfTheTwo - smallerCardOfTheTwo

    elif operation == "*" and valuesInPlayerHand[cardOne] * valuesInPlayerHand[cardTwo] < 15:
        number = valuesInPlayerHand[cardOne] * valuesInPlayerHand[cardTwo]

    elif operation == "/" and str((biggerCardOfTheTwo / smallerCardOfTheTwo))[-2:] == ".0":
        number = round(biggerCardOfTheTwo / smallerCardOfTheTwo)

    try: # if all inputs were valid do the following
        if valuesInPlayerHand[cardOne] >= valuesInPlayerHand[cardTwo]: # if card one is larger than card two
            #create image file name using variables above#
            cardImagePNGtext = f"{number}_of_{firstChosenCardSuit}.png" # use card one's suit
            ##
        elif valuesInPlayerHand[cardOne] <= valuesInPlayerHand[cardTwo]: # if card two is larger than card one
            cardImagePNGtext = f"{number}_of_{secondChosenCardSuit}.png" # use card two's suit

        #create result card image#
        cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
        resizedCardImageFile = cardImageFile.resize((45, 70), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        ##

        #configure the result card#
        TxResultCard.image = actualCardImage
        TxResultCard.config(image=actualCardImage)
        ##
        BtCommitCombine["state"] = "normal"
    except: # if not all inputs are valid, print error
        print("error occurred creating image for result card")
        BtCommitCombine["state"] = "disabled"

def ShowCombineMenu(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                    TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global showingCombineMenu

    if showingCombineMenu:
        ClearWindowOrFrame(FrCommandPanelExtension)
        showingCombineMenu = False
    else:   
        showingCombineMenu = True

        TxResult = Label(FrCommandPanelExtension, text="RESULT", font=("Rockwell", 12), background="dark grey")
        TxResult.place(x=30,y=75)

        TxCardOne = Label(FrCommandPanelExtension, text="CARD 1", font=("Rockwell", 8), background="dark grey")
        TxCardOne.place(x=15,y=5)

        TxCardTwo = Label(FrCommandPanelExtension, text="CARD 2", font=("Rockwell", 8), background="dark grey")
        TxCardTwo.place(x=85,y=5)

        TxOperation = Label(FrCommandPanelExtension, text="MATH OPERATION", font=("Rockwell", 8), background="dark grey")
        TxOperation.place(x=15,y=30)
        
        EnCardOne = Entry(FrCommandPanelExtension, width=2)
        EnCardOne.place(x=0,y=5)
        
        EnCardTwo = Entry(FrCommandPanelExtension, width=2)
        EnCardTwo.place(x=70,y=5)

        EnOperation = Entry(FrCommandPanelExtension, width=2)
        EnOperation.place(x=0,y=30)

        TxResultCard = Label(FrCommandPanelExtension, borderwidth=0)
        TxResultCard.place(x=40,y=100)

        BtCheckCombination = Button(FrCommandPanelExtension, text="CHECK COMBINATION", font=("Rockwell", 9),
                            compound="c", image=pixel, height=15, width=130, borderwidth=0, 
                            command=lambda:SelectTwoCardsToCombine(EnCardOne, EnCardTwo, EnOperation, TxResultCard, BtCommitCombine))
        BtCheckCombination.place(x=0,y=55)

        BtCommitCombine = Button(FrCommandPanelExtension, text="COMBINE", font=("Rockwell", 10),
                            compound="c", image=pixel, height=15, width=115, borderwidth=0, 
                            command=lambda:CommitCombine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, 
                                                        FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList))
        BtCommitCombine.place(x=0,y=175)
        BtCommitCombine["state"] = "disabled" # by default its disabled

# Combination of player's hand ends here #


# Combination of bot hands code starts here #

def TryCombiningIntoFourOfAKind(botHandValues, valueOfPairOrKind):
    
    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]
    print(f"before removing targets trying to combine into 4 of a kind: {botHandValues}\n current bot hand {currentBotHand}")
    target = valueOfPairOrKind # target here is a number that appears three times in bot's hand (including community hand)

    if len(communityHand) == 3:

        if (botHandValues[0] == target and botHandValues[1] == target and botHandValues[2] == target): # if target T T T : _ _ _ _
            botHandValues.pop(0) # remove first community card which is target 1/3
            botHandValues.pop(0) # remove second community card which is target 2/3
            botHandValues.pop(0) # remove third community card which is target 3/3
            situation = 1

        elif (botHandValues[0] == target and botHandValues[1] == target): # if target T T _ : _ _ _ _ 1 T can be anywhere in bot hand
            botHandValues.pop(0) # remove first community card / target
            botHandValues.pop(0) # remove second community card / target
            botHandValues.pop(0) # remove third community card / target
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 3/3
            situation = 2

        elif (botHandValues[1] == target and botHandValues[2] == target): # if target _ T T : _ _ _ _ 1 T can be anywhere in bot hand
            botHandValues.pop(0) # remove first community card / target
            botHandValues.pop(0) # remove second community card / target
            botHandValues.pop(0) # remove third community card / target
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 3/3
            situation = 2

        elif (botHandValues[0] == target and botHandValues[2] == target): # if target T _ T : _ _ _ _ 1 T can be anywhere in bot hand
            botHandValues.pop(0) # remove first community card / target
            botHandValues.pop(0) # remove second community card / target
            botHandValues.pop(0) # remove third community card / target
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 3/3
            situation = 2

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1 or botHandValues.index(target) == 2: 
            # if target 1/3 is in community hand and the target 2/3 and 3/3 are in bot hand
            botHandValues.pop(0) # remove target 1/3 that is community card
            botHandValues.pop(0) # remove comm card 2
            botHandValues.pop(0) # remove community card 3
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the second target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target that isn't community card
            botHandValues.remove(target) # remove target that isn't community card
            situation = 3
        
        elif botHandValues.index(target) > 2: # if none of the 3 targets are community cards then
            botHandValues.pop(0) # remove community card 1
            botHandValues.pop(0) # remove comm card 2
            botHandValues.pop(0) # remove community card 3
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the second target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the third target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 1/3 that isn't community card
            botHandValues.remove(target) # remove target 2/3 that isn't community card
            botHandValues.remove(target) # remove target 3/3 that isn't community card
            situation = 4

    elif len(communityHand) == 2:

        if botHandValues[0] == target and botHandValues[1] == target: # if both targets are in the 2 community cards then
            botHandValues.pop(0) # remove target 1/3 that is community card
            botHandValues.pop(0) # remove target 2/3 that is community card
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 3/3 that isn't community card
            situation = 2

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1: # if target is comm card
            botHandValues.pop(0) # remove target 1/3 that is community card
            botHandValues.pop(0) # remove second community card
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target 2/3 that isn't community card
            botHandValues.remove(target) # remove target 3/3 that isn't community card
            situation = 3

    print(f"situation: {situation}. after removing targets trying to combine into 4 of a kind: {botHandValues}\n current bot hand {currentBotHand}")

    for index in range(len(botHandValues)): # go through every card in bot hand
        firstChosenCard = currentBotHand[index - 1] # used to find suit of card 1
        secondChosenCard = currentBotHand[index] # used to find suit of card 2

        # biggerCardOfTheTwo = max(botHandValues[index - 1], botHandValues[index])
        # smallerCardOfTheTwo = min(botHandValues[index - 1], botHandValues[index])
        print(botHandValues[index - 1], botHandValues[index], index)
        
        if botHandValues[index - 1] + botHandValues[index] == target: # if adding 2 cards makes the target

            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} + {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                print(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")

                currentBotHand.append(resultingCard)  # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png") 
                currentBotHand.append(resultingCard) # add resulting card

                if situation == 2:
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    
                newCardCreated = True
                break

        elif botHandValues[index - 1] * botHandValues[index] == target:
            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} * {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    
                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.append(resultingCard) # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    
                newCardCreated = True
                break

    if not newCardCreated and situation == 2: # if no new card was created thru combo then
        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
        # this is because when looking for target, the target in currentbothand is removed for algorithm to work.
        # so we add it back if target wasnt made 
    elif not newCardCreated and situation == 3:
        currentBotHand.append(targetInCurrentBotHand)
        currentBotHand.append(targetInCurrentBotHand)

    return newCardCreated

def TryCombiningIntoThreeOfAKind(botHandValues, valueOfPairOrKind):
    
    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]
    print(f"before removing target trying to combine into 3 of a kind: {botHandValues}\n current bot hand {currentBotHand}")
    target = valueOfPairOrKind # target here is a number that appears twice in bot's hand (including community hand)

    if len(communityHand) == 3:

        if (botHandValues[0] == target and botHandValues[1] == target): # if target T T _ : _ _ _ _
            botHandValues.pop(0) # remove first community card
            botHandValues.pop(0) # remove second community card
            botHandValues.pop(0) # remove third community card
            situation = 1

        elif (botHandValues[1] == target and botHandValues[2] == target): # if target _ T T : _ _ _ _
            botHandValues.pop(0) # remove first community card
            botHandValues.pop(0) # remove second community card
            botHandValues.pop(0) # remove third community card
            situation = 1

        elif (botHandValues[0] == target and botHandValues[2] == target): # if target T _ T : _ _ _ _
            botHandValues.pop(0) # remove first community card
            botHandValues.pop(0) # remove second community card
            botHandValues.pop(0) # remove third community card
            situation = 1

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1 or botHandValues.index(target) == 2: 
            # if one target out of the two targets is in community hand and the other is in bot hand
            botHandValues.remove(target) # remove target that is community card
            botHandValues.pop(0) # remove comm card 2
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 1] # create variable for the target
            currentBotHand.pop(botHandValues.index(target) - 1) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target that isn't community card
            botHandValues.pop(0) # remove community card 3
            situation = 2

        elif botHandValues.index(target) > 1: # if target isnt community card but is in bot combo hand then
            botHandValues.pop(0) # remove comm card 1
            botHandValues.pop(0) # remove comm card 2
            botHandValues.pop(0) # remove comm card 3
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the second target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target that isnt comm card
            botHandValues.remove(target) # remove the same target again since target is a pair (2 of same card)
            situation = 3

    elif len(communityHand) == 2:

        if botHandValues[0] == target and botHandValues[1] == target: # if both targets are in 2 community cards then
            botHandValues.pop(0) # remove first community card
            botHandValues.pop(0) # remove second community card
            situation = 1

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1: # if target is comm card
            botHandValues.remove(target) # remove target that is community card
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 1] # create variable for the target
            currentBotHand.pop(botHandValues.index(target) - 1) # remove the target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target that isn't community card
            botHandValues.pop(0) # remove other community card
            situation = 2

        elif botHandValues.index(target) > 1: # if target isnt community card but is in bot combo hand then
            botHandValues.pop(0) # remove comm card 1
            botHandValues.pop(0) # remove comm card 2
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] # create variable for the target
            currentBotHand.pop(botHandValues.index(target)) # remove the target card from bot hand (this hand uses .png string)
            currentBotHand.pop(botHandValues.index(target)) # remove the second target card from bot hand (this hand uses .png string)
            botHandValues.remove(target) # remove target that isnt comm card
            botHandValues.remove(target) # remove the same target again since target is a pair (2 of same card)
            situation = 3

    print(f"situation: {situation}. after removing target trying to combine into 3 of a kind: {botHandValues}\n current bot hand {currentBotHand}")

    for index in range(len(botHandValues)): # go through every card in bot hand
        firstChosenCard = currentBotHand[index - 1] # used to find suit of card 1
        secondChosenCard = currentBotHand[index] # used to find suit of card 2

        # biggerCardOfTheTwo = max(botHandValues[index - 1], botHandValues[index])
        # smallerCardOfTheTwo = min(botHandValues[index - 1], botHandValues[index])
        print(botHandValues[index - 1], botHandValues[index], index)
        
        if botHandValues[index - 1] + botHandValues[index] == target: # if adding 2 cards makes the target

            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} + {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                print(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.append(resultingCard) # add resulting card

                if situation == 2:
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

        elif botHandValues[index - 1] * botHandValues[index] == target:
            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} * {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.append(resultingCard) # add resulting card

                if situation == 2: # one target card out of both is in community hand
                    currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                elif situation == 3: # both target cards are in bot combo hand
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

    if not newCardCreated and situation == 2: # if no new card was created thru combo then
        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
        # this is because when looking for target, the target in currentbothand is removed for algorithm to work.
        # so we add it back if target wasnt made 
    elif not newCardCreated and situation == 3:
        currentBotHand.append(targetInCurrentBotHand)
        currentBotHand.append(targetInCurrentBotHand)

    return newCardCreated

def TryCombiningIntoPair(botHandValues):


    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]

    #print(f"Before attempting to combine into pair, bot {whoseTurn}.\n bot hand: {currentBotHand}")
    #print(f"before removing target trying to combine into pair: {botHandValues}\n current bot hand {currentBotHand}.")
    target = max(botHandValues) # find biggest value card in bot's hand

    if botHandValues.index(target) == 0 or botHandValues.index(target) == 1: # if target is comm card
        botHandValues.remove(target) # remove target that is community card
        botHandValues.pop(0) # remove other community card
        if len(communityHand) == 3: # if there are 3 community cards then
            botHandValues.pop(0) # remove third community card
        situation = 1

    elif botHandValues.index(target) > 1: # if target isnt community card
        if len(communityHand) == 3: # if there are 3 community cards then
            botHandValues.pop(0) # remove comm card 1
        targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 2] # create variable for the target
        currentBotHand.pop(botHandValues.index(target) - 2) # remove the target card from bot hand (this hand uses .png string)
        botHandValues.remove(target) # remove target that isnt comm card
        botHandValues.pop(0) # remove comm card 2
        botHandValues.pop(0) # remove comm card 3
        situation = 2

    #print(f"after removing target trying to combine into pair: {botHandValues}\n current bot hand {currentBotHand}.")
    if len(botHandValues) != 1:
        for index in range(len(botHandValues)): # go through every card in bot hand
            firstChosenCard = currentBotHand[index - 1] # used to find suit of card 1
            secondChosenCard = currentBotHand[index] # used to find suit of card 2

            # biggerCardOfTheTwo = max(botHandValues[index - 1], botHandValues[index])
            # smallerCardOfTheTwo = min(botHandValues[index - 1], botHandValues[index])

            #print(f"{botHandValues[index - 1]}, {botHandValues[index]}, {index}")

            if botHandValues[index - 1] + botHandValues[index] == target: # if adding 2 cards makes the target

                firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

                #print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} + {botHandValues[index]} of {secondChosenCardSuit} = {target}")

                if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                    #print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                    resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.append(resultingCard)  # add resulting card

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand

                    newCardCreated = True
                    break

                elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                    #print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                    resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.append(resultingCard) # add resulting card

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                        
                    newCardCreated = True
                    break

            elif botHandValues[index - 1] * botHandValues[index] == target:
                firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

                #print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} * {botHandValues[index]} of {secondChosenCardSuit} = {target}")

                if botHandValues[index - 1] >= botHandValues[index]: # if card one is larger than card two
                    #print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") # use card one's suit
                    resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")

                    currentBotHand.append(resultingCard)  # add resulting card

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                        
                    newCardCreated = True
                    break

                elif botHandValues[index - 1] <= botHandValues[index]: # if card two is larger than card one
                    #print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") # use card two's suit
                    resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")

                    currentBotHand.append(resultingCard) # add resulting card

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
                        
                    newCardCreated = True
                    break

    if not newCardCreated and situation == 2: # if no new card was created thru combo then
        currentBotHand.append(targetInCurrentBotHand) # add back the target card into bot hand
        # this is because when looking for target, the target in currentbothand is removed for algorithm to work.
        # so we add it back if target wasnt made 
    
    #print(f"After attempting to combine into pair, bot {whoseTurn}.\n bot hand: {currentBotHand}")

    return newCardCreated

def DecideWhichCombinationToMake(tempList, FrScrollableText):

    
    botHandStrength = CalculateHandStrength(tempList)
    if type(botHandStrength) == tuple: 
        # bothandstrength can be a tuple if pair, 2pair, 4ofkind, 3ofkind 
        # so take first number in tuple to find strength i.e (2, 6), then its pair.
        valueOfPairOrKind = botHandStrength[1]
        botHandStrength = botHandStrength[0]

    botHandValues = MakeHandIntoListOfValues(tempList)

    #print(f"DecideWhichCombinationToMake, bot {whoseTurn} strength = {botHandStrength}")

    if botHandStrength == 1: # can still add code to make bot combine to make second highest card
        isNewCardCreated = TryCombiningIntoPair(botHandValues)
    elif botHandStrength == 2: # if bot has pair then
        isNewCardCreated = TryCombiningIntoThreeOfAKind(botHandValues, valueOfPairOrKind)
    elif botHandStrength == 4: # if bot has three of a kind
        isNewCardCreated = TryCombiningIntoFourOfAKind(botHandValues, valueOfPairOrKind)

    try:
        UpdateFeedback("tried to combine", FrScrollableText, False, isNewCardCreated)
    except:
        UpdateFeedback("tried to combine", FrScrollableText, False, False)

def MakeBotCombine(FrScrollableText):

    tempList = communityHand.copy() # copy communityHand list, which makes first 2 elements be the community hand

    for card in range(len(allBotHands[whoseTurn - 1])):
        tempList.append(allBotHands[whoseTurn - 1][card]) # add all of the bot's cards into that list

    if len(allBotHands[whoseTurn - 1]) > 0: # if current bot hasn't folded then
        DecideWhichCombinationToMake(tempList, FrScrollableText)

    tempList.clear()

    print(f"bot: {whoseTurn} combination over")
    IncreaseWhoseTurn()

# Combination of bot hands code ends here #


# Showdown round code starts here #

def ShowAllBotAndCommunityCards(FrTableScreen):
    
    TxBotOneCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardOne.place(x=70,y=50)
    TxBotOneCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardTwo.place(x=110,y=50)
    TxBotOneCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardThree.place(x=150,y=50)
    TxBotOneCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardFour.place(x=190,y=50)
    TxBotOneCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardFive.place(x=230,y=50)

    TxBotTwoCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardOne.place(x=70,y=175)
    TxBotTwoCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardTwo.place(x=110,y=175)
    TxBotTwoCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardThree.place(x=150,y=175)
    TxBotTwoCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardFour.place(x=190,y=175)
    TxBotTwoCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardFive.place(x=230,y=175)

    TxBotThreeCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardOne.place(x=70,y=300)
    TxBotThreeCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardTwo.place(x=110,y=300)
    TxBotThreeCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardThree.place(x=150,y=300)
    TxBotThreeCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardFour.place(x=190,y=300)
    TxBotThreeCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardFive.place(x=230,y=300)

    botOneCards = [TxBotOneCardOne, TxBotOneCardTwo, TxBotOneCardThree, TxBotOneCardFour, TxBotOneCardFive]
    botTwoCards = [TxBotTwoCardOne, TxBotTwoCardTwo, TxBotTwoCardThree, TxBotTwoCardFour, TxBotTwoCardFive]
    botThreeCards = [TxBotThreeCardOne, TxBotThreeCardTwo, TxBotThreeCardThree, TxBotThreeCardFour, TxBotThreeCardFive]
    allBotCards = [botOneCards, botTwoCards, botThreeCards]

    for bot in range(3):
        for card in range(len(allBotHands[bot])): # go through every card in bot hand and make image for the card
            #make image for hole card#
            cardImageFile = Image.open(f"Playing Cards/{allBotHands[bot][card]}")
            resizedCardImageFile = cardImageFile.resize((76, 109), Image.LANCZOS)
            actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
            allBotCards[bot][card].image = actualCardImage
            allBotCards[bot][card].config(image=actualCardImage)

    TxCommunityCardOne = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardOne.place(x=505,y=50)

    TxCommunityCardTwo = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardTwo.place(x=545,y=50)

    TxCommunityCardThree = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardThree.place(x=595,y=50)

    allCommunityCards = [TxCommunityCardOne, TxCommunityCardTwo, TxCommunityCardThree]

    for card in range(3): # go through every card in community hand and make image for the card
        #make image for hole card#
        cardImageFile = Image.open(f"Playing Cards/{communityHand[card]}")
        resizedCardImageFile = cardImageFile.resize((76, 109), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        allCommunityCards[card].image = actualCardImage
        allCommunityCards[card].config(image=actualCardImage)

def GetResultOfGame():

    UpdateBotHandStrengthsList()
    
    winOrLoseList = [] 

    for bot in range(3):

        if (type(playerHandStrength) == tuple) and (type(botHandsStrengths[bot]) == tuple):
            if (playerHandStrength[0] > botHandsStrengths[bot][0]): # if player for example has 3 of a kind and bot has pair, then
                winOrLose = "win"
                winOrLoseList.append(winOrLose)
            elif (playerHandStrength[0] == botHandsStrengths[bot][0]): # if player and bot have same pair (eg both have a pair, or three of a kind) then
                if (playerHandStrength[1] > botHandsStrengths[bot][1]): # if player has better pair or kind then 
                    winOrLose = "win"
                elif (playerHandStrength[1] == botHandsStrengths[bot][1]): # if player has same pair or kind then 
                    winOrLose = "tie"
                elif (playerHandStrength[1] < botHandsStrengths[bot][1]): # if player has worse pair or kind then 
                    winOrLose = "lose"
                winOrLoseList.append(winOrLose)
            elif (playerHandStrength[0] < botHandsStrengths[bot][0]): # if player for example has pair and bot has 3 of a kind, then
                winOrLose = "lose"
                winOrLoseList.append(winOrLose)
        
        if (type(playerHandStrength) == tuple) and (type(botHandsStrengths[bot]) == int):
            if (playerHandStrength[0] > botHandsStrengths[bot]):
                winOrLose = "win"
            elif (playerHandStrength[0] == botHandsStrengths[bot]):
                winOrLose = "tie"
            elif (playerHandStrength[0] < botHandsStrengths[bot]):
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

        if (type(playerHandStrength) == int) and (type(botHandsStrengths[bot]) == tuple):
            if (playerHandStrength > botHandsStrengths[bot][0]): 
                winOrLose = "win"
            elif (playerHandStrength < botHandsStrengths[bot][0]): 
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

        if (type(playerHandStrength) == int) and (type(botHandsStrengths[bot]) == int):
            if (playerHandStrength > botHandsStrengths[bot]):
                winOrLose = "win"
            elif (playerHandStrength == botHandsStrengths[bot]):
                winOrLose = "tie"
            elif (playerHandStrength < botHandsStrengths[bot]):
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

    if "lose" in winOrLoseList:
        winOrLose = f"You lost :["
    elif "tie" in winOrLoseList:
        winOrLose = f"You tied and won {pot/2} coins! :|"
    elif "win" in winOrLoseList:
        winOrLose = f"You won {pot} coins! :]"
    
    return winOrLose

# Showdown round code ends here #


# all game rounds starts #
def ExecuteRoundEleven(FrTableScreen):
    # showdown
    ClearWindowOrFrame(FrTableScreen)
    DisplayCurrentRoundInstruction(FrTableScreen, False)

    BtRaise["state"] = "disabled"
    BtCall["state"] = "disabled"
    BtCheck["state"] = "disabled"
    BtCombine["state"] = "disabled"
    BtFold["state"] = "disabled"

    TxbotOne = Label(FrTableScreen, text="Bot 1", font=("Rockwell", 16), background="light grey")
    TxbotOne.place(x=10,y=50)
    TxbotTwo = Label(FrTableScreen, text="Bot 2", font=("Rockwell", 16), background="light grey")
    TxbotTwo.place(x=10,y=175)
    TxbotThree = Label(FrTableScreen, text="Bot 3", font=("Rockwell", 16), background="light grey")
    TxbotThree.place(x=10,y=300)
    TxCommunityHand = Label(FrTableScreen, text="Community cards", font=("Rockwell", 16), background="light grey")
    TxCommunityHand.place(x=320,y=50)

    PrintAllHands()
    ShowAllBotAndCommunityCards(FrTableScreen)

    winOrLose = GetResultOfGame()
    TxWinOrLose = Label(FrTableScreen, text=winOrLose, font=("Rockwell", 16), background="light grey")
    TxWinOrLose.place(x=10,y=420)

    UpdateAccStatsDB(winOrLose)

    BtLeave = Button(FrTableScreen, text="LEAVE\nGAME", font=("Rockwell", 16), borderwidth=0,
                    background="light grey", compound="c", image=pixel, height=70, width=70,
                    command=lambda:Leave())
    BtLeave.place(x=720,y=420)

def ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundTen, numOfPlayersMadeBetInThisRound, roundTenExecuted, previousRoundLastBet
    # fourth round of betting

    if firstTimeExecutingRoundTen: # do this stuff only if its the first time executing round ten
        numOfPlayersMadeBetInThisRound = 0
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "disabled"
        BtCombine.config(width=229) # make combine button long again
        BtFold["state"] = "normal" # in round 10 user has cards, so can always fold.
        BtContinue.destroy() # destroy continue button after combo round
        firstTimeExecutingRoundTen = False

    if whoseTurn != 0: # if not player's turn
        MakeBotBet(TxPot, FrScrollableText) # make a bot bet
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4:
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"
        DisplayCurrentRoundInstruction(FrTableScreen, True) # tell user what to do
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) # wait for user to change a ___Var() type of variable (used to let user choose what to do)

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: # if not max num of players made a bet per round and if not player's turn then
        ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList) 
    elif numOfPlayersMadeBetInThisRound == 4: # if max num of players made a bet per round then
        previousRoundLastBet = lastBet
        roundTenExecuted = True

def ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global BtContinue, roundNineExecuted, firstTimeExecutingRoundNine, numOfPlayersCombinedInThisRound
    #combo round 2
    
    if firstTimeExecutingRoundNine:
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "normal"

        BtCombine.config(width=109)
        
        BtContinue = Button(FrCommandPanel, text="CONTINUE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:[ClearWindowOrFrame(FrCommandPanelExtension),
                        IncreaseWhoseTurn(),
                        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtContinue.place(x=128,y=107)

        numOfPlayersCombinedInThisRound = 0
        firstTimeExecutingRoundNine = False

    if numOfPlayersCombinedInThisRound == 4: 
        roundNineExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn == 0: # if player's turn and maximum number of players haven't bet yet
        DisplayCurrentRoundInstruction(FrTableScreen, True) # tell user what to do
        numOfPlayersCombinedInThisRound += 1

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn != 0: 
        MakeBotCombine(FrScrollableText) # make a bot combine their cards
        numOfPlayersCombinedInThisRound += 1
        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)    
    
def ExecuteRoundEight(cardButtons, communityCardList):
    global roundEightExecuted

    # give everyone 1 combo card (last combo card making 5/5 combo cards)

    GeneratePlayerCard(cardButtons) # give combo card to player
    GenerateCardForAllBots() # give combo card to every bot 
    GenerateCommunityCard(communityCardList) # place a community card onto table

    print("in round eight - given 5 cards to all")

    roundEightExecuted = True

def ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundSeven, numOfPlayersMadeBetInThisRound, roundSevenExecuted, previousRoundLastBet
    # third round of betting

    if firstTimeExecutingRoundSeven: # do this stuff only if its the first time executing round seven
        numOfPlayersMadeBetInThisRound = 0
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "disabled"
        BtCombine.config(width=229) # make combine button long again
        BtFold["state"] = "normal" # in round 7 user has cards, so can always fold.
        BtContinue.destroy() # destroy continue button after combo round
        firstTimeExecutingRoundSeven = False

    if whoseTurn != 0: # if not player's turn
        MakeBotBet(TxPot, FrScrollableText) # make a bot bet
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4:
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"
        DisplayCurrentRoundInstruction(FrTableScreen, True) # tell user what to do
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) # wait for user to change a ___Var() type of variable (used to let user choose what to do)

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: # if not max num of players made a bet per round and if not player's turn then
        ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif numOfPlayersMadeBetInThisRound == 4: # if max num of players made a bet per round then
        previousRoundLastBet = lastBet
        roundSevenExecuted = True

def ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    #combo round 1

    global BtContinue, roundSixExecuted, firstTimeExecutingRoundSix, numOfPlayersCombinedInThisRound

    if firstTimeExecutingRoundSix:
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "normal"

        BtCombine.config(width=109)
        
        BtContinue = Button(FrCommandPanel, text="CONTINUE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:[ClearWindowOrFrame(FrCommandPanelExtension),
                        UpdateFeedback("tried to combine", FrScrollableText, False, False),
                        IncreaseWhoseTurn(),
                        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtContinue.place(x=128,y=107)

        numOfPlayersCombinedInThisRound = 0
        firstTimeExecutingRoundSix = False

    if numOfPlayersCombinedInThisRound == 4: 
        roundSixExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn == 0: # if player's turn and maximum number of players haven't bet yet
        DisplayCurrentRoundInstruction(FrTableScreen, True) # tell user what to do
        numOfPlayersCombinedInThisRound += 1

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn != 0: 
        
        MakeBotCombine(FrScrollableText) # make a bot combine their cards
        numOfPlayersCombinedInThisRound += 1
        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)    
    
def ExecuteRoundFive(cardButtons, communityCardList):
    global roundFiveExecuted, communityHand
    # give everyone 1 more combo card (now total 4 cards for everyone) and put 2 community cards on table

    GeneratePlayerCard(cardButtons) # give combo card to player
    GenerateCardForAllBots() # give combo card to every bot 
    GenerateCommunityCard(communityCardList) # place community card onto table
    GenerateCommunityCard(communityCardList) # place community card onto table

    print("in round five - given 4 cards to all, 2 comm cards")
    PrintAllHands()

    roundFiveExecuted = True

def ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundFour, numOfPlayersMadeBetInThisRound, roundFourExecuted, BtRaise, BtCall, BtCheck, BtCombine, BtFold, previousRoundLastBet

    # first round of betting

    if firstTimeExecutingRoundFour:

        BtRaise = Button(FrCommandPanel, text="RAISE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=229,
                        command=lambda:ShowRaiseMenu(TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension))
        BtRaise.place(x=8,y=8)

        BtCall = Button(FrCommandPanel, text="CALL", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:Call(TxPlayerCoins, TxPot, FrScrollableText, BtCall)) # call - make bet same as last bet
        BtCall.place(x=8,y=57)

        BtCheck = Button(FrCommandPanel, text="CHECK", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:Check(FrScrollableText))
        BtCheck.place(x=128,y=57)

        BtCombine = Button(FrCommandPanel, text="COMBINE", font=("Rockwell", 15), borderwidth=0,
                            background="light grey", compound="c", image=pixel, height=32, width=229,
                            command=lambda:ShowCombineMenu(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList))
        BtCombine.place(x=8, y=107)

        BtFold = Button(FrCommandPanel, text="FOLD", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=229,
                        command=lambda:Fold(FrTableScreen))
        BtFold.place(x=8,y=156)

        BtCombine["state"] = "disabled"
        BtCheck["state"] = "disabled"

        numOfPlayersMadeBetInThisRound = 0
        firstTimeExecutingRoundFour = False # since round three has been started once dont do the stuff above anymore

    if whoseTurn != 0: # if not player's turn
        MakeBotBet(TxPot, FrScrollableText) # make a bot bet
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4: # if player's turn and maximum number of players haven't bet yet
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"

        DisplayCurrentRoundInstruction(FrTableScreen, True) # tell user what to do
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) # wait for user to change a ___Var() type of variable (used to let user choose what to do)

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: # if not max num of players made a bet per round and if not player's turn then
        ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif numOfPlayersMadeBetInThisRound == 4: # if max num of players made a bet per round then
        previousRoundLastBet = lastBet
        roundFourExecuted = True

def ExecuteRoundThree():
    global roundThreeExecuted, botHandsStrengths, communityHand, allBotHands

    # round 4 is just calculating bot hand strengths

    botHandsStrengths = []

    for hand in range(3):
        botHandStrength = CalculateHandStrength(allBotHands[hand]) # calc. every bot's hand strength
        botHandsStrengths.append(botHandStrength) # add the strength to list of strengths


    roundThreeExecuted = True

def ExecuteRoundTwo(cardButtons):
    global roundTwoExecuted

    # give everyone 3 combo cards (first cards)

    for x in range(3): # give 3 combo cards to player
        GeneratePlayerCard(cardButtons) # give combo card to player
        GenerateCardForAllBots() # give combo card to every bot 

    print("in round two - given 3 cards to all")

    roundTwoExecuted = True

def ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global roundOneExecuted, whoseTurnInRoundOne, firstTimeExecutingRoundOne, numOfBetsMade, previousRoundLastBet, lastBet

    if firstTimeExecutingRoundOne:
        whoseTurnInRoundOne = whoseTurn
        numOfBetsMade = 0
        lastBet = 0
        previousRoundLastBet = ""
        firstTimeExecutingRoundOne = False

    if numOfBetsMade < 4 and whoseTurn != 0: # if not max num of bets in round made and not player's turn
        MakeBotBet(TxPot, FrScrollableText) # bot makes bet
        numOfBetsMade += 1 # add to num of bets made in this round
        ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)


    elif numOfBetsMade < 4 and whoseTurn == 0:
        BtBetBlind = Button(FrCommandPanel, text="BET BLIND (10 COINS)",
                            compound="c", image=pixel, height=32, width=229,
                            font=("Rockwell", 13), borderwidth=0, background="light grey",
                            command=lambda:[DeductCoinsFromPlayer(10, TxPlayerCoins), # take 10 coins away from player upon click
                                            UpdatePot(10, TxPot), # add to pot the bet
                                            UpdateFeedback(10, FrScrollableText, False, False), # add label to game feedback saying who bet how much
                                            IncreaseWhoseTurn(), # make it next player's turn
                                            ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtBetBlind.place(x=8,y=8) 
        numOfBetsMade += 1 

    elif numOfBetsMade == 4:
        previousRoundLastBet = lastBet
        roundOneExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
# all game rounds ends #

def ResetMostGlobalValues():
    global pot, allBotHands, playerHand, communityHand, numOfCards, currentRound, dealer, whoseTurn, roundOneExecuted, roundTwoExecuted, roundThreeExecuted, roundFourExecuted
    global roundFiveExecuted, roundSixExecuted, roundSevenExecuted, roundEightExecuted, roundNineExecuted, roundTenExecuted, roundElevenExecuted, cardsList

    pot = 0

    allBotHands = [ [], [], [] ] # Lists for everyone's hands: list 0 = player, list 1 = bot 1, list 2 = bot 2, list 3 = bot 3.
    playerHand = []
    communityHand = []

    dealer = random.randint(0,3) # makes player, bot 1, bot 2, or bot 3 dealer
    if dealer == 3: # if dealer is bot 3 then
        whoseTurn = 0 # it is player's turn
    else: # if dealer is anyone other than bot 3
        whoseTurn = dealer + 1 # it is bot 1, 2, or 3's turn

    currentRound = 1 # game starts at round 1
    roundOneExecuted = False # no rounds have been executed because game just started
    roundTwoExecuted = False
    roundThreeExecuted = False
    roundFourExecuted = False
    roundFiveExecuted = False
    roundSixExecuted = False
    roundSevenExecuted = False
    roundEightExecuted = False
    roundNineExecuted = False
    roundTenExecuted = False
    roundElevenExecuted = False

    numOfCards = 51 # 51 and not 52 because indexing starts at 0    
    cardsList = CreateListOfCards() # create list of cards


# Leave allows the user to leave the current game and its code starts here # 

def Leave():
    ResetMostGlobalValues()
    ClearWindowOrFrame(main)
    MakeWindowGameMenu()

# Leave code ends here #


# Fold allows the user to fold their hand and its code starts here #

def Fold(FrTableScreen):

    ClearWindowOrFrame(FrTableScreen)

    BtRaise["state"] = "disabled"
    BtCall["state"] = "disabled"
    BtCheck["state"] = "disabled"
    BtCombine["state"] = "disabled"
    BtFold["state"] = "disabled"
    try:
        BtContinue["state"] = "disabled"
    except:
        pass

    TxYouFolded = Label(FrTableScreen, text="You folded and lost.", font=("Rockwell", 16))
    TxYouFolded.place(x=10,y=10)

    UpdateAccStatsDB("lost")

    BtLeave = Button(FrTableScreen, text="LEAVE\nGAME", font=("Rockwell", 16), borderwidth=0,
                    background="light grey", compound="c", image=pixel, height=70, width=70,
                    command=lambda:Leave())
    BtLeave.place(x=10,y=40)

# Fold code ends here #


# UpdateBotHandStrengthsList updates every bot's hand strength according to the cards they have and its code starts here #

def UpdateBotHandStrengthsList():
    global botHandsStrengths, playerHandStrength
    botHandsStrengths = []

    # temp
    # communityHand = ['13_of_spades.png', '14_of_diamonds.png', '10_of_diamonds.png']

    # allBotHands[0] = ['13_of_clubs.png', '13_of_diamonds.png', '6_of_spades.png', '3_of_spades.png', '11_of_diamonds.png'] # 3 of a kind 4
    # allBotHands[1] = ['14_of_clubs.png', '7_of_diamonds.png', '8_of_spades.png', '9_of_spades.png', '6_of_diamonds.png'] # straight 5
    # allBotHands[2] = ['14_of_clubs.png', '13_of_spades.png', '2_of_spades.png', '7_of_spades.png', '12_of_spades.png'] # flush 6

    # temp

    # updating strenghts of bots #
    for bot in range(3):
        tempList = communityHand.copy() # make temp list including community cards

        for card in range(len(allBotHands[bot])):
            tempList.append(allBotHands[bot][card]) # add all of the bot's cards into that list

        botHandStrength = CalculateHandStrength(tempList) # calc. every bot's hand strength
        botHandsStrengths.append(botHandStrength) # add the strength to list of strengths
    ##

    print(f"strengths of all bots: {botHandsStrengths}")

    # updating strength of player # 
    tempList = communityHand.copy() # make temp list including community cards and player cards
    for card in range(len(playerHand)):
        tempList.append(playerHand[card]) # add all of the player's cards into that list
    
    playerHandStrength = CalculateHandStrength(tempList)
    ##

# UpdateBotHandStrengthsList code ends here # 


# IncreaseWhoseTurn increments the next player's turn and its code starts here #

def IncreaseWhoseTurn():
    global whoseTurn # make whoseTurn global to edit its value
   
    if whoseTurn == 3: # if bot 3 just did something
        whoseTurn = 0 # it is player's turn now
    else: # if anyone other than bot 3 just did something
        whoseTurn +=1 # it is the next person's turn

# IncreaseWhoseTurn code ends here # 


# UpdatePot adds the most recent bet made to the pot and its code starts here # 

def UpdatePot(number, TxPot):
    global pot # make pot global to edit its value

    pot += int(number) # add to pot
    TxPot.config(text=f"POT: {pot}") # update pot label with correct pot amount

# UpdatePot code ends here # 


# UpdateFeedback tells the player what the bots and themselves are doing (e.g betting) and its code starts here # 

def UpdateFeedback(number, FrScrollableText, fold, combined):
    if fold: # if somebody folded
        if whoseTurn != 0: # if its not player's turn then
            Label(FrScrollableText, text=f"BOT {whoseTurn} FOLDED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying which bot folded
        else: # if it's player's turn then
            Label(FrScrollableText, text=f"{accountUsername} FOLDED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying player folded 

    elif number == 0: # if the bet multiplier made by player/bot is 0 then 
        if whoseTurn != 0: # and it's not player's turn then
            Label(FrScrollableText, text=f"BOT {whoseTurn} CHECKED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying which bot checked 
        else: # if it's player's turn then
            Label(FrScrollableText, text=f"{accountUsername} CHECKED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying player checked 

    elif not combined and number != "tried to combine": # if somebody didn't try to combine then
        if whoseTurn != 0: # and it's not player's turn then 
            Label(FrScrollableText, text=f"BOT {whoseTurn} PLACED BET OF {number}", font=("Rockwell", 10)).pack() # make label in game feedback frame saying which bot made a bet 
        else: # if it's player's turn then
            Label(FrScrollableText, text=f"{accountUsername} PLACED BET OF {number}", font=("Rockwell", 10)).pack() # make label in game feedback frame saying player made a bet 

    elif not combined and number == "tried to combine": # if somebody tried to combine then
        if whoseTurn != 0: # and it's not player's turn then
            Label(FrScrollableText, text=f"BOT {whoseTurn} DIDN'T COMBINE", font=("Rockwell", 10)).pack() # make label in game feedback frame saying which bot didn't combine their cards
        else: # if it's player's turn then
            Label(FrScrollableText, text=f"{accountUsername} DIDN'T COMBINE", font=("Rockwell", 10)).pack() # make label in game feedback frame saying player didn't combine their cards

    elif combined: # if somebody combined their cards
        if whoseTurn != 0: # and it's not player's turn then
            Label(FrScrollableText, text=f"BOT {whoseTurn} COMBINED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying which bot combined their cards
        else: # if it's player's turn then
            Label(FrScrollableText, text=f"{accountUsername} COMBINED", font=("Rockwell", 10)).pack() # make label in game feedback frame saying player combined their cards

# UpdateFeedback code ends here # 


# DisplayCurrentRoundInstruction adds text to screen saying what to do in the current round and its code starts here #

def DisplayCurrentRoundInstruction(FrTableScreen, labelExists):
    global roundInstruction
   
    if not labelExists:
        roundInstruction = Label(FrTableScreen, text="", font=("Rockwell", 16), background="light grey")
        roundInstruction.place(x=10,y=10)

    if whoseTurn == 0: # if round 1 and player's turn then
        if currentRound == 1:
            roundInstruction.config(text="First round of betting")

        elif currentRound == 4:
            roundInstruction.config(text="Second round of betting")

        elif currentRound == 6:
            roundInstruction.config(text="First combination round")

        elif currentRound == 7:
            roundInstruction.config(text="Third round of betting")

        elif currentRound == 9:
            roundInstruction.config(text="Second combination round")

        elif currentRound == 10:
            roundInstruction.config(text="Fourth round of betting")

    if currentRound == 11:
        roundInstruction.config(text="Showdown")

# DisplayCurrentRoundInstruction code ends here #


# ExecuteGameSequence constantly is recalled to keep the game going and its code starts here # 

def ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global currentRound, firstTimeExecutingRoundOne, firstTimeExecutingRoundFour, firstTimeExecutingRoundSix, firstTimeExecutingRoundSeven, firstTimeExecutingRoundNine, firstTimeExecutingRoundTen

    if currentRound == 1: # blind bet round / first round of betting
        firstTimeExecutingRoundOne = True
        if not roundOneExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, False)
            print("start of 'if not' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundOneExecuted:
            print("start of 'if' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1 # increase round by 1
            print("end of 'if' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 2: # give 3 cards to all players
        if not roundTwoExecuted:
            print("start of 'if not' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundTwo(cardButtons)
            print("end of 'if not' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundTwoExecuted:
            print("start of 'if' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
           
    if currentRound == 3: # calculate hand strengths of all players
        if not roundThreeExecuted:
            print("start of 'if not' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundThree()
            print("end of 'if not' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundThreeExecuted:
            print("start of 'if' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 4: # second round of betting
        firstTimeExecutingRoundFour = True
        if not roundFourExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundFourExecuted:
            print("start of 'if' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            playerMadeDecision.set(False)
            print("end of 'if' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 5: # add 2 community cards, 1 player card and 1 bot card (now total 4 cards with every player)
        if not roundFiveExecuted:
            print("start of 'if not' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundFive(cardButtons, communityCardList)
            print("end of 'if not' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundFiveExecuted:
            print("start of 'if' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 6: # combo round
        firstTimeExecutingRoundSix = True
        if not roundSixExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundSixExecuted:
            print("start of 'if' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 7: # third round of betting
        firstTimeExecutingRoundSeven = True
        if not roundSevenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundSevenExecuted:
            print("start of 'if' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            playerMadeDecision.set(False)
            print("end of 'if' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 8: # add 1 community card, 1 player card and 1 bot card (now total 5 cards with every player)
        if not roundEightExecuted:
            print("start of 'if not' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundEight(cardButtons, communityCardList)
            print("end of 'if not' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundEightExecuted:
            print("start of 'if' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 9: # combo round 2
        firstTimeExecutingRoundNine = True
        if not roundNineExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundNineExecuted:
            print("start of 'if' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 10: # fourth round of betting
        firstTimeExecutingRoundTen = True
        if not roundTenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundTenExecuted:
            print("start of 'if' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 11: # showdown
        if not roundElevenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundEleven(FrTableScreen)
            print("end of 'if not' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundElevenExecuted:
            print("start of 'if' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

# ExecuteGameSequence code ends here # 


# game game window code starts here # 

def MakeWindowGame():

    #window config#
    main.geometry("1050x700+480+200") # +480+200 to center window
    ##

    #Frames#
    #Fr = Frame#
    FrCardScreen = Frame(main, background="dark grey", width=800, height=200)
    FrCardScreen.place(x=0, y=500)

    FrTableScreen = Frame(main, width=800, height=500)
    FrTableScreen.place(x=0, y=0)

    FrCommandPanel = Frame(main, background="grey", width=250, height=200)
    FrCommandPanel.place(x=800, y=500)

    FrGameFeedback = Frame(main, width=250, height=500)
    FrGameFeedback.place(x=800, y=0)

    FrCommandPanelExtension = Frame(main, background="dark grey", width=135, height=200)
    FrCommandPanelExtension.place(x=665, y=500)
    ##

    #Shapes#
    #Ca = Canvas#
    CaTableScreen = Canvas(FrTableScreen, background="light grey", width=800, height=500)
    CaTableScreen.place(x=0, y=0)

    CaTableScreen.create_rectangle(100, 100, 700, 400,
                                outline="black", fill="dark green",
                                width=2)

    CaTableScreen.create_rectangle(50, 150, 100, 350,
                                outline="black", fill="#6F4E37",
                                width=2)

    CaTableScreen.create_rectangle(300, 50, 500, 100,
                                outline="black", fill="#6F4E37",
                                width=2)

    CaTableScreen.create_rectangle(700, 150, 750, 350,
                                outline="black", fill="#6F4E37",
                                width=2)

    CaTableScreen.create_rectangle(300, 400, 500, 450,
                                outline="black", fill="#6F4E37",
                                width=2)
    ##

    #labels#
    #Tx = Text#
    TxBot1Name = Label(FrTableScreen, text="BOT 1", font=("Rockwell", 10), background="#6F4E37", foreground="white")
    TxBot1Name.place(x=55,y=240)

    TxBot2Name = Label(FrTableScreen, text="BOT 2", font=("Rockwell", 10), background="#6F4E37", foreground="white")
    TxBot2Name.place(x=380,y=65)

    TxBot3Name = Label(FrTableScreen, text="BOT 3", font=("Rockwell", 10), background="#6F4E37", foreground="white")
    TxBot3Name.place(x=705,y=240)

    TxPlayerName = Label(FrTableScreen, text=accountUsername, font=("Rockwell", 10), background="#6F4E37", foreground="white")
    TxPlayerName.place(x=380,y=412)

    playerCoins = GetPlayerCoins()
    TxPlayerCoins = Label(FrTableScreen, text=accountUsername + "'s coins: " + str(playerCoins), font=("Rockwell", 16), background="light grey")
    TxPlayerCoins.place(x=297,y=460)

    TxPot = Label(FrTableScreen, text="POT: " + str(pot), font=("Rockwell", 10), background="dark green", foreground="white")
    TxPot.place(x=380,y=200)

    if dealer == 0:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=247,y=413)
    elif dealer == 1:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=49,y=364)
    elif dealer == 2:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=247,y=50)
    elif dealer == 3:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=711,y=364)
    ##

    # creating user's cards starts here #
    BtCardOne = Button(FrCardScreen, borderwidth=0)
    BtCardOne.place(x=15,y=15)

    BtCardTwo = Button(FrCardScreen, borderwidth=0)
    BtCardTwo.place(x=145,y=15)

    BtCardThree = Button(FrCardScreen, borderwidth=0)
    BtCardThree.place(x=275,y=15)

    BtCardFour = Button(FrCardScreen, borderwidth=0)
    BtCardFour.place(x=405,y=15)

    BtCardFive = Button(FrCardScreen, borderwidth=0)
    BtCardFive.place(x=535,y=15)

    
    cardButtons = [BtCardOne, BtCardTwo, BtCardThree, BtCardFour, BtCardFive] # making list of all card buttons
    # creating user's cards ends here #

    # creating community cards starts here #
    TxCommCardOne = Label(FrTableScreen, borderwidth=0)
    TxCommCardOne.place(x=310,y=230)

    TxCommCardTwo = Label(FrTableScreen, borderwidth=0)
    TxCommCardTwo.place(x=380,y=230)

    TxCommCardThree = Label(FrTableScreen, borderwidth=0)
    TxCommCardThree.place(x=450,y=230)

    
    communityCardList = [TxCommCardOne, TxCommCardTwo, TxCommCardThree] # make list of all community cards
    # creating community cards ends here #

    #Game feedback scrollbar code starts here #
    CaGameFeedback = Canvas(FrGameFeedback, width=228, height=496) # make canvas in game feedback frame.
    scrollBar = Scrollbar(FrGameFeedback, orient="vertical", command=CaGameFeedback.yview) # put scrollbar into game feedback frame.
    FrScrollableText = Frame(CaGameFeedback) # make frame of scrollable text in canvas (the one in game feedback frame).

    FrScrollableText.bind("<Configure>", lambda e: CaGameFeedback.configure(scrollregion=CaGameFeedback.bbox("all")))
    # /\-- make a box to scroll the text inside
    CaGameFeedback.create_window((0, 0), window=FrScrollableText, anchor="nw") # make a window for the scrollable text.
    CaGameFeedback.configure(yscrollcommand=scrollBar.set) # attach scrollable text frame to scrollbar.

    CaGameFeedback.pack(side=LEFT, fill=BOTH, expand=True)
    scrollBar.pack(side=RIGHT, fill="y")

    CaGameFeedback.update_idletasks() # used to move scrollbar to bottom by default.
    CaGameFeedback.yview_moveto(1) # move scrollbar to bottom by default.
    # must "_moveto" bottom AFTER packing scrollbar.
    # Game feedback scrollbar code ends here #
   
    ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)

# game game window code ends here #


# game window menu code starts here #

def MakeWindowGameMenu():

    #window config#
    main.geometry("215x215")
    ##

    #labels#
    #Tx = Text#
    TxGame = Label(main, text="GAME", font=("Rockwell", 18))
    TxGame.pack()
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtPlay = Button(main, text="PLAY",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(2))
    BtPlay.place(x=8, y=33)

    BtViewAccStats = Button(main, text="VIEW ACCOUNT\nSTATISTICS",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=60, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(3))
    BtViewAccStats.place(x=8, y=70)

    BtHelp = Button(main, text="HELP",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(1))
    BtHelp.place(x=8, y=142)

    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(0))
    BtBack.place(x=8, y=179)
    ##

    if not loggedIn: # this is to stop user from playing and viewing account stats without logging in
        BtPlay["state"] = "disabled"
        BtViewAccStats["state"] = "disabled"

# game window menu code ends here #


# account stats window code starts here #

def MakeWindowAccountStats():

    #window config#
    main.geometry("400x230")
    ##

    statsDbName = (f"Stats({accountUsername}).db") # defining name of this account's stats database file
    con = sqlite3.connect(statsDbName) # making connection to database
    cursor = con.cursor() # creating a cursor for this connection
        
    # retrieve all data in stats table and place it in statsList array
    cursor.execute(f"SELECT * FROM tblStats_{accountUsername}")
    records = cursor.fetchall()
    statsList = []

    for x in range(6):
        for row in records:
            statsList.append(row[x])
    cursor.close()
    
    statsList.pop(0) # remove "None" value that is at start of list for some reason

    #labels#
    #Tx = Text#
    TxStatsTitle = Label(main, text=f"{accountUsername}'s STATISTICS", font=("Rockwell", 18))
    TxStatsTitle.pack()

    TxCurrentMoney = Label(main, text=f"Current coins: {statsList[0]}", font=("Rockwell", 18))
    TxCurrentMoney.place(x=10, y=30)

    TxHandsWon = Label(main, text=f"Total hands won: {statsList[1]}", font=("Rockwell", 18))
    TxHandsWon.place(x=10, y=60)

    TxHandsLost = Label(main, text=f"Total hands lost: {statsList[2]}", font=("Rockwell", 18))
    TxHandsLost.place(x=10, y=90)

    TxLifetimeWinnings = Label(main, text=f"Lifetime winnings: {statsList[3]}", font=("Rockwell", 18))
    TxLifetimeWinnings.place(x=10, y=120)

    TxBiggestPotWon = Label(main, text=f"Biggest pot won: {statsList[4]}", font=("Rockwell", 18))
    TxBiggestPotWon.place(x=10, y=150)
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=375,
                    borderwidth=0, bg="light grey",
                    command=lambda:[ClearWindowOrFrame(main),
                    MakeWindowGameMenu()])
    BtBack.place(x=10, y=190)
    ##

# account stats window code ends here #


# messages to user code starts here #

def AccountCreatedMessage(BtBack, BtRegisterAccount):
    main.geometry("295x258")
    counter = 0
    BtBack["state"] = "disabled" # disable button while counting down the return to main menu
    BtRegisterAccount["state"] = "disabled" # disable button while counting down the return to main menu
    actualText = "ACCOUNT CREATED.\nRETURNING TO MAIN MENU IN 3..."
    TxFeedback = Label(main, text=actualText, font=("Rockwell", 10))
    TxFeedback.place(x=45, y=220)
    UpdateAccountCreatedMessage(counter, TxFeedback, actualText)

def UpdateAccountCreatedMessage(counter, TxFeedback, actualText):
    actualText = actualText[0:-4] + str(3-counter) + "..."
    TxFeedback.config(text=actualText)
    counter += 1
    if counter <= 4:
        #count down from 3 to 0
        main.after(1000, lambda:UpdateAccountCreatedMessage(counter, TxFeedback, actualText))
    else:
        TxFeedback.destroy()
        counter = 0
        #return to main menu
        RegisterMenuToAnotherMenu(1)

def LoggedIntoAccountMessage(BtBack, BtLogIn):
    if loggedIn:
        main.geometry("295x185")
        counter = 0
        BtBack["state"] = "disabled" # disable back button while counting down the return to main menu
        BtLogIn["state"] = "disabled" # disable login button while counting down the return to main menu
        actualText = "LOGGING INTO ACCOUNT.\nRETURNING TO MAIN MENU IN 3..."
        TxFeedback = Label(main, text=actualText, font=("Rockwell", 10))
        TxFeedback.place(x=45, y=145)
        UpdateLoggedInMessage(counter, TxFeedback, actualText)

def UpdateLoggedInMessage(counter, TxFeedback, actualText):
    actualText = actualText[0:-4] + str(3-counter) + "..."
    TxFeedback.config(text=actualText)
    counter += 1
    if counter < 5:
        #count down from 3 to 0
        main.after(1000, lambda:UpdateLoggedInMessage(counter, TxFeedback, actualText))
    else:
        TxFeedback.destroy()
        counter = 0
        #return to main menu
        LogInMenuToAnotherMenu(1)

# messages to user code ends here #


# registering, logging in and account deletion code starts here #

def LogOut(BtLogOut, BtBack, TxLoggedInUser):
    global loggedIn, accountUsername, accountPassword
    loggedIn = False
    accountUsername = ""
    accountPassword = ""

    BtLogOut.destroy()
    BtBack.destroy()
    TxLoggedInUser.destroy()
    print("LOGGED OUT")
    AccountMenuToAnotherMenu(0)

def FindUser(EnUsername, EnPassword, delete):

    def DeleteAccount(givenUsername):
        global loggedIn, accountUsername, accountPassword
        cursor.execute("DELETE from tblAccounts where username = ?", (givenUsername,)) #comma needed for some reason
        con.commit()

        try:
            os.remove(f"E:\Programming\VS Code Python Programs\CS NEA\Stats({givenUsername}).db")
            print("Account and its stats have been DELETED")
        except:
            print("Account has been DELETED")
            print("deleted account doesn't have stats db.")
            
        loggedIn = False
        accountUsername = None
        accountPassword = None
        cursor.close()

    def LogUserIn(givenUsername, givenPassword):
        print("Username & Password: MATCH. LOGGED IN.")
        global loggedIn, accountUsername, accountPassword
        loggedIn = True
        accountUsername = givenUsername
        accountPassword = givenPassword
        CheckAccStatsDB() # check if stats db file exists for this user that loggged in.

    #BELOW - login. makes temp list w/ temp user + pass. Checks if user and pass match.

    givenUsername = EnUsername.get()
    givenPassword = EnPassword.get()

    con = sqlite3.connect("Accounts.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM tblAccounts')
    records = cursor.fetchall()

    tempLoginList = [str(givenUsername), str(givenPassword)]
    recordsList = []

    for col in records:
        recordsList.append(col[0])
        recordsList.append(col[1])

    usernameMatch = False
    passwordMatch = False

    for x in range(0, len(recordsList)):
        if tempLoginList[0] == recordsList[x - 1]:
            usernameMatch = True
            if usernameMatch == True:
                y = x
            if tempLoginList[1] == recordsList[y]:
                passwordMatch = True
    print(recordsList)
    if usernameMatch and passwordMatch:
        if delete:
            DeleteAccount(givenUsername)
        elif not delete:
            LogUserIn(givenUsername, givenPassword)

    elif not usernameMatch and not passwordMatch:
        print("\nUsername & Password: DON'T MATCH.")

    cursor.close()

def RegisterUser(EnUsername, EnPassword, EnConfirmPassword, BtBack, BtRegisterAccount):
    username = EnUsername.get()
    password = EnPassword.get()
    confirmPassword = EnConfirmPassword.get()

    if password == confirmPassword:
        con = sqlite3.connect(f"Accounts.db")
        cursor = con.cursor()
        record = []
        cursor.execute('SELECT * FROM tblAccounts')
        records = cursor.fetchall()
        recordsList = []

        usernamesMatch = False

        for col in records:
            recordsList.append(col[0])

        for x in range(0, len(recordsList)):
            if username == recordsList[x - 1]:
                usernamesMatch = True

        if usernamesMatch:
            print("\n----------------------------------\n")
            print(f"username: '{username}' ALREADY EXISTS.\n")
            # do something here to retry

        record.append(username)
        record.append(password)

        if not usernamesMatch:
            cursor.execute("INSERT INTO tblAccounts VALUES (?,?)", record)
            con.commit()
            star = "*"
            print("""
            Account CREATED.
            Username: '""" + username + """'.
            Password: '""" + star*len(password) + """'.
            """)
            record = []
            AccountCreatedMessage(BtBack, BtRegisterAccount)
    else:
        print("password and confirm password doesn't match")

# registering, logging in and account deletion code ends here #


# account/account statistic database file code starts here #

def UpdateAccStatsDB(wonOrLost):

    statsDbName = (f"Stats({accountUsername}).db")
    con = sqlite3.connect(f"{statsDbName}")
    cursor = con.cursor()
        
    if "won" in wonOrLost:

        cursor.execute(f"UPDATE tblStats_{accountUsername} SET currentMoney = currentMoney + {pot}")
        con.commit()

        cursor.execute(f"UPDATE tblStats_{accountUsername} SET handsWon = handsWon + 1")
        con.commit()

        cursor.execute(f"UPDATE tblStats_{accountUsername} SET lifetimeWinnings = lifetimeWinnings + {pot}")
        con.commit()

        # retrieve previously biggest pot won
        cursor.execute(f"SELECT biggestPotWon FROM tblStats_{accountUsername}")
        for row in cursor:
            biggestPotWon = row[0]

        # check if current pot that player won is bigger than his previously biggest pot won
        if pot > biggestPotWon:
            cursor.execute(f"UPDATE tblStats_{accountUsername} SET biggestPotWon = {pot}") # update accordingly
            con.commit()

    elif "tie" in wonOrLost:

        cursor.execute(f"UPDATE tblStats_{accountUsername} SET currentMoney = currentMoney + {pot/2}")
        con.commit()

        cursor.execute(f"UPDATE tblStats_{accountUsername} SET lifetimeWinnings = lifetimeWinnings + {pot/2}")
        con.commit()

        # retrieve previously biggest pot won
        cursor.execute(f"SELECT biggestPotWon FROM tblStats_{accountUsername}")
        for row in cursor:
            biggestPotWon = row[0]

        # check if current pot that player won is bigger than his previously biggest pot won
        if (pot/2) > biggestPotWon:
            cursor.execute(f"UPDATE tblStats_{accountUsername} SET biggestPotWon = {pot/2}") # update accordingly
            con.commit()

    elif "lost" in wonOrLost:
        cursor.execute(f"UPDATE tblStats_{accountUsername} SET handsLost = handsLost + 1")
        con.commit()

    cursor.close()

def CheckAccStatsDB():

    #BELOW - checks if Stats(accountUsername).db file exists. If not, makes new table with default data
    statsDbName = (f"Stats({accountUsername}).db")
    
    if isfile(statsDbName):
        print("\n----------------------------------\n")
        print(f"'{statsDbName}' DATABASE EXISTS.")
        print("\n----------------------------------\n")

    else:
        print(f"\nNO DATABASE FOUND.\n CREATING '{statsDbName}' DATABASE.")
        con = sqlite3.connect(f"{statsDbName}")
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE tblStats_""" + accountUsername + """
            (
            """ + accountUsername + """ STRING,
            currentMoney INT,
            handsWon INT,
            handsLost INT,
            lifetimeWinnings INT,
            biggestPotWon INT,
            primary key (""" + accountUsername + """)
            )
            """)

        # insert default data for new table of stats
        cursor.execute(f"INSERT INTO tblStats_{accountUsername} (currentMoney,handsWon,handsLost,lifetimeWinnings,biggestPotWon) \
                                                                VALUES (100000, 0, 0, 0, 0)")
        con.commit()

def MakeAccountTableDB():

    #BELOW - checks if db exists. makes db file if not found.
    dbName = ("Accounts.db")
    if isfile(f"{dbName}"):
        print("\n'Accounts.db' DATABASE EXISTS.")
    else:
        print("NO DATABASE FOUND.\n CREATING 'Accounts.db' DATABASE.")
        con = sqlite3.connect(f"{dbName}")
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE tblAccounts
            (
            username STRING,
            password STRING,
            primary key (username)
            )
            """)

# account/account statistic database file code ends here #


# delete account window code starts here #

def MakeWindowDelAccMenu():

    #window config#
    main.geometry("295x155")
    ##

    #labels#
    #Tx = Text#
    TxDelAcc = Label(main, text="DELETE ACCOUNT", font=("Rockwell", 18))
    TxDelAcc.pack()

    TxUsername = Label(main, text="USERNAME", font=("Rockwell", 18))
    TxUsername.place(x=5, y=40)

    TxPassword = Label(main, text="PASSWORD", font=("Rockwell", 18))
    TxPassword.place(x=5, y=80)
    ##

    #entries#
    #En = Entry#
    EnUsername = Entry(main, width=22)
    EnUsername.place(x=150, y=46)

    EnPassword = Entry(main, show="*", width=22)
    EnPassword.place(x=150, y=87)
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:DelAccountMenuToAnotherMenu(0))
    BtBack.place(x=10, y=116)

    BtDelAcc = Button(main, text="DELETE",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:FindUser(EnUsername, EnPassword, True)) # True means delete account
    BtDelAcc.place(x=150, y=116)
    ##

# delete account window code ends here #


# login window code starts here #

def MakeWindowLogInMenu():

    #window config#
    main.geometry("295x155")
    ##

    #labels#
    #Tx = Text#
    TxLogIn = Label(main, text="LOG IN", font=("Rockwell", 18))
    TxLogIn.pack()

    TxUsername = Label(main, text="USERNAME", font=("Rockwell", 18))
    TxUsername.place(x=5, y=40)

    TxPassword = Label(main, text="PASSWORD", font=("Rockwell", 18))
    TxPassword.place(x=5, y=80)
    ##

    #entries#
    #En = Entry#
    EnUsername = Entry(main, width=22)
    EnUsername.place(x=150, y=46)

    EnPassword = Entry(main, show="*", width=22)
    EnPassword.place(x=150, y=87)
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:LogInMenuToAnotherMenu(0))
    BtBack.place(x=10, y=116)

    BtLogIn = Button(main, text="LOG IN",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:[FindUser(EnUsername, EnPassword, False), # False means dont delete account, but log in
                                    LoggedIntoAccountMessage(BtLogIn, BtBack)])
    BtLogIn.place(x=150, y=116)
    ##

# login window code ends here #


# Register window code starts here #

def MakeWindowRegisterMenu():

    #window config#
    main.geometry("295x228")
    ##

    #labels#
    #Tx = Text#
    TxRegister = Label(main, text="REGISTER", font=("Rockwell", 18))
    TxRegister.pack()

    TxUsername = Label(main, text="USERNAME", font=("Rockwell", 18))
    TxUsername.place(x=5, y=40)

    TxPassword = Label(main, text="PASSWORD", font=("Rockwell", 18))
    TxPassword.place(x=5, y=80)

    TxCofirmPassword = Label(main, text="CONFIRM\nPASSWORD", font=("Rockwell", 18))
    TxCofirmPassword.place(x=5, y=120)
    ##

    #entries#
    #En = Entry#
    EnUsername = Entry(main, width=22)
    EnUsername.place(x=150, y=46)

    EnPassword = Entry(main, show="*", width=22)
    EnPassword.place(x=150, y=87)

    EnConfirmPassword = Entry(main, show="*", width=22)
    EnConfirmPassword.place(x=150, y=127)
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:RegisterMenuToAnotherMenu(0))
    BtBack.place(x=10, y=188)

    BtRegisterAccount = Button(main, text="REGISTER",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=130,
                    borderwidth=0, bg="light grey",
                    command=lambda:RegisterUser(EnUsername, EnPassword, EnConfirmPassword, BtBack, BtRegisterAccount))
    BtRegisterAccount.place(x=150, y=188)
    ##

# Register window code ends here #


# Account window code starts here #

def MakeWindowAccountMenu():

    BtLogOut = Button(main)
    BtLogOut.destroy()
    BtLogIn = Button(main)
    BtLogIn.destroy()

    #window config#
    main.geometry("246x197")
    ##

    #labels#
    #Tx = Text#
    TxAccount = Label(main, text="ACCOUNT", font=("Rockwell", 18))
    TxAccount.pack()
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtRegister = Button(main, text="REGISTER",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=225,
                    borderwidth=0, bg="light grey",
                    command=lambda:AccountMenuToAnotherMenu(1))
    BtRegister.place(x=8, y=40)

    BtDeleteAccount = Button(main, text="DELETE ACCOUNT",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=225,
                    borderwidth=0, bg="light grey",
                    command=lambda:AccountMenuToAnotherMenu(3))
    BtDeleteAccount.place(x=8, y=120)

    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=225,
                    borderwidth=0, bg="light grey",
                    command=lambda:AccountMenuToAnotherMenu(0))
    BtBack.place(x=8, y=160)

    if loggedIn:
        main.geometry("246x227")

        BtLogIn.destroy()

        BtLogOut = Button(main, text="LOG OUT",
                        font=("Rockwell", 18),
                        compound="c", image=pixel,
                        height=25, width=225,
                        borderwidth=0, bg="light grey",
                        command=lambda:LogOut(BtLogOut, BtBack, TxLoggedInUser))
        BtLogOut.place(x=8, y=80)

        

        TxLoggedInUser = Label(main, text=f"Logged into: {accountUsername}", font=("Rockwell", 11))
        TxLoggedInUser.place(x=8, y=195)

    elif not loggedIn:

        BtLogOut.destroy()

        BtLogIn = Button(main, text="LOG IN",
                        font=("Rockwell", 18),
                        compound="c", image=pixel,
                        height=25, width=225,
                        borderwidth=0, bg="light grey",
                        command=lambda:AccountMenuToAnotherMenu(2))
        BtLogIn.place(x=8, y=80)
    ##

# Account window code ends here #


# Main menu window code starts here #

def MakeWindowMainMenu():

    #window config#
    main.geometry("200x157")
    ##

    #labels#
    #Tx = Text#
    TxMainMenu = Label(main, text="MAIN MENU", font=("Rockwell", 18))
    TxMainMenu.pack()
    ##

    #buttons#
    #Bt = Button#
    #compound=c is used to make text appear along with image=pixel#
    BtAccount = Button(main, text="ACCOUNT",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=180,
                    borderwidth=0, bg="light grey",
                    command=lambda:MainMenuToAnotherMenu(0))
    BtAccount.place(x=8, y=40)

    BtGame = Button(main, text="GAME",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=180,
                    borderwidth=0, bg="light grey",
                    command=lambda:MainMenuToAnotherMenu(1))
    BtGame.place(x=8, y=80)

    BtExit = Button(main, text="EXIT",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=180,
                    borderwidth=0, bg="light grey",
                    command=lambda:MainMenuToAnotherMenu(2))
    BtExit.place(x=8, y=120)
    ##

# Main menu window code ends here #

cardsList = CreateListOfCards() # create list of cards
MakeAccountTableDB() # create database for accounts if one doesnt already exist
MakeWindowMainMenu() # open main menu of game
main.mainloop()
