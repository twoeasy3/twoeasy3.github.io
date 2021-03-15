from tkinter import *
import random
import os

class card(object):
    def __init__(self,card_id,NAME,RATING,TEAM,NATIONALITY,RARITY,WEIGHT,PICTURE="mystery.png"):
        self.card_id = card_id
        self.name = NAME
        self.rating = RATING
        self.team = TEAM
        self.nationality = NATIONALITY
        self.rarity = RARITY
        self.weight = WEIGHT
        self.picture = PICTURE

def getPackContents():
    packContents = open("packcontents.dat",'r')
    newline = packContents.readline()
    PackGrabber = []
    while "End of" not in newline :
        if newline[0] == "|":
            newline = newline.strip('\n')
            newline = newline.split('|')            
            print(newline)
            cardList[newline[1]] = card(newline[1],
                                        newline[2],
                                        newline[3],
                                        newline[4],
                                        newline[5],
                                        newline[6],
                                        newline[7],
                                        newline[8])
            print(newline[6])
            if newline[6] == "RARE":
                packweight = int(((100-eval(newline[3]))**2)/16)
            elif newline[6] == "COMMON":
                packweight = int(((100-eval(newline[3]))**2)/18)
            elif newline[6] == "HERO":
                packweight = 3
            elif newline[6] == "LEGEND":
                packweight = 4
            elif newline[6] == "FLASHBACK":
                packweight = int(((100-eval(newline[3]))**2)/36)
                if packweight < 4:
                    packweight = 4
            else:
                packweight = 3
            print(packweight)
            for i in range(1,packweight):
                PackGrabber.append(newline[1])
        newline = packContents.readline()
    return(PackGrabber)
def drawCard():
        cardPulled = cardList[PackGrabber[random.randint(0,len(PackGrabber)-1)]]
        print(cardPulled.rating,cardPulled.name,cardPulled.team,cardPulled.nationality,cardPulled.rarity)
        return(cardPulled)    
        
def openPack():
        global packsLeft
        if packsLeft == 0:            
            debrief()
            return    
        packsLeft -= 1
        pressToOpen.config(text="Click here to open a pack! Packs left: {0}".format(packsLeft))
        if packsLeft == 0:
            pressToOpen.config(text="Out of packs! Click here to see a summary.",command=quitToSummary)
        first_card = drawCard()
        second_card = drawCard()
        while first_card == second_card:
            second_card = drawCard()
        third_card = drawCard()
        while third_card == first_card or third_card == second_card:
            third_card = drawCard()
        label2.config(text=max(first_card.rating,second_card.rating,third_card.rating), font = "Verdana 24 bold")
        path1 = os.path.join(os.getcwd(),"cards",first_card.picture)
        path2 = os.path.join(os.getcwd(),"cards",second_card.picture)
        path3 = os.path.join(os.getcwd(),"cards",third_card.picture)
        card1.config(file = path1)
        card2.config(file = path2)
        card3.config(file = path3)
        findAndAddOne(first_card)
        findAndAddOne(second_card)
        findAndAddOne(third_card)
        root.mainloop()

def debrief():
        root = Tk()
        summary = Frame(root)
        summary.pack(side = "bottom")
        savefile = open("packpulls.dat","r+")
        lines= []
        newline = savefile.readline()
        curr_row = 0
        curr_column = 0
        path = os.path.join(os.getcwd(),"icons","uncollected","mystery.png")
        icon = PhotoImage(file = path)
        iconLabel = Label(summary,image = icon).grid(row=curr_row,column = curr_column)
        cardCount = Label(summary,text="none", font = "Verdana 20 bold")
        while len(newline) != 0 and newline[0] == '|':
            if curr_column == 10:
                curr_column = 0
                curr_row +=2
            newline = newline.strip('\n')
            (nothing,card,number,nothing) = newline.split('|')
            if int(number) == 0:
                path = os.path.join(os.getcwd(),"icons","uncollected",cardList[card].picture)
            else:
                path = os.path.join(os.getcwd(),"icons","collected",cardList[card].picture)
            icon = PhotoImage(file = path)
            iconLabel = Label(summary,image = icon)
            iconLabel.image = icon
            iconLabel.grid(row=curr_row,column = curr_column)
            cardCount = Label(summary,text= number, font = "Verdana 12 bold")
            cardCount.text = number
            cardCount.grid(row=curr_row+1 , column = curr_column)
            curr_column += 1
            newline = savefile.readline()
        root.mainloop()
        
def findAndAddOne(CARD):
    savefile = open("packpulls.dat","r+")
    lines= []
    newline = savefile.readline()
    while len(newline) != 0 and newline[0] == '|':
        newline = newline.strip('\n')
        (nothing,card,number,nothing) = newline.split('|')
        if card == CARD.card_id:
            number = int(number)+1
            newline = "|{0}|{1}|:)".format(card,number)
        lines.append(newline)
        newline = savefile.readline()
    savefile.close()
    savefile = open("packpulls.dat","w")
    for i in range(0,len(lines)):
        print(lines[i],file = savefile)
    print("End of File",file = savefile)
    savefile.close()

def quitToSummary():
    root.destroy()
    debrief()
            


packsLeft = 5
cardList = {}
PackGrabber = getPackContents()
print(PackGrabber)
root = Tk()
frame = Frame(root)
frame.pack()
mysterypath = os.path.join(os.getcwd(),"cards","mystery.png")
card1 = PhotoImage(file= mysterypath)
card2 = PhotoImage(file= mysterypath)
card3 = PhotoImage(file= mysterypath)
card1Label = Label(frame,image=card1)
card2Label = Label(frame,image=card2)
card3Label = Label(frame,image=card3)
label2 = Label(frame,text="nothing")
pressToOpen = Button(root,text="Click here to open a pack! Packs left: {0}".format(packsLeft),command=openPack)
pressToOpen.pack()
card1Label.pack(side="left")
card2Label.pack(side="left")
card3Label.pack(side="left")
label2.pack()
root.mainloop()

