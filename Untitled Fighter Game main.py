import pygame

pygame.init()

#game window
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Untitled Fighter Game")


#load background - from: https://wallpapercave.com/landscape-pixel-art-wallpapers
bg_image = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ImageBG.jpg").convert_alpha()

#bg draw function
def drawBG():
    screen.blit(bg_image,(0,0))




#game loop
run = True
while run:


    #draw bg
    drawBG()

    #events
    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False


    


    #update display
    pygame.display.update()




#exit pygame
pygame.quit()
