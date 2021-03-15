import socket
from _thread import *
import sys
import pickle
import random


server = "192.168.1.123"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


charToRank = {"Assassin" : 1,
              "Thief": 2,
              "Magician":3,
              "King":4,
              "Bishop":5,
              "Merchant":6,
              "Architect":7,
              "Warlord":8}


def get_cards():
    deck = []
    carddata = open('cardlist.dat','r')
    newline = carddata.readline()
    newline = carddata.readline()
    while "END OF" not in newline:
        newline = newline.strip('\n').split('|')
        for i in range(0,int(newline[3])):## no. of copies in deck
            deck.append(newline[0])
        newline = carddata.readline()
    carddata.close()
    random.shuffle(deck)
    return(deck)


deck = get_cards() ##list of cardnames
characters = [1,2,3,4,5,6,7,8]##character ranks
current_characters = []

def start_draft(characters,crown):
    global current_characters
    current_characters = characters
    if len(players_conn) == 4 or len(players_conn) == 3:
        faceup = random.sample(current_characters,2)
        ##draw faceup ## draw in client
        replyString = pickle.dumps(("faceup_cards",faceup))
        for player in player_slots:
            player.send(replyString)
        for rank in faceup:
            current_characters.remove(rank)
    elif len(player_conn) == 5:
        faceup = random.sample(current_characters,1)
        ##draw faceup
        replyString = pickle.dumps(("faceup_cards",faceup))
        for player in player_slots:
            player.send(replyString)
        current_characters.remove(faceup[0])
    
    facedown = random.sample(current_characters,1)
    replyString = pickle.dumps(("facedown_cards",faceup))
    for player in player_slots:
        player.send(replyString)
    current_characters.remove(facedown[0])
    draft_pass(current_characters,None)

def draft_pass(characters,fromplayer): ##client to use sendNoReply
    if len(characters) == 1 and len(players_conn) != 7:
        return
    if fromplayer == None:
        for player in players_conn:
            if player[1][4] == True: ###index 4 is King status
                passString = pickle.dumps(("draft_pass",characters))
                player[0].send(passString)
    else:
        playerslot = players_conn[fromplayer][2]
        if playerslot == len(players_conn)-1:
            nextslot = 0
        else:
            nextslot = playerslot + 1
        passString = pickle.dumps(("draft_pass",characters)) 
        players_slots[nextslot].send(passString)
       


def get_deck(numberOfCards):
    global deck
    listOfCards = []
    for i in range(0,numberOfCards):
        listOfCards.append(deck.pop(0))
    return(listOfCards)

def send_to_bottom(listOfCards):
    global deck
    print(deck)
    for card in listOfCards:
        deck.append(card)
    print(deck)
    pass



players_conn = {} ##dictionary of (connSocket,[playerObjectList],trueSlotNumber)s with their name as key
players_slots = {} ##dictionary of (connSocket) with their slots as key
player_names = []
dead_this_round = []
robbed_this_round = []
not_used_this_round = [] ##faceup,facedown and dead


##DO THIS AT START OF GAME##
slot = 0
for player in players_conn:
    player.append = slot
    players_slots[slot] = player[0]
    slot += 1
##DO THIS AT START OF GAME##
    

def update_opponents(playerList):
    update = ('playerupdate',playerList[0],playerList)
    updateP = pickle.dumps(update)
    for player in players_conn:
        if player != playername:
            players_conn[player][0].send(updateP)

def update(playerList):
    players_conn[playerList[0]][1] = playerList
    update_opponents(playerList)

def status_update():
    newList = [] ##name,playerList,slot
    for player in players_conn:
        newList.append([player,players_conn[player][1],players_conn[player][2]])
        newListP = pickle.dumps(('all_opponent_update',newList))
    for player in players_conn:
        print("sending to",player)
        players_conn[player][0].send(newListP)
        

def next_turn(playername):
    character = players_conn[playername][1][1]
    characterRank = charToRank[character]
    lookingFor = characterRank + 1
    while lookingFor not in not_used_this_round:
        lookingFor = characterRank + 1
    if lookingFor <= 8:
        for player in players_conn:
            if lookingFor == charToRank[players_conn[player][1][1]]:
                ##sendTurn(player)
                pass

def force_hand(newhand,target,magician):
    sendstring = pickle.dumps(("new_hand",newhand,magician))
    players_conn[target][0].send(sendstring)

def force_destroy(district,target,warlord):
    sendstring = pickle.dumps(("destroy",district,warlord))
    players_conn[target][0].send(sendstring)

def start_game():
     for player in player_names:
        connP = pickle.dumps(('start_game',0))
        players_conn[player][0].send(connP)

def update_room():
    for player in player_names:
        connP = pickle.dumps(('room_update',player_names))
        players_conn[player][0].send(connP)

def change_crown(newKing):
    for player in players_conn:
        if players_conn[player][1][5] == True:
            players_conn[player][1][5] = False
            p = pickle.dumps(('remove_crown'))
            players_conn[player][0].send(p)
    
    players_conn[player][1][5] = True

def robbery(gold):
    for player in players_conn:
        if players_conn[player][1][1] == 'Thief':
            p = pickle.dumps(('get_loot',gold))
            players_conn[player][0].send(p)

def assassinate(deadRank):
    deadUpdate = pickle.dumps(('deaded',deadRank))
    for player in player_names:
        players_conn[player][0].send(deadUpdate)

def startRob(robbedRank):
    robUpdate = pickle.dumps(('robbed',deadRank))
    for player in player_names:
        players_conn[player][0].send(robUpdate)
        
    

slot_number = 0

def threaded_client(conn,hippo):
    global players_conn
    global player_names
    global slot_number
    sendP = pickle.dumps("player_request")
    conn.send(sendP)
    playerdataP = conn.recv(2048)
    acknowledgeP = pickle.dumps("acknowledged.")
    conn.send(acknowledgeP)
    print("PLAYERDATAP: ",playerdataP)
    playername = pickle.loads(playerdataP) ##(playername,playerObject made into list)
    newplayerlist = [playername,None,2,[],[],False,1]

    players_conn[playername] = [conn,newplayerlist,slot_number]
    
    slot_number += 1
    player_names.append(playername)
    
    update_room()
    update_room()

        
    while True:
        try:
            data = (conn.recv(2048))
            print(data)
            decoded = pickle.loads(data)
            print(decoded)
            if decoded != "ping":
                if decoded[0] == 'draft_pass':
                    draft_pass()
                elif decoded[0] == 'get_deck': ##returns list of cards from top of deck
                    cards = ('get_deck',get_deck(decoded[1]),decoded[2])
                    cardsP = pickle.dumps(cards)
                    conn.send(cardsP)
                elif decoded[0] == 'send_to_bottom':
                    send_to_bottom(decoded[1])
                elif decoded[0] == 'update': ###after an action is done, return player object   
                    update(decoded[1])
                elif decoded[0] == 'pass_turn':
                    next_turn(playername)
                elif decoded[0] == 'new_hand':
                    force_hand(decoded[1],decoded[2],playername)
                elif decoded[0] == 'destroy':
                    force_destroy(decoded[1],decoded[2],playername)
                elif decoded[0] == 'start_game':       
                    start_game()
                    status_update()
                elif decoded[0] == 'player_update':
                    status_update()
                elif decoded[0] == 'remove_king':
                    change_crown(decoded[1])
                elif decoded[0] == 'robbery':
                    robbery(decoded[1])
                elif decoded[0] == 'assassinate':
                    assassinate(decoded[1])
                elif decoded[0] == 'robbed':
                    startRob(decoded[1])
            

            if not data:
                print("Disconnected")
                break
            else:
                pass
        except:
            pass
            #break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,"hippo"))
    
    currentPlayer += 1
