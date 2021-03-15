import pygame
import random
from network import Network
import time
import pickle
from _thread import *
import startscreen

pygame.init()
clock = pygame.time.Clock()
window_w = 1200
window_h = 800
window = pygame.display.set_mode((window_w,window_h))
window.fill((40,80,120))
pygame.display.set_caption("Citadels P2W Edition")
hand_collisions = []##list of tupple of (collision_r rect,cardname)
board_collisions = [] ##list of tupple of (collision_r rect,cardname)
UI_collisions = []
faceup_this_round = []
dead_this_round = []
robbed_this_round = []
magicianFlag = False
activeTurn = False
abilityTurn = [False,False]

selectedCharacters = {1:'Assassin',
                      2:'Thief',
                      3:'Magician',
                      4:'King',
                      5:'Bishop',
                      6:'Merchant',
                      7:'Architect',
                      8:'Warlord'} ### for later implementation

boardCoords = [[(190,600),(240,600),(290,600),(340,600),(390,600), ##opponent slots 1 thru 7; player slot 0
                (190,520),(240,520),(290,520),(340,520)],
               [(480,600),(530,600),(580,600),(630,600),(680,600),
                (480,520),(530,520),(580,520),(630,520)],
               [(835,280),(835,330),(835,380),(835,430),(835,490),
                (755,280),(755,330),(755,380),(755,430)],
               [(835,10),(835,60),(835,110),(835,160),(835,210),
                (755,10),(755,60),(755,110),(755,160)],               
               [(680,15),(630,15),(580,15),(530,15),(480,15),
                (680,95),(630,95),(580,95),(530,95)],
               [(390,15),(340,15),(290,15),(240,15),(190,15),
                (390,95),(340,95),(290,95),(240,95)],
               [(10,10),(10,60),(10,110),(10,160),(10,210),
                (90,10),(90,60),(90,110),(90,160)],
               [(10,280),(10,330),(10,380),(10,430),(10,490),
                (90,280),(90,330),(90,380),(90,430)]]

infoCoords = [[(190+50,475),(240+50,475),(204+50,442),(236+50,442),(268+50,442)], ##Profile Pic, name, crown, full_districts, completed_city
              [(480,475),(530,475),(496,442),(528,442),(560,442)],
              [(707,360),("calculate",710,360),(707,327),(675,327),(642,327)],
              [(707,280),("calculate",710,280),(707,247),(675,247),(642,247)],
              [(480,202),(530,202),(496,169),(528,169),(560,169)],
              [(190+50,202),(240+50,202),(204+50,169),(236+50,169),(268+50,169)],
              [(152,280),(202,280),(168,247),(200,247),(232,247)],
              [(152,360),(202,360),(168,327),(200,327),(232,327)]]


player_r = []

for i in range(0,len(infoCoords)): ##fix slots 2 and 3
    player_r.append(pygame.Rect(infoCoords[i][0][0],infoCoords[i][0][1],150,40))
    

rank_coords = [(355,282),(407,282),(459,282),(511,282),
                (355,334),(407,334),(459,334),(511,334)]

rank_targets = []
for i in range(0,len(rank_coords)):
    rank_targets.append(pygame.Rect(rank_coords[i][0],rank_coords[i][1],50,50))
    
               
               
               
class Card(object):
    def __init__(self,name,cost,colour,text,copies,cardimage):
        self.name = name
        self.cost = cost
        self.colour = colour
        ##self.text = text ##not necessary for now
        self.copies = copies
        self.cardimage = cardimage

class Character(object):
    def __init__(self,name,rank,text,cardimage):
        self.name = name
        self.rank = rank
        self.cardimage = cardimage
        ##self.text = text ##not necessary for now
    
class Player(object):
    def __init__(self,name,character = None,
                 gold=2,hand = None,board = None,king = False, buildlimit = 1):
        self.name = name
        self.character = None
        self.gold = gold
        if hand == None:
            self.hand = []
        else:
            self.hand = hand
        if board == None:
            self.board = []
        else:
            self.board = board
        self.king = king
        self.buildlimit = buildlimit

    def use_ability(self):
        if self.character == "Assassin":
            if abilityTurn[0] == True:
                abilityTurn[0] = False
                global dead_this_round
                update_info_box("Click on a character icon to kill.")
                image1 = "gui/ability_assassin.png"
                choice = choice_of_two(image1,None)
                if choice == 1:
                    deaded = get_target()
                    dead_this_round.append(deaded)
                    reply = "You killed the " + selectedCharacters[deaded]
                    n.sendNoReply("assassinate",deaded)
                    update_info_box(reply)
                    draw_rank_icons()

        elif self.character == "Thief":
            if abilityTurn[0] == True:
                abilityTurn[0] = False
                global robbed_this_round
                update_info_box("Click on a character icon to rob.")
                image1 = "gui/ability_thief.png"
                choice = choice_of_two(image1,None)
                if choice == 1:
                    robbed = get_target([2])## rank 2 is illegal target
                    robbed_this_round.append(robbed)
                    reply = "You robbed the " + selectedCharacters[deaded]
                    n.sendNoReply(('robbed',robbed))
                    update_info_box(reply)
            pass
        
        elif self.character == "Magician":
            image1 = "gui/ability_magicianSwap.png"
            image2 = "gui/ability_magicianCycle.png"
            choice = choice_of_two(image1,image2)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    update_info_box("Click on a player to swap hands.")
                    target = target_player()
                    target = slot_to_player(target)
                    currentHand = p.hand
                    opponentHand = opponents[target][0].hand
                    p.hand = opponentHand
                    n.sendNoReply(("new_hand",currentHand,target))
                    update_screen() ##OPTIMISE THIS
                    pygame.display.flip()
            elif choice == 2:
                if abilityTurn[1] == True:
                    abilityTurn[1] = False
                    global magicianFlag
                    magicianFlag = True
                    update_info_box("Select cards to cycle.")
                    print("CYCLE")
                    
        elif self.character == "King":
            image1 = "gui/ability_district.png"
            choice = choice_of_two(image1,None)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    for district in self.board:
                        if cards[district].colour == "Yellow" or cards[district].name == "School Of Magic":
                            self.gold +=1
                            update_gold()

        elif self.character == "Bishop":
            image1 = "gui/ability_district.png"
            choice = choice_of_two(image1,None)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    for district in self.board:
                        if cards[district].colour == "Blue" or cards[district].name == "School Of Magic":
                            self.gold +=1
                            update_gold()
            
        elif self.character == "Merchant":
            image1 = "gui/ability_Merchant.png"
            image2 = "gui/ability_district.png"
            choice = choice_of_two(image1,image2)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    self.gold += 1
                    update_gold()
            if choice == 2:
                if abilityTurn[1] == True:
                    abilityTurn[1] = False
                    for district in self.board:
                        if cards[district].colour == "Green" or cards[district].name == "School Of Magic":
                            self.gold +=1
                            update_gold()                  

        elif self.character == "Architect":
            image1 = "gui/ability_architect.png"
            choice = choice_of_two(image1,None)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    self.draw(2)
                
            pass
        elif self.character == "Warlord":
            image1 = "gui/ability_warlord.png"
            image2 = "gui/ability_district.png"
            choice = choice_of_two(image1,image2)
            if choice == 1:
                if abilityTurn[0] == True:
                    abilityTurn[0] = False
                    update_info_box("Click on a player to target.")
                    target = slot_to_player(target_player([0]))
                    while len(opponents[target][0].board) <7 and opponents[target][0].character != "Bishop":
                        target = slot_to_player(target_player([0]))
                    warlord_draw(opponents[target][0])
                    print("DESTROY")
            if choice == 2:
                if abilityTurn[1] == True:
                    abilityTurn[1] = False
                    for district in self.board:
                        if cards[district].colour == "Red" or cards[district].name == "School Of Magic":
                            self.gold +=1
                            update_gold()


            pass
        
    def get_score(self):
        score = 0
        for card in self.board:
            score += cards[card].cost
            if card == "Dragon Gate" or card == "University":
                score += 2
        return(score)

    def get_complete_set(self):
        if len(self.board) > 4:
            HauntedFlag = False
            districts = [False,False,False,False,False]
            for card in self.board:
                if card != "Haunted City":
                    if cards[card].colour == "Red":
                        districts[0] = True
                    elif cards[card].colour == "Blue":
                        districts[1] = True
                    elif cards[card].colour =="Yellow":
                        districts[2] = True
                    elif cards[card].colour == "Green":
                        districts[3] = True
                    elif cards[card].colour == "Purple":
                        districts[4] = True
                else:
                    HauntedFlag = True
            if districts.count(False) == 0:
                return(True)
            elif districts.count(False) == 1 and HauntedFlag == True:
                return(True)
            else:
                return(False)
                    
        else:
            return(False)          

    def scry(self,scry_cards):
        scry_images = [] ##to draw on screen
        scry_images_r = [] ##for collisions
        x = 168
        y = 200
        
        for i in range(0,len(scry_cards)):
            scry_cards[i] = cards[scry_cards[i]]
            scry_images.append(pygame.image.load(scry_cards[i].cardimage).convert())
            scry_images[i] = pygame.transform.rotozoom(scry_images[i],0,0.5)
            scry_images_r.append(window.blit(scry_images[i],(x,y)))
            x += 220
            pygame.display.flip()
        chosenFlag = False
        while chosenFlag == False:            
            for event in pygame.event.get():            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(0,len(scry_images_r)):
                        if scry_images_r[i].collidepoint(pos):
                            self.hand.append(scry_cards.pop(i).name)
                            chosenFlag == True
                            update_info()
                            display_hand()
                            for i in range(0,len(scry_cards)):
                                scry_cards[i] = scry_cards[i].name
                            send_to_bottom(scry_cards)
                            return

    def draw(self,number):
        get_deck(number,'draw')
        update_server()

    def get_gold(self,extra_gold = 0):
        self.gold += 2
        update_gold()
        update_server()

    def draft_select(self,charactersRound):
        char_images = [] ##to draw on screen
        char_images_r = [] ##for collisions
        draft_coords = [(152,158),(252,158),(352,158),(452,158),(152,332),(252,332),(352,332),(452,332)]
        for i in range(0,len(charactersRound)):
            charactersRound[i] = characters[selectedCharacters[charactersRound[i]]] ###characters[name]; charactersRound are Ranks, selectedCharacters give names
            char_images.append(pygame.image.load(charactersRound[i].cardimage).convert())
            char_images[i] = pygame.transform.rotozoom(char_images[i],0,0.22790697674)
            char_images_r.append(window.blit(char_images[i],draft_coords[i]))
            pygame.display.flip()
        chosenFlag = False        
        while chosenFlag == False:            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                    
                    for i in range(0,len(char_images_r)):
                        if char_images_r[i].collidepoint(pos):
                            self.character = charactersRound.pop(i).name
                            chosenFlag == True
                            update_info()
                            update_server()
                            for i in range(0,len(charactersRound)):
                                charactersRound[i] = charactersRound[i].rank
                            ##send charactersRoundBack
                            return
                else:
                    for i in range(0,len(char_images_r)):         
                        if char_images_r[i].collidepoint(pos):
                            display = pygame.image.load(charactersRound[i].cardimage).convert()
                            display = pygame.transform.rotozoom(display,0,0.68)
                            window.blit(display,(900,15))
                            pygame.display.flip()

def warlord_draw(player):
    d_cards = []
    d_images = []
    d_images_r = []
    s = 0
    for i in range(0,len(player.board)):
        if player.board[i] != "Keep":
            d_cards.append(cards[player.board[i]])
            d_images.append(pygame.image.load(d_cards[i].cardimage).convert())
            d_images[i] = pygame.transform.rotozoom(d_images[i],0,0.2)
            d_images_r.append(window.blit(d_images[i],rank_coords[s]))
            s += 1
    pygame.display.flip()
    chosenFlag = False        
    while chosenFlag == False:            
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                    
                for i in range(0,len(d_images_r)):
                    if d_images_r[i].collidepoint(pos):
                        n.sendNoReply('destroy',d_cards[i],player.name)
                        chosenFlag == True
                        update_info()
                        return
            else:
                for i in range(0,len(d_images_r)):         
                    if d_images_r[i].collidepoint(pos):
                        display = pygame.image.load(d_cards[i].cardimage).convert()
                        display = pygame.transform.rotozoom(display,0,0.68)
                        window.blit(display,(900,15))
                        pygame.display.flip()


def get_destroyed(district,warlord):
    string = "The warlord detroyed your " + district
    update_info_box(string)
    for district_b in p.board:
        if district_b == district:
            p.board.remove(district)
            update_screen()
            return
   

def slot_to_player(slot):
    for player in opponents:
        if opponents[player][1] == slot:
            return(player)

def force_hand(newhand,magician):
    p.hand = newhand
    update_info_box("The magician swapped hands with you!")
 
def get_target(illegalTargets=[]):
    legal_targets = [2,3,4,5,6,7,8]
    for rank in illegalTargets:
        if rank in legal_targets:
            legal_targets.remove(rank)
    for rank in faceup_this_round:
        if rank in legal_targets:
            legal_targets.remove(rank)
    for rank in dead_this_round:
        if rank in legal_targets:
            legal_targets.remove(rank)
    chosenFlag = False
    while chosenFlag == False:            
        for event in pygame.event.get():            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for rank in legal_targets:
                    if rank_targets[rank-1].collidepoint(pos):
                        print("Targetting: ", rank)
                        return(rank)

def target_player(illegalTargets = [0]):
    legal_targets = [0,1,2,3,4,5,6,7] #### get this from playerlist please
    for slot in illegalTargets:
        if slot in legal_targets:
            legal_targets.remove(slot)

    chosenFlag = False
    while chosenFlag == False:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for slot in legal_targets:
                    if player_r[slot].collidepoint(pos):
                        print("Targetting: ", slot)
                        return(slot)       
    

def choice_of_two(image1,image2): ############WHILE ACTIVE BLIT ABILITY BUTTON TO CANCEL###########
    pygame.draw.rect(window,(204,102,0),pygame.Rect(152,208,598,308))
    if image2 != None:
        display1 = pygame.image.load(image1).convert()
        display1 = pygame.transform.rotozoom(display1,0,0.5)
        display2 = pygame.image.load(image2).convert()
        display2 = pygame.transform.rotozoom(display2,0,0.5)
        display1_r = window.blit(display1,(160,250))
        display2_r = window.blit(display2,(460,250))
        pygame.display.flip()
        chosenFlag = False        
        while chosenFlag == False:            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                    
                    if display1_r.collidepoint(pos):
                        update_info()
                        return(1)
                        chosenFlag == True
                    if display2_r.collidepoint(pos):
                        update_info()
                        return(2)
                        chosenFlag == True                
                    return
    else:
        display1 = pygame.image.load(image1).convert()
        display1 = pygame.transform.rotozoom(display1,0,0.5)
        display1_r = window.blit(display1,(310,250))
        pygame.display.flip()
        chosenFlag = False  
        while chosenFlag == False:            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                    
                    if display1_r.collidepoint(pos):
                        update_info()
                        return(1)
                        chosenFlag == True

        
def gather_resources():
    pygame.draw.rect(window,(204,102,0),pygame.Rect(152,208,598,308))
    scryIcon = pygame.image.load('gui/card-draw.png').convert_alpha()
    scryIcon = pygame.transform.rotozoom(scryIcon,0,0.5)
    goldIcon = pygame.image.load('gui/receive-money.png').convert_alpha()
    goldIcon = pygame.transform.rotozoom(goldIcon,0,0.5)
    scryIcon_r = window.blit(scryIcon,(160,250))
    goldIcon_r = window.blit(goldIcon,(460,250))
    pygame.display.flip()
    chosenFlag = False        
    while chosenFlag == False:            
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                    
                if scryIcon_r.collidepoint(pos):
                    update_info()
                    if 'Observatory' in p.board:
                        get_deck(3,'scry')
                    if 'Library' in p.board:
                        p.draw(2)
                    else:
                        print('scrying')
                        get_deck(2,'scry')
                    chosenFlag == True
                if goldIcon_r.collidepoint(pos):
                    print('gold')
                    update_info()
                    p.get_gold()
                    chosenFlag == True                
                return


def get_deck(numberOfCards,action): ####change this to use requests thread
    send = ("get_deck",numberOfCards,action)
    n.sendNoReply(send) ##('get_deck',listOfCards)
    return

def get_deck_receive(listOfCards,action):
    if action == "draw":
        for card in listOfCards:
            p.hand.append(card)
        display_hand()
        update_info()
    elif action == "scry":
        p.scry(listOfCards)
    pass

def send_to_bottom(cardsList):
    send = ("send_to_bottom",cardsList)
    n.sendNoReply(send)

def update_screen(): ##for in-game
    ##window.fill((40,80,120))
    window.blit(gold,(1000,700))
    pygame.draw.rect(window,(40,80,120),pygame.Rect(0,0,900,800))
    update_gold()
    display_hand()
    display_board()
    update_info()
    pygame.display.flip()

def update_info_box(text):
    pygame.draw.rect(window,(40,80,120),pygame.Rect(900,520,300,80))
    infoBox = pygame.font.SysFont('bahnschrift',25)
    infoBoxText = infoFont.render(text,True,(0,0,0),)
    w = infoBoxText.get_width()
    window.blit(infoBoxText,(1200-w-3,520))
    pygame.display.flip()
    

def display_hand():
    pygame.draw.rect(window,(40,80,120),pygame.Rect(0,680,900,120))
    global hand_collisions
    handimages = []
    hand_r = []
    y = 680
    x = 15
    print(p.hand)
    for i in range(0,len(p.hand)):
        handimages.append(pygame.image.load(cards[p.hand[i]].cardimage).convert())
        handimages[i] = pygame.transform.rotozoom(handimages[i],0,0.2)
        hand_r.append((window.blit(handimages[i],(x,y)),p.hand[i]))
        x += 80
    hand_collisions = hand_r
    pygame.display.flip()

def display_board():
    global board_collisions
    board_collions = []
    for i in range(0,len(p.board)):
        display = pygame.image.load(cards[p.board[i]].cardimage).convert()
        display = pygame.transform.rotozoom(display,0,0.1)
        board_collisions.append(((window.blit(display,boardCoords[0][i])),p.board[i]))
    for player in opponents:
        print
        for i in range(0,len(opponents[player][0].board)):
            display = pygame.image.load(cards[opponents[player][0].board[i]].cardimage).convert()
            if opponents[player][1] == 1:
                display = pygame.transform.rotozoom(display,0,0.1)
            elif opponents[player][1] == 2 or opponents[player][1] == 3:
                display = pygame.transform.rotozoom(display,90,0.1)
            elif opponents[player][1] == 4 or opponents[player][1] == 5:
                 display = pygame.transform.rotozoom(display,180,0.1)
            elif opponents[player][1] == 6 or opponents[player][1] == 7:
                 display = pygame.transform.rotozoom(display,270,0.1)
            board_collisions.append(((window.blit(display,boardCoords[opponents[player][1]][i])),opponents[player][0].board[i]))

def draw_UI_buttons():
    global UI_collisions
    UI_collisions = []
    passTurn = pygame.image.load("gui/passTurn.png").convert()
    passTurn = pygame.transform.rotozoom(passTurn,0,0.4)
    UI_collisions.append(window.blit(passTurn,(1000,650)))
    useAbility = pygame.image.load("gui/useAbility.png").convert()
    useAbility = pygame.transform.rotozoom(useAbility,0,0.4)
    UI_collisions.append(window.blit(useAbility,(1000,600)))
    pygame.display.flip()

def draw_rank_icons():
    rank_icons = []

    for i in range(0,8):
        filename = "gui/rankicon_" + str(i+1) + ".png"
        rank_icons.append(pygame.image.load(filename).convert())
        rank_icons[i] = pygame.transform.rotozoom(rank_icons[i],0,0.09765625)
        window.blit(rank_icons[i],rank_coords[i])
    cross = pygame.image.load("gui/cross-mark.png").convert_alpha()
    cross = pygame.transform.rotozoom(cross,0,0.09765625)
    for rank in faceup_this_round:
        window.blit(cross,rank_coords[rank-1])
    dead = pygame.image.load("gui/chopped-skull.png").convert()
    dead = pygame.transform.rotozoom(dead,0,0.09765625)
    for rank in dead_this_round:
        window.blit(dead,rank_coords[rank-1])
    pygame.display.flip()
        
    
def update_gold():
    pygame.draw.rect(window,(40,80,120),pygame.Rect((1100,710,120,120)))
    goldcount = oldFont.render(str(p.gold),True,(0,0,0),)
    window.blit(goldcount,(1100,710))
    pygame.display.flip()
    

def update_info(): ##profile, name, crown ,districtSet,completed ##also change this to check for conditions lmao
    pygame.draw.rect(window,(40,80,120),pygame.Rect(152,158,598,358))
    infostring = p.name + " (" + str(len(p.hand))+ ',' + str(p.gold) + ")"
    infotext = infoFont.render(infostring,True,(0,0,0),)
    for i in range(0,2):  ## Profile icon, name
        if i != 1:
            window.blit(infoIcons[i],infoCoords[0][i])
        elif i == 1:
            window.blit(infotext,infoCoords[0][i])
    if p.king == True:
        window.blit(infoIcons[2],infoCoords[0][2])
    if p.get_complete_set() == True:
        window.blit(infoIcons[3],infoCoords[0][3])
    if len(p.board) >= 7:
        window.blit(infoIcons[4],infoCoords[0][4])
    for player in opponents:
        infostring = player + " (" + str(len(opponents[player][0].hand))+ ',' + str(opponents[player][0].gold) + ")"
        infotext = infoFont.render(infostring,True,(0,0,0),)
        for i in range(0,2): ## Profile icon, name
            if i != 1:
               window.blit(infoIcons[i],infoCoords[opponents[player][1]][i])
            elif i == 1:
                if infoCoords[opponents[player][1]][i][0] == "calculate":
                    width = infotext.get_width()
                    newCoords = (infoCoords[opponents[player][1]][i][1] - width - 3,
                                 infoCoords[opponents[player][1]][i][2])
                    window.blit(infotext,newCoords)
                else:
                    window.blit(infotext,infoCoords[opponents[player][1]][i])

        if opponents[player][0].king == True:
            window.blit(infoIcons[2],infoCoords[opponents[player][1]][2])
        if opponents[player][0].get_complete_set() == True:
            window.blit(infoIcons[3],infoCoords[opponents[player][1]][3])
        if len(opponents[player][0].board) >= 7:
            window.blit(infoIcons[4],infoCoords[opponents[player][1]][4])
    draw_rank_icons()
    pygame.display.flip()

def draw_magician_cycle(selectedCards):
    print(selectedCards)
    magicianTrash = pygame.image.load('gui/trash-can.png').convert_alpha()
    magicianTrash = pygame.transform.rotozoom(magicianTrash,0,0.05)
    magicianCoordX = 45
    y = 660
    pygame.draw.rect(window,(40,80,120),pygame.Rect(35,660,700,20))
    for index in selectedCards:
        window.blit(magicianTrash,(magicianCoordX + 80*index,y))
    
def collisions_thread():
    magicianSelect = []    
    LabFlag = False
    
    while True:
        print("collisions ON")
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in hand_collisions:
                    if card[0].collidepoint(pos):
                        
                        if LabFlag == True: ##Lab Choose discard ability                           
                            print(card[1])
                            LabFlag = False
                            lab_ability(card[1])

                        elif magicianFlag == True:
                            for i in range(0,len(p.hand)):
                                if p.hand[i] == card[1]:
                                    if i in magicianSelect:
                                        magicianSelect.remove(i)
                                        draw_magician_cycle(magicianSelect)
                                    else:
                                        magicianSelect.append(i)
                                        draw_magician_cycle(magicianSelect)
                                            
                        else:                          
                            build(card[1])
                            
                for i in range(0,len(UI_collisions)):
                    if UI_collisions[i].collidepoint(pos):
                        if i == 0:
                            pass_turn()
                        elif i == 1:
                            if magicianFlag == True:
                                magicianSwap(magicianSelect)
                                magicianSelect = []
                            else:
                                p.use_ability()

                for card in board_collisions:
                    if card[0].collidepoint(pos):
                        if cards[card[1]].name ==  "Laboratory" and "Laboratory" in p.board:
                            update_info_box("Choose a card to discard.")
                            print("LAB ABILITY")
                            LabAbility = True
                        if cards[card[1]].name ==  "Smithy" and "Smithy" in p.board:
                            print("SMITHY ABILITY")
                            smithy_ability()
                        
            else:
                for card in hand_collisions:                    
                    if card[0].collidepoint(pos):
                        display = pygame.image.load(cards[card[1]].cardimage).convert()
                        display = pygame.transform.rotozoom(display,0,0.68)
                        pygame.draw.rect(window,(40,80,120),pygame.Rect(900,15,293,502))
                        window.blit(display,(900,15))
                        pygame.display.flip()
                for card in board_collisions:
                    if card[0].collidepoint(pos):
                        display = pygame.image.load(cards[card[1]].cardimage).convert()
                        display = pygame.transform.rotozoom(display,0,0.68)
                        pygame.draw.rect(window,(40,80,120),pygame.Rect(900,15,293,502))
                        window.blit(display,(900,15))
                        pygame.display.flip()

def magicianSwap(listOfCards):
    toRemove = []
    for index in listOfCards:
        toRemove.append(p.hand[index])
    for card in toRemove:
        p.hand.remove(card)
    send_to_bottom([toRemove])
    p.draw(len(listOfCards))
    display_hand()
    draw_magician_cycle([])
    update_server()
        


def lab_ability(card):
    send_to_bottom([card])
    p.hand.remove(card)
    p.gold += 1
    display_hand()
    update_info()
    update_gold()
    update_server()

def smithy_ability():
    if p.gold >= 2:
        p.gold -= 2
        p.draw(3)
        display_hand()
        update_info()
        update_gold()
    update_server()
    
def build(buildcard):
    if p.buildlimit > 0:
        p.buildlimit -=1
        for i in range(0,len(p.hand)):
            print(p.hand[i] , buildcard)
            if p.hand[i] == buildcard:
                index = i

        global board_collisions
        if p.gold >= cards[p.hand[index]].cost:
            p.gold -= cards[p.hand[index]].cost
            p.board.append(p.hand[index])        
            p.hand.pop(index)
            update_screen()
            update_server()

    
def update_opponents(playername,playerObject):
    opponents[playername] = playerObject

def load_cards():
    dictionary = {}
    carddata = open('cardlist.dat','r')
    newline = carddata.readline()
    newline = carddata.readline()    
    while "END OF" not in newline:
        newline = newline.strip('\n').split('|')
        cardimage = "cardImages/"+newline[4]
        dictionary[newline[0]] = Card(newline[0],int(newline[2]),newline[1],newline[5], newline[3],cardimage)
        newline = carddata.readline()
    carddata.close()
    return(dictionary)

def load_characters():
    dictionary = {}
    chardata = open('characterlist.dat','r')
    newline = chardata.readline()
    newline = chardata.readline()    
    while len(newline) != 0:
        newline = newline.strip('\n').split('|')
        imageline = 'characterImages/' + newline[3]
        dictionary[newline[1]]= Character(newline[1],newline[0],newline[2],imageline)
        newline = chardata.readline().strip('\n')
    return(dictionary)

def playerToList(playerObject):
    playerList = []
    playerList.append(playerObject.name)
    playerList.append(playerObject.character)
    playerList.append(playerObject.gold)
    playerList.append(playerObject.hand)
    playerList.append(playerObject.board)
    playerList.append(playerObject.king)
    playerList.append(playerObject.buildlimit)
    return(playerList)

def listToPlayer(playerList):
    global opponents
    opponents[playerList[0]][0] = Player(playerList[0],
                                      playerList[1],
                                      playerList[2],
                                      playerList[3],
                                      playerList[4],
                                      playerList[5],
                                      playerList[6])
    
def update_opponents(listOfStuff): ##refresh all opponents on client;from server status_update()
    for item in listOfStuff:
        listToPlayer(item[1])

def update_server():
    n.sendNoReply(('update',playerToList(p)))

def start_turn():
    global activeTurn
    global abilityTurn
    abilityTurn = [True,True]
    activeTurn = True
    if characters[p.character].rank in dead_this_round:
        update_info_box("You were assassinated this round.")
        return
    if p.character == "King":
        p.king = True
        n.sendNoReply(('remove_king',p.name))
    
    if p.character == "Architect":
        update_info_box("Your build limit is three.")
        p.buildlimit = 3
    else:
        p.buildlimit = 1

    if characters[p.character].rank in robbed_this_round:
        update_info_box("You were robbed this round!")
        gold = p.gold
        n.sendNoReply(('robbery',p.gold))
        p.gold = 0
    gather_resources()
    
def pass_turn():
    global activeTurn
    n.sendNoReply(('pass_turn'))
    activeTurn = False

def slot_opponents(listOfStuff): ##[[playername,playerList,truePlayerSlot]]
    global opponents
    template = slot_templates[len(listOfStuff)-1]
    found_player = False
    for item in listOfStuff:
        if item[0] == p.name:
            found_player = True
        if item[0] != p.name and found_player == True:
            opponents[item[0]] = [0,0]
            listToPlayer(item[1])
            opponents[item[0]][1] = template.pop()
    for i in range(0,len(template)):
        opponents[listOfStuff[i][0]] = [0,0]
        listToPlayer(listOfStuff[i][1])
        opponents[listOfStuff[i][0]][1] = template.pop()   
        
    
    

def requests_thread():
    run = True
    while run == True:
        print(opponents)
        receive = n.receive()
        print("receive: ",receive)
        if receive != None:
            if receive[0] == 'update': ##('playerupdate','playername',players_conn[playername])
                update_opponents(receive[1],receive[2])
            elif receive[0] == 'get_deck':
                get_deck_receive(receive[1],receive[2])
            elif receive[0] == 'new_hand':
                force_hand(receive[1],receive[2])
            elif receive[0] == 'destroy':
                get_destroyed(receive[1],receive[2])
            elif receive[0] == 'player_update':
                update_opponents(receive[1])
            elif receive[0] == 'remove_crown':
                update_info_box("You lost the crown!")
                p.king = False
            elif receive[0] == 'get_loot':
                p.gold += receive[1]
                update_gold()
            elif receive[0] == 'playerupdate':
                listToPlayer(receive[1])
            elif receive [0] == 'all_opponent_update':
                slot_opponents(receive[1])
                
            
opponents = {} ##[playerObjects,displaySlotNo] with their names as the key
n = Network()

name = startscreen.main(window,n)
p = Player(name)   
    

window.fill((40,80,120))
gold = pygame.image.load("gui/gold.png").convert_alpha()
gold = pygame.transform.rotozoom(gold,0,1,)
oldFont = pygame.font.SysFont("gui/BLKCHCRY.TTF",100)
goldcount = oldFont.render(str(p.gold),True,(0,0,0),)
profile = pygame.image.load("gui/gluttony.png").convert()
profile = pygame.transform.rotozoom(profile,0,0.07815)
crown = pygame.image.load("gui/crown.png").convert()
crown = pygame.transform.rotozoom(crown,0,0.05859375)
districtSet = pygame.image.load("gui/star-formation.png").convert()
districtSet = pygame.transform.rotozoom(districtSet,0,0.05859375)
completed = pygame.image.load("gui/podium-winner.png").convert()
completed = pygame.transform.rotozoom(completed,0,0.05859375)
infoIcons = [profile,None,crown,districtSet,completed]
infoFont = pygame.font.SysFont('bahnschrift',20)



draw_UI_buttons() 

slot_templates = [None,[5],[4,5],[1,4,5],[1,2,4,5],[1,2,4,5,7],[1,2,3,4,5,7],[1,2,3,4,5,6,7]] ##slots for len(players)
start_new_thread(requests_thread,())


cards = load_cards() ##cardObjects with cardname as key
characters = load_characters() ##characterObjects with character name as key

start_new_thread(collisions_thread,())
update_info()
update_screen()
draw_rank_icons()

time.sleep(1)
p.draw(2)
time.sleep(1)
p.draft_select([1,2,3,4,5,6,7,8])
gather_resources()

run = True


while run == True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

        
