import pygame
import socket
from _thread import *

class startFlag(object):
    def __init__(self,flagStatus):
        self.Flag = flagStatus
        self.opponents = []

def main(window,n):
    sf = startFlag(False)
    pygame.init()
    clock = pygame.time.Clock()
    infoFont = pygame.font.SysFont('bahnschrift',50)
    askText = infoFont.render("Please enter your name (max. 10 char)",True,(0,0,0),)
    queueText = infoFont.render("Players in room: ",True,(0,0,0),)
    window.blit(askText,(50,120))
    window.blit(queueText,(50,270))
    start_game = pygame.image.load('gui/start_game.png').convert()
    start_game = pygame.transform.rotozoom(start_game,0,0.3)
    start_game_r = window.blit(start_game,(650,200))

    pygame.draw.rect(window,(255,255,255),pygame.Rect((50,200,400,60)))
    pygame.display.flip()
    name = ''

    entered = False
    while entered == False:
        for event in pygame.event.get():            
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum():
                    if len(name) >= 10:
                        pass
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    pygame.draw.rect(window,(255,255,255),pygame.Rect((50,200,400,60)))
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        entered = True
                        receive = n.connect() ## pickle is done in network.py
                        if receive == "player_request":
                            h = n.sendNoReply(name)
                            nameText = infoFont.render(name,True,(0,0,0),)
                            window.blit(nameText,(50,330))

                    
                
        infotext = infoFont.render(name,True,(0,0,0),)
        window.blit(infotext,(50,200))
        pygame.display.flip()

    start_new_thread(room_update,(n,window,name,sf))
    while sf.Flag == False:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_game_r.collidepoint(pos):
                    n.sendNoReply(('start_game',0))
    if sf.Flag == True:
        return(name)
        
def room_update(n,window,name,sf):
    gameStart = False
    infoFont = pygame.font.SysFont('bahnschrift',50)
    while gameStart == False:
        print('yes')
        receive = n.receive()
        print(receive)
        if receive != None:
            if receive[0] == 'room_update':
                y = 400
                pygame.draw.rect(window,(40,80,120),pygame.Rect((50,400,400,600)))
                for player in receive[1]:
                    if player not in sf.opponents and player != name:
                        sf.opponents.append(player)
                    if player != name:
                        nameText = infoFont.render(player,True,(0,0,0),)
                        window.blit(nameText,(50,y))
                        y+=70
                        pygame.display.flip()
            elif receive[0] == 'start_game':
                sf.Flag = True
                gameStart = True
                return(True)
            
            
                
                    
               
        
