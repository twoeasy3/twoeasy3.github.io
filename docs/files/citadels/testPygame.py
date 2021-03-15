import pygame
import time

pygame.init()
clock = pygame.time.Clock()
window_w = 1200
window_h = 800
window = pygame.display.set_mode((window_w,window_h))
window.fill((255,255,255))
pygame.display.set_caption("Citadels P2W Edition")
images = []
images.append(pygame.image.load('cardImages/card_library.png').convert())
images.append(pygame.image.load('cardImages/card_monastery.png').convert())
images.append(pygame.image.load('cardImages/card_greatWall.png').convert())
image_r = []
x = 0
for i in range(0,len(images)):
    images[i] = pygame.transform.rotozoom(images[i],0,0.5)
    image_r.append(window.blit(images[i],(x,0)))
    x += 220
    print(x)    
pygame.display.flip()
while True:
    clock.tick(60)
    for i in range(0,len(images)):
        if image_r[i].collidepoint(pygame.mouse.get_pos()):
                print("hovering",[i])
        for event in pygame.event.get():            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if image_r[i].collidepoint(pos):
                    print("click click")
        
